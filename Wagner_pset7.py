#JACKSON WAGNER CS134 PSET 7 PROBLEM 4
import random
import math
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from collections import defaultdict
from collections import deque

# def loadNetwork(file):
#     npArray = np.loadText(file, delimiter = "\t")

def makeGraphFromFile(file):
    with open(file, "r") as ins:
        graph = defaultdict(lambda: defaultdict(dict))
        for line in tqdm(ins):
            if not line.startswith("#"):
                key, value, prob = map(float,line.split("\t"))
                graph[key][value]= prob
        return graph

def partA(g):
    return g[42][75]

def genRandGraph(weights):
    E = defaultdict(list)
    for i in weights:
        for j in weights[i]:
            r  = random.random()
            if r < weights[i][j]:
                E[i].append(j)
                if j not in E:
                    E[j] = []
    return E


def getReachable(graph, S):
    numReachable = 0
    queue = deque(S)
    seen = set()
    while len(queue) > 0:
        vertex = queue.popleft()

        numReachable += 1

        for next in graph[vertex]:
            if next not in seen:
                seen.add(next)
                queue.append(next)
    return numReachable

def sampleInfluence(G, S, m):
    count = 0
    for i in range(m):
        realizedEdges = genRandGraph(G)
        ri = getReachable(realizedEdges, S)
        count += ri
    fs = float(count)/float(m)
    return fs

def partB(g):
    nodeCount = 0.00
    for i in range(100):
        E = genRandGraph(g)
        nodeCount += len(E)
    return nodeCount/100

def getNodeWithMaxInfluence(g, S):
    maxInfluence = 0
    maxNode = None
    for i in g:
        influence = sampleInfluence(g, S.union({i}), 15)
        if maxInfluence < influence:
            maxNode = i
            maxInfluence = influence
    return (maxNode, maxInfluence)


def partD(g, k):
    S = set()
    score = 0
    while len(S) < k:
        a = getNodeWithMaxInfluence(g, S)
        node = a[0]
        inf = a[1] - score
        score = a[1]
        print "fs(a) = ", inf
        S.add(node)
    print "Score = ", score
    return S

def main():
    file = "network.txt"
    g = makeGraphFromFile(file)
    S = [17,23,42,2017]
    m = 500
    #print partA(g)
    #print partB(g)

    # part c below
    #print sampleInfluence(g, S, m)

    print partD(g, 5)




if __name__ == '__main__':
    main()
