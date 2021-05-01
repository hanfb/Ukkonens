"""
Assignment 2 Q3
Author: Kevin Lew
Student ID: 29677475
"""

from Ukkonens import ukkonens
import sys

def lcp(s1, s2, l_pairs):
    """finds the longest prefix common to the suffix of two different strings 

    Args:
        s1 (str): first string which is the prefix string
        s2 ([type]): second string which is the suffix string
        l_pairs (List(tuple(int, int))): List of L pair values 
    """
    output = []
    for i in range(len(l_pairs)):
        l = l_pairs[i]
        s1_temp = shorten(l[0], s1)
        s2_temp = shorten(l[1], s2)
        t1 = ukkonens(s1_temp)
        t2 = ukkonens(s2_temp)
        sfx1 = gen_suffix(s1_temp, t1)
        sfx2 = gen_suffix(s2_temp, t2)
        max_val = 0
        for j in range(len(sfx1)):
            if j == len(sfx2):
                break
            elif sfx1[j] == sfx2[j] and max_val < len(sfx2[j]):
                max_val = len(sfx2[j])
        output.append(max_val)
    for i in range(len(output)):
        l_pairs[i].append(output[i])
    write_file(l_pairs)
            
def shorten(s, w):
    """shortens a string by starting at index s instead of starting at index 0

    Args:
        s (int): the starting index of the shortened word
        w (str): the string to be shortened

    Returns:
        str: the shortened string
    """
    temp = []
    for i in range(s, len(w)):
        temp.append(w[i])
    return "".join(temp)

def gen_suffix(s, t):
    """generates the suffixes of a given word by traversing through its suffix tree

    Args:
        s (str): word to be identified for its suffixes
        t (Ukkonens): the corresponding tree of the word

    Returns:
        List[str]: list of the word's suffixes
    """
    sfx = []
    for i in range(len(s)):
        sfx.append(traverse(0, i, t.root, s))
    return sfx

def find_edge(s, node, w):
    """during traversal when the an new edge is required for continuing the traversal find_edge 
    finds an available edge for traversal

    Args:
        s (int): the next point of traversal (next character of comparison)
        node (Node): the destination node of the previously travelled edge 
        w (str): the word that the suffix tree is constructed from

    Returns:
        Edge or None: None if no available edge is found or the next Edge if an available edge is found
    """
    r = None
    if node is None:
        return r
    for i in range(node.get_len()):
        edge = node.get_edge(i)
        # for finding normal edges
        if w[edge.start] == w[s] and edge.start > -1:
            r = edge
            break
    return r

def traverse(s, e, node, w):
    """traverses the tree for a given word indicated by the start and end index

    Args:
        s (int): start index
        e (int): end index
        node (Node): root node of suffix tree
        w (str): the word that the suffix tree is constructed from

    Returns:
        str: longest suffix found within tree specified by start index and end index
    """
    r = ""
    edge = find_edge(s, node, w)
    if edge.source is not None:
        cnt = 0
        n = edge.start
        for i in range(s, e+1):
            if cnt >= edge.end[0] + 1:
                edge = find_edge(i, edge.dest, w)
                if edge is None: 
                    return r
                else: 
                    n = edge.start
            if w[i] != w[n]:
                break
            n += 1 
            cnt += 1
            r += w[i]
    return r        

def write_file(data):
    """writes the result from lcp to the output file

    Args:
        data (List[int]): list of L pairs followed by the corresponding L values 
    """
    f = open("output_lcp.txt", "w")
    for line in data:
        for i in line:
            f.write(str(i) + " ")
        f.write("\n")

def read_file(fileN):
    """reads file and creates list representing the L pairs

    Args:
        fileN (str): name of file to be opened

    Returns:
        List[str]: list of L pairs
    """
    f = open(fileN, "r")
    r = []
    for line in f:
        r.append(line)
    return r

def process_l(l_pairs):
    """creates new List that changes L pairs into lists of only int values 

    Args:
        l_pairs (List[str]): list of L pairs

    Returns:
        List[List[int]]: List of L pairs in an operatable form
    """
    r = []
    for line in l_pairs:
        pair = line.rstrip("\n").split() 
        pair = [int(i) for i in pair]
        r.append(pair)
    return r

def main():
    """generate operatable input variables and run lcp
    """
    s1 = read_file(sys.argv[1])[0]
    s2 = read_file(sys.argv[2])[0]
    l_pairs = process_l( read_file(sys.argv[3]) )
    lcp(s1,s2,l_pairs)
    
if __name__ == "__main__":
    main()