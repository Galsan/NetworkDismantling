from random import randrange

import networkit as nk
import sys
import matplotlib.pyplot as plt
import math
import GraphTool as gt

# Adaptive бишээр 10, 15, 20, 25 хувийг устгасны дараах үр дүн
END = 70
BEGIN = 0
dat_dc = []
dat_bc = []
dat_ev = []
dat_cc = []
dat_random = []
percents = [i for i in range(BEGIN, END + 1, 5)]


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


def not_adapt_dc(G, per, n):
    largest = nk.components.ConnectedComponents.extractLargestConnectedComponent(G)
    dc = nk.centrality.DegreeCentrality(largest)
    dc.run()
    largest_data = zipLargestComponentNodeWithValue(dc.scores(), largest.nodes())
    remove_nodes = top_nodes(largest_data, per)
    for i in [q for q, j in remove_nodes]:
        G.removeNode(i)
    dat_dc.append(nk.components.ConnectedComponents.extractLargestConnectedComponent(G).numberOfNodes() / n)


def not_adapt_bc(G, per, n):
    largest = nk.components.ConnectedComponents.extractLargestConnectedComponent(G)
    bc = nk.centrality.EstimateBetweenness(largest, math.log2(n)*10)
    bc.run()
    largest_data = zipLargestComponentNodeWithValue(bc.scores(), largest.nodes())
    remove_nodes = top_nodes(largest_data, per)
    for i in [q for q, j in remove_nodes]:
        G.removeNode(i)
    dat_bc.append(nk.components.ConnectedComponents.extractLargestConnectedComponent(G).numberOfNodes() / n)


def not_adapt_cc(G, per, n):
    largest = nk.components.ConnectedComponents.extractLargestConnectedComponent(G)
    cc = nk.centrality.ApproxCloseness(largest, math.log2(n)*10)
    cc.run()
    largest_data = zipLargestComponentNodeWithValue(cc.scores(), largest.nodes())
    remove_nodes = top_nodes(largest_data, per)

    for i in [q for q, j in remove_nodes]:
        G.removeNode(i)
    # cc = nk.centrality.TopCloseness(largest, per)
    # cc.run()
    # for i in cc.topkNodesList():
    #     G.removeNode(i)
    dat_cc.append(nk.components.ConnectedComponents.extractLargestConnectedComponent(G).numberOfNodes() / n)


def not_adapt_ev(G, per, n):
    largest = nk.components.ConnectedComponents.extractLargestConnectedComponent(G)
    ev = nk.centrality.EigenvectorCentrality(largest)
    ev.run()
    largest_data = zipLargestComponentNodeWithValue(ev.scores(), largest.nodes())
    remove_nodes = top_nodes(largest_data, per)
    for i in [q for q, j in remove_nodes]:
        G.removeNode(i)
    dat_ev.append(nk.components.ConnectedComponents.extractLargestConnectedComponent(G).numberOfNodes() / n)


def not_adapt_random(G, per, n):
    ctr = 0
    while True:
        key = randrange(0, n)
        if G.hasNode(key):
            G.removeNode(key)
            ctr += 1
        if ctr == per:
            break
    dat_random.append(nk.components.ConnectedComponents.extractLargestConnectedComponent(G).numberOfNodes() / n)


def largestComp(fileLoc):
    file = open(fileLoc)
    G, n = gt.read_graph(file)

    # Эхлэх үеийн хамгийн том компонент
    largestComponent = nk.components.ConnectedComponents.extractLargestConnectedComponent(G).numberOfNodes()

    dat_dc.append(largestComponent / n)
    dat_bc.append(largestComponent / n)
    dat_cc.append(largestComponent / n)
    dat_ev.append(largestComponent / n)
    dat_random.append(largestComponent / n)

    for i in percents[1:]:
        not_adapt_dc(G.__copy__(), math.ceil(n / 100 * i), n)
        not_adapt_bc(G.__copy__(), math.ceil(n / 100 * i), n)
        not_adapt_cc(G.__copy__(), math.ceil(n / 100 * i), n)
        not_adapt_ev(G.__copy__(), math.ceil(n / 100 * i), n)
        not_adapt_random(G.__copy__(), math.ceil(n / 100 * i), n)


def main():
    nk.setNumberOfThreads(4)
    name = 'Yeast1'
    largestComp('TextFiles/' + str(name) + '.txt')
    plt.grid(True)
    plt.plot(percents, dat_dc, label='Degree centrality', color='#000000', linestyle='solid')
    plt.plot(percents, dat_bc, label='Betweenness centrality', color='#000000', linestyle='dashed')
    plt.plot(percents, dat_cc, label='Closeness centrality', color='#8a8686', linestyle='solid')
    plt.plot(percents, dat_ev, label='EigenVector centrality', color='#8a8686', linestyle='dashed')
    plt.plot(percents, dat_random, label='Random', color='#d9d4d4', linestyle='solid')

    plt.title('Харьцуулалт (' + str(name) + ')')
    plt.xlabel('Устгасан оройн тоо (Хувиар)')
    plt.ylabel('Хамгийн том компонентийн хэмжээ')
    plt.legend()
    plt.savefig('NotAdaptiveDismantlingFigure/' + str(name) + '.png')
    plt.show()


if __name__ == '__main__':
    sys.setrecursionlimit(int(1e9))

    main()
