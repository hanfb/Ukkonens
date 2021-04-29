from Ukkonens import ukkonens

def traversal(node):
    for i in range(node.get_len()):
        if not node.is_leaf():
            e = node.get_edge(i)
            if e.start > -1:
                print(e.start)
                traversal(e.dest)


def main():
    w = "mississippi$"
    traversal(ukkonens(w).root)
    

if __name__ == "__main__":
    main()