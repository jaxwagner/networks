#JACKSON WAGNER CS134 PSET 10 PROBLEM 4
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import pickle as pk
from tqdm import tqdm
from collections import defaultdict
from collections import deque
from scipy.optimize import linprog
import seaborn as sns
import copy

def makeGraphFromFile(s, delimeter="\t"):
    with open(s, "r") as ins:
        graph = {}
        for line in tqdm(ins):
            key, value = map(int,line.split(delimeter))
            if key not in graph:
                graph[key] = {value}
            else:
                graph[key].add(value)
            if value not in graph:
                graph[value] = {key}
            else:
                graph[value].add(key)
        return graph

def partA(file):
    graph = makeGraphFromFile(file)
    print "num nodes = ", len(graph)
    numEdges = 0
    for u in graph:
        numEdges += len(graph[u])
    print "num edges = ", float(numEdges)/float(2.0)

def getDistances(graph):
    distances = defaultdict(lambda: defaultdict(int))
    #breadth first search
    for u in graph:
        queue = [(u, 0)]
        seen = set([u])
        while len(queue) > 0:
            (vertex, steps) = queue.pop(0)

            distances[u][vertex] = steps

            for next in graph[vertex]:
                if next not in seen:
                    seen.add(next)
                    queue.append((next,steps + 1))
    return distances



def min_pairwise(graph):
    distances = getDistances(graph)
    count = 0
    denom = 0
    for u in distances:
        for v in distances[u]:
            denom += 1
            count += distances[u][v]
    print "min d ave = ", float(count)/float(denom)

def dist(p, m, c, norm):
    if norm == "min":
        minD = None
        for v in m[p]:
            if minD == None or (v in c and m[p][v] < minD):
                minD = m[p][v]
        return minD
    if norm == "max":
        maxD = 0
        for v in m[p]:
            if v in c and m[p][v] > maxD:
                maxD = m[p][v]
        return maxD
    if norm == "mean":
         count = 0
         for v in m[p]:
             if v in c:
                 count += m[p][v]
    return float(count)/float(len(c))

def partC(graph):
    m = getDistances(graph)
    print "mean = ", dist(5, m, {2,8,20}, "mean")
    print "min = ", dist(5, m, {2,8,20}, "min")
    print "max = ", dist(5, m, {2,8,20}, "max")

def assign(p, m, c_list, norm):
    closest = None
    closestIndex = None
    for i,c in enumerate(c_list):
        d = dist(p,m,c,norm)
        if closest == None or d < closest:
            closest = d
            closestIndex = i
    return closestIndex

def partD(graph):
    m = getDistances(graph)
    print "mean closest Index = ", assign(5, m, [{2, 8, 20}, {3, 4, 8, 26}], "mean")
    print "min closest Index = ", assign(5, m, [{2, 8, 20}, {3, 4, 8, 26}], "min")
    print "max closest Index = ", assign(5, m, [{2, 8, 20}, {3, 4, 8, 26}], "max")

def center(m,c):
    minNode = None
    minTotal = None
    for i in c:
        total = 0
        for j in c:
            total += m[i][j]
        if minTotal == None or total < minTotal:
            minTotal = total
            minNode = i
    return minNode

def partE(graph):
    m = getDistances(graph)
    print "c = ", center(m, {2, 3, 4, 8, 20, 26})

def cluster(m, k, norm, i):
    nodes = m.keys()
    centroids = random.sample(nodes, k)
    c_list = [{c} for c in centroids]
    for j in range(i):
        c_list_new = [{c} for c in centroids]
        newCentroids = []
        random.shuffle(nodes)
        for u in nodes:
            if u not in centroids:
                index = assign(u, m, c_list, norm)
                c_list_new[index].add(u)
        c_list = c_list_new
        for n in range(len(centroids)):
            newCentroids.append(center(m, c_list[n]))
        if centroids == newCentroids:
            break
        centroids = newCentroids
        #print centroids
    return (centroids, c_list)

def objective(clusters, centers, norm, m):
    total = 0
    for i,u in enumerate(clusters):
        center = centers[i]
        for x in u:
            total += (m[center][x])**2
    return total


def partG(graph):
    k_list = [3, 5, 10, 20]
    norm_list = ["min", "max", "mean"]
    m = getDistances(graph)
    for k in k_list:
        for norm in norm_list:
            centNclusts = cluster(m, k, norm, 20)
            center = centNclusts[0]
            clusters = centNclusts[1]
            objFunction = objective(clusters, center, norm, m)
            print " "
            print norm
            print "k = ", k
            print "CENTER = ", center
            print "OBJECTIVE FUNCTION = ", objFunction
            print "SIZE OF CLUSTERS:"
            for i in range(len(clusters)):
                print len(clusters[i])


def main():
    file = "data.txt"
    graph = makeGraphFromFile(file)
    #partA(file)
    #min_pairwise(graph)
    #partC(graph)
    #partD(graph)
    #partE(graph)
    #partF --> see cluster function
    n = 3
    for x in range(n):
        print "TRIAL ", x
        partG(graph)
        print " "
        print " "



if __name__ == '__main__':
    main()
