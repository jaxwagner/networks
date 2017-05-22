#JACKSON WAGNER CS134 PSET 4 PROBLEM 3
import random
import math
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

def isDirected(file):
    return file.find("ungraph") == -1

def makeGraphFromFile(file, directed):
    with open(file, "r") as ins:
        graph = {}
        for line in tqdm(ins):
            if not line.startswith("#"):
                key, value = map(int,line.split("\t"))
                if key not in graph:
                    graph[key] = [value]
                else:
                    graph[key].append(value)
                if value not in graph:
                    graph[value] = []
                if not directed:
                    graph[value].append(key)
        return graph

def sumDegreesOfNeighbors(graph, neighbors):
    if len(neighbors) == 0:
        return 0
    return float(sum(map(lambda x: len(graph[x]), neighbors)))/float(len(neighbors))

def friendshipParadox(file):
    directed = isDirected(file)
    graph = {}
    graph = makeGraphFromFile(file, directed)

    num = float(sum(map(len, graph.values())))

    denom = float(sum(map(lambda x: sumDegreesOfNeighbors(graph, x), graph.values())))

    return num/denom

def main():
    f1 = "com-youtube.ungraph.txt"
    f2 = "email-Enron.txt"
    f3 = "com-lj.ungraph.txt"
    f4 = "com-dblp.ungraph.txt"
    f5 = "soc-Epinions1.txt"
    f6 = "soc-Slashdot0811.txt"
    f7 = "wiki-Talk.txt"
    f8 = "com-orkut.ungraph.txt"

    print friendshipParadox(f1)
    # print friendshipParadox(f2)
    # print friendshipParadox(f3)
    # print friendshipParadox(f4)
    # print friendshipParadox(f5)
    # print friendshipParadox(f6)
    # print friendshipParadox(f7)
    # print friendshipParadox(f8)

if __name__ == '__main__':
    main()
