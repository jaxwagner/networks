#JACKSON WAGNER CS134 PSET 8 PROBLEM 5
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import pickle as pk
from tqdm import tqdm
from collections import defaultdict
from collections import deque
from scipy.optimize import linprog

def loadPk(pkFile):
    opinions = pk.load( open( pkFile, "rb" ) )
    return opinions

def partA(opinionsArray):
    print "T = ", len(opinionsArray[0][0])
    print "num diffusion processes = ", len(opinionsArray)

def makeGraphFromFile(s, delimeter=" "):
    with open(s, "r") as ins:
        graph = {}
        for line in tqdm(ins):
            key, value = map(int,line.split(delimeter))
            if key not in graph:
                graph[key] = [key, value]
            else:
                graph[key].append(value)
            if value not in graph:
                graph[value] = [value]
        return graph

def partB(graph):
    numNodes = len(graph)
    print "num nodes = ", numNodes
    count = 0
    for key in graph:
        count += len(graph[key])
    print "Ave out-degree = ", float(count)/float(numNodes)
    return numNodes

def partD(graph, opinionsArray, m):
    weightedGraph = defaultdict(lambda: defaultdict(dict))

    #test
    # print weightsFromU(graph, opinionsArray, 0, len(graph))

    for u in graph:
        weightsFromUVar = weightsFromU(graph, opinionsArray, u, len(graph))
        #print weightsFromUVar
        for i, v in enumerate(graph[u]):
            weightedGraph[u][v] = weightsFromUVar[i]
    #print "weight 2-16 = ", weightedGraph[2][16]
    #print "weight 29-22 = ", weightedGraph[29][22]
    filename = "weightedGraph"
    saveToCSV(filename, weightedGraph)
    return weightedGraph

def saveToCSV(filename, weightedGraph):
    with open(filename, "w") as outfile:

        for i in weightedGraph:
            for j in weightedGraph[i]:
                outfile.write("{},{},{}\n".format(i,j,weightedGraph[i][j]))

def partE(weightedGraph):
    nodeToSums = {}
    for u in weightedGraph:
        count = 0
        for v in weightedGraph[u]:
            count += weightedGraph[u][v]
        nodeToSums[u] = count

    topFive = np.zeros(5)
    for i in range(5):
        largest = 0
        for j in nodeToSums:
            if nodeToSums[j] > largest and j not in topFive:
                topFive[i] = j
                largest = nodeToSums[j]
    return topFive




def weightsFromU(graph, opinionsArray, u, m):
    #optimize the set of constraints
    numV = len(graph[u])
    c = -1 * np.ones(numV)

    b_ub = []
    A_ub = []
    for i in range(len(opinionsArray)):
        for t in range(1, m):
            coefficients = np.zeros(numV)
            for j, v in enumerate(graph[u]):
                if opinionsArray[i][v][t-1] == 1:
                    coefficients[j] = 1
            uOpinion = opinionsArray[i][u][t]
            b = .5
            if uOpinion == 1:
                coefficients = -1 * coefficients
                b *= -1
            A_ub.append(coefficients)
            b_ub.append(b)

    # print np.array(A_ub)
    # print b_ub
    A_eq = [[1] * numV]
    res = linprog(c, A_ub, b_ub, A_eq, b_eq=[1], bounds=(0,1), options={'disp':True})

    return res.x

def main():
    opinionsFile = "pset8_opinions.pkl"
    networkFile = "pset8_network1.txt"
    opinionsArray = loadPk(opinionsFile)
    graph = makeGraphFromFile(networkFile)
    #partA(opinionsArray)
    #partB(graph)
    weightedGraph = partD(graph, opinionsArray, partB(graph))
    print partE(weightedGraph)












if __name__ == '__main__':
    main()
