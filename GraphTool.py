import networkit as nk


def read_graph(fin):
    n = int(fin.readline())
    G = nk.Graph(n)
    while True:
        try:
            line = fin.readline()
        except:
            break
        line = line.split()
        if len(line) == 0:
            break
        x = int(line[0][:-1])
        arr = [int(y) for y in line[1:]]
        for y in arr:
            if not G.hasEdge(x, y):
                G.addEdge(x, y, addMissing=True)
    return G, n
