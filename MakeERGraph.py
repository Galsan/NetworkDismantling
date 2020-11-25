import networkx as nx


def main():
    G = nx.erdos_renyi_graph(78125, p=0.0000448, directed=False, seed=None)

    f = open("TextFiles/ER.txt", 'a')
    f.write(str(G.number_of_nodes()) + '\n')

    i = 0
    for node in G.nodes():
        line = str(i) + ': '

        edges = [q for v, q in G.edges(node)]

        for edge in edges:
            line += str(edge) + " "

        f.write(line + "\n")
        i += 1

    f.close()
    print(nx.info(G))


if __name__ == '__main__':
    main()
