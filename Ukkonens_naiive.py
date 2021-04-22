class Node():
    def __init__(self):
        self.edges = []

    def is_leaf(self):
        if len(self.edges) > 0:
            False
        else:
            True
    
    def get_len(self):
        return len(self.edges)

    def get_edge(self, ind):
        return self.edges[ind]
    
    def new_edge(self, edge):
        self.edges.append(edge)

class Edge():
    def __init__(self, s, d, n_start, n_end):
        self.source = s
        self.dest = d
        self.start = n_start
        self.end = n_end

    def increment(self):
        self.end += 1
    
    def re_direct(self, n_dest, n_end):
        self.dest = n_dest
        self.end = n_end

class Ukkonens():
    def __init__(self, wrd):
        self.word = wrd
        self.root = None
        self.edges = []
        self.create_tree()

    def create_tree(self):
        self.root = Node()
        wrd = self.word
        s = len(wrd)
        for i in range(s):
            phase = i+1
            for j in range(phase):
                start = j
                end = i
                self.perform_rule(start, end)
    
    def perform_rule(self, s, e):
        node = self.root
        w = self.word
        edge = self.find_edge(s, node)
        if edge.source is not None:
            last_ind = 0
            n = edge.start
            cnt = 0
            for i in range(s, e+1):
                last_ind = i
                if cnt >= edge.end + 1:
                    old_e = edge
                    edge = self.find_edge(i, edge.dest)
                    if edge.source is None: 
                        edge = old_e
                        break
                    else: 
                        n = edge.start
                if w[i] != w[n]:
                        break
                n += 1 
                cnt += 1
            # rule 1
            if last_ind == edge.end+1:
                edge.increment()
            # don't do anything if rule 3
            elif cnt < e - s + 1:
                # rule 2ii 
                n_node = Node()
                n_e2 = Edge(n_node, edge.dest, n, edge.end)
                n_e3 = Edge(n_node, Node(), last_ind, e)
                self.edges.append(n_e2)
                self.edges.append(n_e3)
                n_node.new_edge(n_e3)
                n_node.new_edge(n_e2)
                edge.re_direct(n_node, n-1)
        else:
            # rule 2i
            n_edge = Edge(self.root, Node(), s, e)
            self.edges.append(n_edge)
            self.root.new_edge(n_edge)
    
    def find_edge(self, s, node):
        w = self.word
        r = Edge(None, None, None, None)
        for i in range(node.get_len()):
            edge = node.get_edge(i)
            if w[edge.start] == w[s]:
                r = edge
                break
        return r

    def disp_edges(self):
        edges = self.edges
        for i in edges:
            print("start val: ", i.start, "end val: ", i.end)

def main():
    wrd = "abac$"
    tree = Ukkonens(wrd)
    tree.disp_edges()

if __name__ == "__main__":
    main()