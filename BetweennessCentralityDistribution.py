import math
import networkit as nk
import matplotlib.pyplot as plt
import GraphTool as gt


def saveFig(name):
    file = open('TextFiles/' + str(name) + '.txt')
    G, n = gt.read_graph(file)

    bc = nk.centrality.EstimateBetweenness(G, math.log2(n))
    bc.run()
    bc_data = bc.scores()

    mx = max(bc_data)
    mn = min(bc_data)

    # Бүх оноог арван тэнцүү завсарт хувааж байна
    rng = (mx - mn) / 10.0
    bins = [float(i) / 1000.0 for i in
            range(math.floor(mn * 1000), math.ceil(mx * 1000) + math.ceil(rng * 1000), math.ceil(rng * 1000))]

    # Оноог тоолох зорилготой хувьсагч
    counter = []
    for i in range(0, len(bins)):
        counter.append(0)

    for data in bc_data:
        for i in range(0, len(bins) - 1):
            if bins[i + 1] > data >= bins[i]:
                counter[i] += 1

    for i in range(0, len(counter)):
        if counter[i] == 0:
            counter[i] += 1

    print(bins)

    # Хамгийн их тооны орон тоолох зориулалттай хувьсагч
    digitCtr = 0
    while mx != 0:
        digitCtr += 1
        mx = int(mx / 10)

    # x тэнхлэгийг 4н оронтой болгож багасгах зорилготой
    digitCtr -= 4

    plt.figure(figsize=[8, 5])
    plt.title('Betweenness centrality(' + name + ')')
    plt.ylabel('Нягтын функц')
    plt.xlabel('Betweenness оноо * 10^-' + str(digitCtr))
    plt.grid(True)
    plt.yscale('logit')
    # 1-р хувьсагч: плот нь х тэнхлэгтээ бүхэл тоон утга авдаг учир 10ын 3н зэрэгтээр үржлээ
    # 2-р хувьсагч: нь тоолсон оройн тоог бүх оройн тоонд хувааж нягтыг гаргаж байна
    plt.plot([math.ceil(i / math.pow(10, digitCtr)) for i in bins], [float(i / n) for i in counter], "-ko")
    plt.savefig('BetweennessCentralityDistributionFigure/' + name + ".png")
    plt.show()


if __name__ == '__main__':
    saveFig('Yeast1')
