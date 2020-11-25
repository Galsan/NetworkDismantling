import networkit as nk
import sys
import matplotlib.pyplot as plt
import math
import GraphTool as gt


def plot(ax, x, y, title):
    ax.set_title(title)
    ax.plot(x, y)


def addLargeComp(fileLoc):
    file = open(fileLoc)
    G, n = read_graph(file)
    cc = nk.components.ConnectedComponents(G)
    cc.run()
    # print(cc.getComponentSizes())

    bc = nk.centrality.EstimateBetweenness(G, math.log2(n))
    bc.run()
    bc_data = bc.scores()
    C = math.ceil(n / 10)

    # bc_procent10 = procent(G.__copy__(), remove_nodes(bc_data, 10, n), bc_data, n, C)
    # bc_procent15 = procent(G.__copy__(), remove_nodes(bc_data, 15, n), bc_data, n, C)
    # bc_procent20 = procent(G.__copy__(), remove_nodes(bc_data, 20, n), bc_data, n, C)
    # bc_procent25 = procent(G.__copy__(), remove_nodes(bc_data, 25, n), bc_data, n, C)

    dc = nk.centrality.DegreeCentrality(G)
    dc.run()
    dc_data = dc.scores()

    dc_procent_10 = procent(G.__copy__(), top_nodes(dc_data, 10, n), dc_data, n, C)
    dc_procent_15 = procent(G.__copy__(), top_nodes(dc_data, 15, n), dc_data, n, C)
    dc_procent_20 = procent(G.__copy__(), top_nodes(dc_data, 20, n), dc_data, n, C)
    dc_procent_25 = procent(G.__copy__(), top_nodes(dc_data, 25, n), dc_data, n, C)

    print(dc_procent_10)
    print(dc_procent_15)
    print(dc_procent_20)
    print(dc_procent_25)


def procent(G, scores, data, n, C):
    del_index = []
    for i in scores:
        index = data.index(i)
        G.removeNode(index)
        del_index.append(index)

    cc = nk.components.ConnectedComponents(G)
    cc.run()

    comp_sizes = [len(i) for i in cc.getComponents()]

    sum = 0
    for i in comp_sizes:
        if i > C:
            sum += i
    return sum / n


def largestComp(fileLoc):
    file = open(fileLoc)
    G, n = gt.read_graph(file)

    bc = nk.centrality.DegreeCentrality(G)
    bc.run()
    bc_data = bc.scores()

    remove_nodes = top_nodes(bc_data, 40, n)

    for i in remove_nodes:
        G.removeNode(bc_data.index(i))

    cc = nk.components.ConnectedComponents(G)
    cc.run()
    comps = cc.getComponentSizes()

    print(comps)
    print(max(comps))

    print(nk.components.ConnectedComponents.extractLargestConnectedComponent(G).numberOfNodes() / n)


def top_nodes(data, pro, n):
    length = math.ceil(n / 100) * pro  # % нөд устгана
    scores = sorted(data, reverse=True)[:length]
    return scores


def main():
    nk.setNumberOfThreads(4)
    largestComp('TextFiles/ER.txt')


if __name__ == '__main__':
    sys.setrecursionlimit(int(1e9))

    main()
