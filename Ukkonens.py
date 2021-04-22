class Node():
    def __init__(self):
        self.edges = []

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
    
    def re_direct(self, n_dest, n_end):
        self.dest = n_dest
        self.end = n_end

class Ukkonens():
    def __init__(self, wrd):
        self.word = wrd
        self.root = Node()
        self.edges = []
        self.lastj = -1
        self.split = -2 # 
        self.implicit = 0
        self.lr3 = False # indicates if last performed rule was rule 3
        self.n_sfxLink = True 
        self.laste = Edge(None, None, None, None)
        self.lastn = Node()
        self.showstopper = False
        self.an = self.root # active node
        self.globalEnd = [-1]
        self.remainder = [-1, -1] # [-1, -1] = empty string
        # BEGIN THE CYCLE OF LIFE
        self.create_tree()

    def create_tree(self):
        # suffix link 
        n_e = Edge(self.root, self.root, -1, [-1])
        self.root.new_edge(n_e)
        self.edges.append(n_e)
        lastS = -2
        lastn = Node()
        wrd = self.word
        s = len(wrd)
        for i in range(s):
            self.showstopper = False
            self.globalEnd[0] += 1
            phase = i+1
            for j in range(self.lastj+1, phase):
                if self.showstopper: 
                    break
                start = j
                end = i
                # 0 = n, 1 = cnt, 2 = last_ind, 3 = s
                r = self.traverse(start, end)
                self.makeExtension(r[0], r[1], r[2], start, end)
                # lastS, lastn is the previous extension values
                self.resolveSuffixLinks(lastS, lastn, phase)
                lastS = self.split
                lastn = self.lastn
                self.moveToNextExtension(j, phase, r[0], r[3])
    
    def moveToNextExtension(self, extension, phase, n, s):
        node = self.an
        # rule 2
        if not self.lr3:
            # traverse out suffix link
            self.an = self.find_edge(-1, node).dest
            if self.an == self.root:
                # manual remainder reduction - implicit remainder reduction
                self.remainder[0] += 1 - self.implicit
                # set remainder to 'empty'
                if self.remainder[0] > self.remainder[1]:
                    self.remainder[0] = -1
                    self.remainder[1] = -1
        # rule 3
        else:
            # activate show stopper and increment/initialise remainder
            self.showstopper = True
            if self.remainder[0] == -1:
                self.remainder[0] = extension
                self.remainder[1] = phase-1
            else: 
                self.remainder[0] = s
                self.remainder[1] += 1

    def traverse(self, s, e):
        node = self.an
        cnt = 0
        w = self.word
        if self.remainder[0] != -1:
            temp = s
            # begin from remainder
            s = self.remainder[0]
            # increment count by number of skips before traverse due to remainder and active node
            cnt = s - temp
            # implicit remainder reduction
            self.implicit = s - temp
            # amount of skips available for skip counting 
            skip_dist = self.remainder[1] - self.remainder[0] + 1
        else:
            skip_dist = 0
        edge = self.find_edge(s, node)
        # skip count
        if edge.source is not None:
            edge_len = edge.end[0]-edge.start+1
            # keep traversing edges via skip counting
            while edge.source is not None and skip_dist >= edge_len:
                skip_dist -= edge_len
                # increment counter and start pointer by amount of length just skipped
                s += edge_len
                cnt += edge_len
                # set active node to new node
                self.an = edge.dest
                edge = self.find_edge(s, edge.dest)
                if edge.source is not None: edge_len = edge.end[0]-edge.start+1
            # if edge length is enough then skip count
            if edge.source is not None and edge_len >= skip_dist+s:
                # increment start pointer and counter by amount of length just skipped
                s += skip_dist
                cnt += skip_dist
                n = edge.start + skip_dist
            else:
                n = edge.start
        # naiive traversal
        # note: n is pointer pointing to edge character for comparison with word character
        if edge.source is not None:
            last_ind = 0
            for i in range(s, e+1):
                last_ind = i
                if w[i] != w[n]:
                        break
                n += 1 
                cnt += 1
        else:
            # make sure n and last_ind is declared
            n, last_ind = 0, 0
        # indicate edge for extensions to be performed on
        self.laste = edge
        # RETURN S VALUE BEFORE SKIP COUNT TO CALCULATING REMAINDER FOR NEXT EXTENSION
        return n, cnt, last_ind, s-skip_dist

    def resolveSuffixLinks(self, lastS, lastn, phase):
        j = self.lastj
        # if last rule 2ii was just performed and any rule 2 was performed before it
        if j == lastS + 1 and self.n_sfxLink:
            # create suffix link from last branch node created from rule 2 to current active node
            n_e = Edge(lastn, self.an, -1,[-1])
            lastn.new_edge(n_e)
            self.edges.append(n_e)
    
    def makeExtension(self, n, cnt, last_ind, s, e):
        # note: any rule 2 deactivates show stopper
        edge = self.laste
        if edge.source is not None:
            # rule 2
            if cnt < e - s + 1:
                # rule 2ii
                self.n_sfxLink = True
                self.lastj = s 
                self.split = s
                n_node = Node()
                # DO NOT CREATE NEW EDGE IF LEFTOVER EDGE REMAINS CONSTANT
                if edge.end[0] >= n:
                    n_e2 = Edge(n_node, edge.dest, n, edge.end)
                    self.edges.append(n_e2)
                    n_node.new_edge(n_e2)
                n_e3 = Edge(n_node, Node(), last_ind, self.globalEnd)
                self.edges.append(n_e3)
                n_node.new_edge(n_e3)
                self.lastn = n_node
                edge.re_direct(n_node, [n-1])
                self.lr3 = False
            # rule 3
            else:
                # don't create new suffix link
                self.n_sfxLink = False
                # show stopper ACTIVATE
                self.lr3 = True
        else:
            # rule 2i
            self.n_sfxLink = True
            self.lastj = s
            n_node = Node()
            if self.an != self.root:
                # increment start pointer by length skipped during skip counting
                s += self.remainder[1] - self.remainder[0] + 1
            n_edge = Edge(self.root, n_node, s, self.globalEnd)
            self.edges.append(n_edge)
            self.an.new_edge(n_edge)
            self.lr3 = False

    def find_edge(self, s, node):
        w = self.word
        r = Edge(None, None, None, None)
        for i in range(node.get_len()):
            edge = node.get_edge(i)
            if w[edge.start] == w[s] and (edge.start > -1 or s == -1):
                r = edge
                break
        return r

    def disp_edges(self):
        edges = self.edges
        for i in edges:
            print("start val: ", i.start, "end val: ", i.end[0])
    
def main():
    wrd = "abacabad"
    tree = Ukkonens(wrd)
    tree.disp_edges()

if __name__ == "__main__":
    main()