import networkit as nk
from matplotlib import pyplot as plt
import GraphTool as gt


def saveFig(name):
    file = open('TextFiles/' + str(name) + '.txt')
    G, n = gt.read_graph(file)

    dc = nk.centrality.DegreeCentrality(G)
    dc.run()
    degree_val = dc.scores()

    unique = sorted(set(degree_val))
    unique_count = [degree_val.count(x) for x in unique]
    degree_cen = [float(i) / (G.numberOfNodes()) for i in unique_count]

    if max(unique) > 100:
        plt.figure(figsize=[15, 8])
        plt.xscale('log')
        plt.xlabel('Зэрэг (log scale)')
    else:
        plt.figure(figsize=[8, 5])
        plt.xlabel('Зэрэг')

    plt.title(name)
    plt.ylabel('Нягтын функц')
    plt.yscale('logit')
    plt.plot(unique, degree_cen, '-ko')
    plt.savefig('DegreeDistributionFigure/' + str(name) + '.png')
    plt.show()


if __name__ == '__main__':
    saveFig('EU_flights')
