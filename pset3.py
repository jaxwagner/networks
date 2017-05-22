#JACKSON WAGNER CS134 PSET 3 PROBLEM 5
import random
import seaborn as sns
import math
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

def makeGraphFromFile(s, delimeter="\t"):
    with open(s, "r") as ins:
        graph = {}
        for line in tqdm(ins):
            key, value = map(int,line.split(delimeter))
            if key not in graph:
                graph[key] = [value]
            else:
                graph[key].append(value)
            if value not in graph:
                graph[value] = []
        return graph

def part1(f1, f2):
    graph1 = makeGraphFromFile(f1, " ")
    graph2 = makeGraphFromFile(f2, " ")
    deg1 = map(len, graph1.values())
    deg2 = map(len, graph2.values())
    sns.distplot(deg1)
    plt.xlabel('degree')
    plt.ylabel('frequency')
    plt.show()
    sns.distplot(deg2)
    plt.xlabel('degree')
    plt.ylabel('frequency')
    plt.show()

def part2(f1, f2):
    graph1 = makeGraphFromFile(f1, " ")
    graph2 = makeGraphFromFile(f2, " ")
    part2WorkGraph(graph1)
    part2WorkGraph(graph2)

def part2WorkGraph(graph):
    deg = map(len, graph.values())
    c = map(float, np.bincount(deg))
    c /= np.sum(deg)
    logC = map(np.log, c)
    x = []
    for i in range(0, len(c)):
        x.append(np.log(i))
    plt.xlabel('log degree')
    plt.ylabel('log frequency')
    plt.scatter(x, logC)
    plt.show()

def part4(f1, f2):
    graph1 = makeGraphFromFile(f1, " ")
    graph2 = makeGraphFromFile(f2, " ")
    workPart4(graph1)
    workPart4(graph2)

def workPart4(graph):
    deg = filter(lambda x: x != 0, map(len, graph.values()))
    c = map(float, deg)
    cbins = map(float, np.bincount(deg))
    cbins /= np.sum(deg)
    logC = map(np.log, cbins)
    print logC
    xLog = []
    for i in range(0, len(cbins)):
        if i == 0:
            xLog.append(np.nan)
        else:
            xLog.append(np.log(i))
    xMin = float(min(deg))
    sumTerm = sum(map(lambda n: np.log(n/xMin), c))
    alpha = 1 + len(c)/sumTerm


    #finding the b term
    xExp = [i**(-alpha) for i in xrange(int(xMin), len(cbins))]
    probSum = np.sum(xExp)
    b = -np.log(probSum)

    plt.scatter(np.exp(xLog),np.exp(logC))
    plt.plot(np.exp(xLog), np.exp(np.multiply(-alpha, xLog) + b))
    plt.xlabel('degree')
    plt.ylabel('frequency')
    plt.show()

def part3(f1, f2):
    g1 = makeGraphFromFile(f1, " ")
    g2 = makeGraphFromFile(f2, " ")
    workPart3(g1)
    workPart3(g2)

def workPart3(graph):
    deg = map(len, graph.values())
    counts = map(float, np.bincount(deg))
    c = []
    for i in range(1, len(counts)):
        if counts[i] != 0:
            c.append(counts[i])

    c /= np.sum(c)
    logC = map(np.log, c)
    x = []

    for i in range(1, len(c)):
        x.append(np.log(i))
    A = np.vstack([x, np.ones(len(x))]).T
    del logC[0]
    m, c = np.linalg.lstsq(A, np.array(logC))[0]

    print m, c

    plt.plot(x, np.multiply(m,x) + c)
    plt.scatter(x, logC)
    plt.xlabel('log degree')
    plt.ylabel('log frequency')
    plt.show()

def part5(f1, f2):
    g1 = makeGraphFromFile(f1, " ")
    g2 = makeGraphFromFile(f2, " ")
    workPart5(g1)
    workPart5(g2)

def workPart5(graph):
    deg = map(len, graph.values())
    counts = map(float, np.bincount(deg))
    c = []
    for i in range(0, len(counts)):
        if counts[i] != 0:
            c.append(float(counts[i]))
    c = np.array(c)
    c /= float(np.sum(c))
    logC = map(np.log, c)
    x = []
    x.append(-1)
    for i in range(1, len(c)):
        x.append(np.log(i))
    A = np.vstack([x, np.ones(len(x))]).T

    m, b = np.linalg.lstsq(A, np.array(logC))[0]

    #f = cx^-alpha
    alphaPartC = m
    cPartC = np.exp(b)

    print alphaPartC

    alphaPartD, cPartD = getOtherAlpha(graph)

    print alphaPartC, cPartC
    print alphaPartD, cPartD

    xList = range(1, len(c)+1)
    yList1 = map(lambda x: cPartC*x**(alphaPartC), xList)
    yList2 = map(lambda x: cPartD*x**(-alphaPartD), xList)
    plt.scatter(xList, c)
    plt.plot(xList, yList1, label="OLS")
    plt.plot(xList, yList2, label="MLE")
    plt.legend()
    plt.xlabel('degree')
    plt.ylabel('frequency')
    plt.show()

def getOtherAlpha(graph):
    deg = filter(lambda x: x != 0, map(len, graph.values()))
    c = map(float, deg)
    xMin = float(min(deg))
    sumTerm = sum(map(lambda n: np.log(n/xMin), c))

    alpha = 1 + len(c)/sumTerm

    xExp = [i**(-alpha) for i in xrange(int(xMin), len(c))]
    probSum = np.sum(xExp)
    b = 1/probSum

    return alpha, b

def main():
    f1 = "network1.txt"
    f2 = "network2.txt"

    #part1(f1, f2)
    #part2(f1, f2)
    #part3(f1, f2)
    #part4(f1, f2)
    part5(f1, f2)

if __name__ == '__main__':
    main()
