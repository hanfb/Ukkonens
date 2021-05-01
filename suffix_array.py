"""
Assignment 2 Q2
Author: Kevin Lew
Student ID: 29677475
"""

from Ukkonens import ukkonens
import sys

def suffix_array(tree):
    """generates the suffix array from a given suffix tree by dfs

    Args:
        tree (Ukkonens): suffix tree 
    """
    root = tree.root
    edges = root.edges
    suffix_array = [[]] # pointer for suffix array
    w = tree.word
    traversal(root, suffix_array, tree)
    r = []
    for i in suffix_array[0]:
        r.append(i)
    write_file(r)

def traversal(node, s, t):
    """sorting the edges by ascending order while dfs traversal

    Args:
        node (Node): root of Ukkonens suffix tree
        s (List[List[int]]): pointer to suffix_array 
        t (Ukkonens): instance of Ukkonens suffix tree
    """
    node.edges.sort(key=t.takeInd)
    for i in range(node.get_len()):
        e = node.get_edge(i)
        if e.start > -1:
            if e.dest.suffixind > -1:
                s[0].append(e.dest.suffixind) # append suffix index (starting index of suffix) to pointer
            traversal(e.dest, s, t)

def read_file(fileN):
    """opens file and returns the word inside file

    Args:
        fileN (str): name of file to be opened

    Returns:
        str: word within the file
    """
    f = open(fileN, "r")
    return f.read()

def write_file(suffix_array):
    """writes the suffix arrays into the output file

    Args:
        suffix_array (List[int]): List of suffix start index representing the suffix array
    """
    f = open("output_suffix_array.txt", "w")
    for i in suffix_array:
        f.write(str(i) + "\n")

def main():
    """prepares word for operation and runs suffix_array
    """
    w = read_file(sys.argv[1])+"$"
    suffix_array(ukkonens(w))

if __name__ == "__main__":
    main()