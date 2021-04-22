from suffix_trees import STree

class Node(object):
    """A node in the suffix tree. 
    
    suffix_node
        the index of a node with a matching suffix, representing a suffix link.
        -1 indicates this node has no suffix link.
    """
    def __init__(self):
        self.edge = []

class Edge(object):
    def __init__(self, data, src_node, dst_node):
        self.data = data
        self.src = src_node
        self.dst = dst_node
     
class SuffixTree(object):
    """A suffix tree for string matching. Uses Ukkonen's algorithm
    for construction.
    """
    def __init__(self, string):
        """
        string
            the string for which to construct a suffix tree
        """
        self.string = string
        self.N = len(string) 
        self.tree = [Node()]
        self.edges = []
        self.size = len(self.tree)
        self.suffix = []
        self.create()
    
    def create(self):
        self.process_sfx()
        for i in range(len(self.suffix)):
            wrd = self.suffix[i]
            self.add_sfx(wrd)
      
    def process_sfx(self):
        sfx = []
        for i in range(self.N):
            sfx.append(self.string[i:self.N]+"$")
        sfx.append("$")
        self.suffix = sfx

    def add_sfx(self, wrd):
        root = self.tree[0]
        if len(self.tree) == 1:
            # add new edge to root node
            n_edge = Edge(wrd, self.tree[0], Node())
            root.edge.append(n_edge)
            self.edges.append(n_edge)
        curr_n = root
        trav_e = self.new_edge(curr_n, wrd[0])
        sta = 0
        stp = 0
        if trav_e is not None:
            for i in range(1, len(wrd)):
                if i >= len(trav_e.data):
                    # detect new edge required
                    sta = i
                    curr_n = trav_e.dst
                    trav_e = self.new_edge(curr_n, wrd[i])
                if trav_e is None or trav_e.data[i-sta] != wrd[i]:
                    # detect mismatch or no valid edges for next traversal
                    stp = i
                    break
            # branch new node
            n_node = Node()
            dst = trav_e.dst
            trav_e.dst = n_node
            trav_e.data = wrd[sta:stp]
            n_node.edge.append(Edge(wrd[stp-1::], n_node, Node()))
            self.edges.append(Edge(wrd[stp-1::], n_node, Node()))
            n_node.edge.append(Edge(trav_e.data[stp-1::], n_node, dst))
            self.edges.append(Edge(trav_e.data[stp-1::], n_node, dst))
        else:
            # add new edge to root node
            n_edge = Edge(wrd, self.tree[0], Node())
            root.edge.append(n_edge)
            self.edges.append(n_edge)

    @staticmethod
    def new_edge(node, cha):
        edge = Edge(-1, Node(), Node())
        if len(node.edge) > 0:
            for i in range(len(node.edge)):
                if node.edge[i].data[0] == cha:
                    edge = node.edge[i]
        if edge.data == -1:
            return None
        return edge
    
    def __repr__(self):
        s = ""
        for i in range(len(self.edges)):
            s += self.edges[i].data + "\n"
        return repr(s)
    
def main():
    tree = SuffixTree("abcd")
    print(repr(tree))

if __name__ == "__main__":
    main()