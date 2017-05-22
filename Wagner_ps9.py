#JACKSON WAGNER CS134 PSET 9 PROBLEM 5
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

def makeGraphFromFile(s, delimeter=" "):
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

def makeGraphFromFileWithString(s, delimeter=" "):
    with open(s, "r") as ins:
        graph = {}
        for line in tqdm(ins):
            parts = line.split(delimeter)
            key = int(parts[0])
            value = str(parts[1])
            if key not in graph:
                graph[key] = value
            #else:
                # graph[key].append(value)
            if value not in graph:
                graph[value] = []
        return graph

def partB(file):
    links = makeGraphFromFile(file)
    print "num nodes = ", len(links)

    totalDeg = 0
    for u in links:
        totalDeg += len(links[u])
    aveOut = float(totalDeg)/float(len(links))
    print "ave out-degree = ", aveOut
    return links

def pageRankerIter(g,d):
    dnew = defaultdict(float)
    for u, adj in g.items():
        if len(adj) != 0:
            if u not in dnew:
                dnew[u] = 0.0
            shareNum = float(d[u])/float(len(adj))
            for i in adj:
                dnew[i] += shareNum
        else:
            dnew[u] += d[u]
    return dnew

def basicPR(g,d,k):
    dnew = d
    for i in tqdm(range(k)):
        dnew = pageRankerIter(g, dnew)
    return dnew



def scaledPR(g,d,k,s):
    print "in scaledPR"
    dnew = d
    residual = float(1.00-s)/float(len(dnew))
    for j in tqdm(range(k)):
        #update by PR update
        dnew = pageRankerIter(g,d)
        #scale all PR values down by factor of s
        for u in dnew:
            dnew[u] *= s
        for i in dnew:
            dnew[i] += residual
    return dnew

def partF(g, k, s, links, word):
    d = {}
    n = len(g)
    for u in g:
        d[u] = float(1)/float(n)
    dnew = scaledPR(g, d, k, s)
    sortedD = sorted(dnew.keys(), reverse=True, key = lambda u: dnew[u])

    #filter so will only be in if link contains string
    finalList = []
    for u in sortedD:
        if links[u].find(word) != -1:
            finalList.append(u)

    #print the top five
    count = 0
    for u in finalList:
        print links[u]
        count +=1
        if count == 5:
            break


def partE(links, k, s):
    g = links
    d = {}
    n = len(g)
    for u in g:
        d[u] = float(1)/float(n)
    print "in E"
    dNew = scaledPR(g, d, k, s)
    bins = np.arange(0, .000035, .0000005)

    sns.distplot(dNew.values(), kde=False, bins = bins)
    plt.show()

def partD(links, k):
    g = links
    d = {}
    n = len(g)
    for u in g:
        d[u] = float(1)/float(n)
    dNew = basicPR(g, d, k)
    bins = np.arange(0, .000035, .0000005)
    sns.distplot(dNew.values(), kde=False, bins = bins)
    plt.show()

def partC(links):
    g = links
    d = {}
    n = len(g)
    for u in g:
        d[u] = float(1)/float(n)
    dNew = pageRankerIter(g, d)
    print len(dNew)
    bins = np.arange(0, .000035, .0000005)
    sns.distplot(dNew.values(), kde=False, bins=bins)
    plt.show()



def main():
    file = "google.txt"
    file2 = "links.txt"
    k = 200
    s = .85
    word = "34"
    gText = partB(file)
    links = makeGraphFromFileWithString(file2)

    #partC(gText)
    #partD(gText, k)
    partE(gText, k, s)
    #partF(gText, k, s, links, word)



if __name__ == '__main__':
    main()
