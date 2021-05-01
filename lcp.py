from Ukkonens import ukkonens

def lcp(s1, s2, l_pairs):
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
        #print("sfx1: ", sfx1)
        #print("sfx2: ", sfx2)
        for j in range(len(sfx1)):
            if j < len(sfx2):
                if sfx1[j] == sfx2[j]:
                    if max_val < len(sfx2[j]):
                        max_val = len(sfx2[j])
        output.append(max_val)
    return output
            
def shorten(s, w):
    temp = []
    for i in range(s, len(w)):
        temp.append(w[i])
    return "".join(temp)

def gen_suffix(s, t):
    sfx = []
    for i in range(len(s)):
        sfx.append(traverse(0, i, t.root, s))
    return sfx

def find_edge(s, node, w):
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
        

def main():
    s1 = "abcdacbdab"
    s2 = "dacbdabc"
    L = [(3, 0), (4, 2), (0, 5)]
    print(lcp(s1, s2, L))

if __name__ == "__main__":
    main()