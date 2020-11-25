import math
import networkit as nk
import matplotlib.pyplot as plt
import GraphTool as gt


def saveFig(name):
    file = open('TextFiles/' + str(name) + '.txt')
    G, n = gt.read_graph(file)

    ev = nk.centrality.EigenvectorCentrality(G)
    ev.run()
    ev_data = ev.scores()

    mx = max(ev_data)
    mn = min(ev_data)

    # Бүх оноог арван тэнцүү завсарт хувааж байна
    rng = (mx - mn) / 10.0
    bins = [float(i) / 1000.0 for i in
            range(math.floor(mn * 1000), math.ceil(mx * 1000) + math.ceil(rng * 1000), math.ceil(rng * 1000))]

    # Оноог тоолох зорилготой хувьсагч
    counter = []
    for i in range(0, len(bins)):
        counter.append(0)

    for data in ev_data:
        for i in range(0, len(bins) - 1):
            if bins[i + 1] > data >= bins[i]:
                counter[i] += 1

    # Аль нэг завсарын тоо 0тэй тэнцүү байхад графикийг зурвал тасарсан гарах учир
    # 0 тэй тэнцүү байгаа завсрын оройн тоог 1ээр нэмж байна
    for i in range(0, len(counter)):
        if counter[i] == 0:
            counter[i] += 1

    plt.figure(figsize=[8, 5])
    plt.title('Eigenvector centrality(' + name + ')')
    plt.ylabel('Нягтын функц')
    plt.xlabel('EigenVector оноо * 10^3')
    plt.grid(True)
    plt.yscale('logit')
    # 1-р хувьсагч: плот нь х тэнхлэгтээ бүхэл тоон утга авдаг учир 10ын 3н зэрэгтээр үржлээ
    # 2-р хувьсагч: нь тоолсон оройн тоог бүх оройн тоонд хувааж нягтыг гаргаж байна
    plt.plot([int(i * 1000) for i in bins], [float(i / n) for i in counter], "-ko")
    plt.savefig('EigenvectorCentralityDistributionFigure/' + name + ".png")
    plt.show()


if __name__ == '__main__':
    saveFig('Yeast1')
