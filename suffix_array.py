from Ukkonens import ukkonens

def suffix_array(tree):
        root = tree.root
        edges = root.edges
        suffix_array = [[]]
        w = tree.word
        traversal(root, suffix_array, tree)
        r = []
        for i in suffix_array[0]:
            r.append(i)
        print(r)

def traversal(node, s, t):
    node.edges.sort(key=t.takeInd)
    for i in range(node.get_len()):
        e = node.get_edge(i)
        if e.start > -1:
            if e.dest.suffixind > -1:
                s[0].append(e.dest.suffixind)
            traversal(e.dest, s, t)

def main():
    w = "mississippi$"
    suffix_array(ukkonens(w))

if __name__ == "__main__":
    main()