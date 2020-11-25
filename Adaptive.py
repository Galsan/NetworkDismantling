from random import randrange

import networkit as nk
import sys
import matplotlib.pyplot as plt
import math

END = 20
BEGIN = 0
dat_dc = []
dat_bc = []
dat_ev = []
dat_cc = []
dat_random = []
per = [i for i in range(BEGIN, END + 1)]


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


def zipLargestComponentNodeWithValue(data, largestCompNodes):
    # Хамгийн том компонентийн оноонуудаар лист үүсгээд оройн индексийг zip хийнэ
    largestComp = []
    for i in largestCompNodes:
        largestComp.append(data[i])
    largestComp = zip(largestCompNodes, largestComp)
    return largestComp


def top_nodes(data, one_per):
    # Хамгийн их оноотой оройнуудыг буцаана
    return sorted(data, key=lambda x: x[1], reverse=True)[:one_per]


def adapt_dc(G, one_per, n):
    largest = nk.components.ConnectedComponents.extractLargestConnectedComponent(G)
    dc = nk.centrality.DegreeCentrality(largest)
    dc.run()
    largest_data = zipLargestComponentNodeWithValue(dc.scores(), largest.nodes())
    remove_nodes = top_nodes(largest_data, one_per)
    for i in [q for q, j in remove_nodes]:
        G.removeNode(i)
    dat_dc.append(nk.components.ConnectedComponents.extractLargestConnectedComponent(G).numberOfNodes() / n)


def adapt_bc(G, one_per, n):
    largest = nk.components.ConnectedComponents.extractLargestConnectedComponent(G)
    bc = nk.centrality.EstimateBetweenness(largest, math.log2(n))
    bc.run()
    largest_data = zipLargestComponentNodeWithValue(bc.scores(), largest.nodes())
    remove_nodes = top_nodes(largest_data, one_per)
    for i in [q for q, j in remove_nodes]:
        G.removeNode(i)
    dat_bc.append(nk.components.ConnectedComponents.extractLargestConnectedComponent(G).numberOfNodes() / n)


def adapt_cc(G, one_per, n):
    largest = nk.components.ConnectedComponents.extractLargestConnectedComponent(G)
    cc = nk.centrality.ApproxCloseness(largest, math.log2(n))
    cc.run()
    largest_data = zipLargestComponentNodeWithValue(cc.scores(), largest.nodes())
    remove_nodes = top_nodes(largest_data, one_per)

    for i in [q for q, j in remove_nodes]:
        G.removeNode(i)
    # cc = nk.centrality.TopCloseness(largest, one_per)
    # cc.run()
    # for i in cc.topkNodesList():
    #     G.removeNode(i)
    dat_cc.append(nk.components.ConnectedComponents.extractLargestConnectedComponent(G).numberOfNodes() / n)


def adapt_ev(G, one_per, n):
    largest = nk.components.ConnectedComponents.extractLargestConnectedComponent(G)
    ev = nk.centrality.EigenvectorCentrality(largest)
    ev.run()
    largest_data = zipLargestComponentNodeWithValue(ev.scores(), largest.nodes())
    remove_nodes = top_nodes(largest_data, one_per)
    for i in [q for q, j in remove_nodes]:
        G.removeNode(i)
    dat_ev.append(nk.components.ConnectedComponents.extractLargestConnectedComponent(G).numberOfNodes() / n)


def adapt_random(G, one_per, n):
    ctr = 0
    while True:
        key = randrange(0, n)
        if G.hasNode(key):
            G.removeNode(key)
            ctr += 1
        if ctr == one_per:
            break
    dat_random.append(nk.components.ConnectedComponents.extractLargestConnectedComponent(G).numberOfNodes() / n)


def largestComp(fileLoc):
    file = open(fileLoc)
    G, n = read_graph(file)
    G_bc = G.__copy__()
    G_cc = G.__copy__()
    G_ev = G.__copy__()
    G_random = G.__copy__()

    # Эхлэх үеийн хамгийн том компонент
    largestComponent = nk.components.ConnectedComponents.extractLargestConnectedComponent(G).numberOfNodes()

    dat_dc.append(largestComponent / n)
    dat_bc.append(largestComponent / n)
    dat_cc.append(largestComponent / n)
    dat_ev.append(largestComponent / n)
    dat_random.append(largestComponent / n)

    one_per = math.ceil(n / 100)
    for i in range(BEGIN, END):
        adapt_dc(G, one_per, n)
        adapt_bc(G_bc, one_per, n)
        adapt_cc(G_cc, one_per, n)
        adapt_ev(G_ev, one_per, n)
        adapt_random(G_random, one_per, n)


def main():
    nk.setNumberOfThreads(4)
    name = 'Yeast1'
    largestComp('TextFiles/' + str(name) + '.txt')
    plt.grid(True)
    plt.plot(per, dat_dc[BEGIN:], label='Degree centrality', color='#000000', linestyle='solid')
    plt.plot(per, dat_bc[BEGIN:], label='Betweenness centrality', color='#000000', linestyle='dashed')
    plt.plot(per, dat_cc[BEGIN:], label='Closeness centrality', color='#8a8686', linestyle='solid')
    plt.plot(per, dat_ev[BEGIN:], label='EigenVector centrality', color='#8a8686', linestyle='dashed')
    plt.plot(per, dat_random[BEGIN:], label='Random', color='#d9d4d4', linestyle='solid')

    plt.title('Харьцуулалт (' + str(name) + ')')
    plt.xlabel('Устгасан оройн тоо (Хувиар)')
    plt.ylabel('Хамгийн том компонентийн хэмжээ')
    plt.legend()
    plt.savefig('figure/' + str(name) + '.png')
    plt.show()


if __name__ == '__main__':
    sys.setrecursionlimit(int(1e9))
    main()
