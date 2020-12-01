import math

import networkit as nk
from matplotlib import pyplot as plt
import GraphTool as gt


def saveFig(name):
    file = open('TextFiles/' + str(name) + '.txt')
    G, n = gt.read_graph(file)

    dc = nk.centrality.DegreeCentrality(G, normalized=True)
    dc.run()
    degree_val = dc.scores()

    mx = max(degree_val)
    mn = min(degree_val)
    print(mx)

    uld = mx
    ctr = 0
    while uld / 100 < 1:
        uld *= 10
        ctr += 1

    rng = (mx - mn) / 10.0
    bins = [float(i) / float(math.pow(10, ctr)) for i in
            range(math.floor(mn * math.pow(10, ctr)),
                  math.ceil(mx * math.pow(10, ctr)) + math.ceil(rng * math.pow(10, ctr)),
                  math.ceil(rng * math.pow(10, ctr)))]

    counter = []
    for i in range(0, len(bins)):
        counter.append(0)

    # Бүх оноог арван тэнцүү завсарт хувааж байна
    rng = (mx - mn) / 10.0

    for data in degree_val:
        for i in range(0, len(bins) - 1):
            if bins[i + 1] > data >= bins[i]:
                counter[i] += 1

    for i in range(0, len(counter)):
        if counter[i] == 0:
            counter[i] += 1

    print(bins)
    print(counter)
    plt.figure(figsize=[8, 5])
    plt.title('Closeness centrality(' + name + ')')
    plt.ylabel('Нягтын функц')
    plt.xlabel('Зэргийн оноо * 10^' + str(ctr))
    plt.yscale('logit')
    plt.plot([int(i * math.pow(10, ctr)) for i in bins], [float(i / n) for i in counter], "-ko")
    plt.savefig('DegreeDistributionFraction/' + str(name) + '.png')
    plt.show()


if __name__ == '__main__':
    saveFig('Yeast1')
