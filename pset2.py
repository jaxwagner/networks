#JACKSON WAGNER CS134 PSET 1 PROBLEM 5
import random
import math
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm


# PART 1 ***************************************************************
def makeLattice(r):
    n = r*r
    lattice = {}
    k = 2
    l = 2
    #add adjacent node connections and close node connections
    for i in range(1,r+1):
        for j in range(1,r+1):
            lst = set()
            for x in range(k*(-1),k + 1):
                for y in range(k*(-1),k + 1):
                    if i + x > 0 and i + x <= r and j + y > 0 \
                    and j + y <= r and (x != 0 or y != 0):
                        dist = abs(x) + abs(y)
                        if dist <= k:
                            lst.add((i+x, j+y))
            lattice[(i,j)] = lst
    #long range connections
    for key in lattice:
        x1 = random.randrange(1,r + 1)
        y1 = random.randrange(1,r + 1)
        x2 = random.randrange(1,r + 1)
        y2 = random.randrange(1,r + 1)
        while (x1,y1) in lattice[key]:
            x1 = random.randrange(1,r + 1)
            y1 = random.randrange(1,r + 1)
        while (x2,y2) in lattice[key]:
            x2 = random.randrange(1,r + 1)
            y2 = random.randrange(1,r + 1)
        lattice[key].add((x1,y1))
        lattice[key].add((x2,y2))
    if r == 2:
        print (lattice)
    return lattice

def distance(lattice, n1, n2):
    #breadth first search
    queue = [(n1, 0)]
    seen = set([n1])
    while len(queue) > 0:
        (vertex, steps) = queue.pop(0)

        if vertex == n2:
            return steps

        for next in lattice[vertex]:
            if next not in seen:
                seen.add(next)
                queue.append((next,steps + 1))
    return -1

def getAveDistance(r):
     numGraphsOfSize = 5
     distanceSum = 0
     #sum distances
     for i in range(0,numGraphsOfSize):
         l = makeLattice(r)
         d = 0
         n = 0
         for x in range(1, r + 1):
             for y in range(1,r+1):
                 for x1 in range(1, r + 1):
                     for y1 in range(1,r+1):
                         n += 1
                         d += distance(l, (x,y), (x1, y1))
        #get average
         aveI = (float(d)/float(n))
         distanceSum += aveI
     return distanceSum/numGraphsOfSize



def part1():
    print "This might take a minute :)"
    rMax = 10
    xList = []
    yList = []
    logX = []
    for x in range(1,rMax):
        xList.append(x*x)
        yList.append(getAveDistance(x))
        logX.append(math.log10(x))
    plt.plot(xList, yList)
    plt.plot(xList, logX)
    plt.show()

#PART 2 ****************************************************************
def makeKleinberg(r):
    n = r*r
    lattice = {}
    k = 2
    l = 2
    #add adjacent node connections and close node connections
    for i in range(1,r+1):
        for j in range(1,r+1):
            lst = set()
            for x in range(k*(-1),k + 1):
                for y in range(k*(-1),k + 1):
                    if i + x > 0 and i + x <= r and j + y > 0 \
                    and j + y <= r and (x != 0 or y != 0):
                        dist = abs(x) + abs(y)
                        if dist <= k:
                            lst.add((i+x, j+y))
            lattice[(i,j)] = lst
    # long range connecitons
    for key in lattice:
        count = 0
        for i in range(1, r+1):
            for j in range(1, r+1):
                p = getProb(lattice, key, (i,j), r)
                if random.randrange(0,1) < p and count < l \
                and (i,j) not in lattice[key]:
                    lattice[key].add((i,j))
                    count += 1
    return lattice

def getProb(lattice, key, node, r):
    nominator = 0
    denominator = 0
    #program the given formula for probability
    if distance(lattice, key, node) != 0:
        nominator = 1.0/(float(distance(lattice, key, node)**2))
    for i in range(1, r + 1):
        for j in range(1, r+1):
            if key != (i,j):
                denominator += 1.0/(float(distance(lattice, key, (i,j))**2))
    if denominator == 0:
        return float(nominator)
    return (float(nominator)/float(denominator))

def getAveKleinbergDistance(r):
     numGraphsOfSize = 5
     distanceSum = 0
     for i in range(0,numGraphsOfSize):
         l = makeKleinberg(r)
         d = 0
         n = 0
         for x in range(1, r + 1):
             for y in range(1,r+1):
                 for x1 in range(1, r + 1):
                     for y1 in range(1,r+1):
                         n += 1
                         d += distance(l, (x,y), (x1, y1))

         aveI = (float(d)/float(n))
         distanceSum += aveI
     return distanceSum/numGraphsOfSize

def part2():
    print "This might take a minute :)"
    rMax = 10
    xList = []
    yList = []
    logX = []
    for x in range(1,rMax):
        print "in the loop"
        xList.append(x*x)
        yList.append(getAveKleinbergDistance(x))

    for x in range(2, rMax**2):
            logX.append(math.log10(math.log10(x)))
    plt.plot(xList, yList)
    plt.plot(logX)
    plt.show()

#PART 3 *************************************************************
def makeLatticeFromFile(s):
    with open(s, "r") as ins:
        graph = {}
        for line in tqdm(ins):
            key, value = map(int,line.split("\t"))
            if key not in graph:
                graph[key] = [value]
            else:
                graph[key].append(value)
            if value not in graph:
                graph[value] = []
        return graph

#search by going to "geographically closest node" with each step
def kleinbergSearch(graph, start, end, dist=0):
    closest = graph[start][0]
    seenNodes = set()
    numSteps = 0
    while closest != end and closest not in seenNodes:
        seenNodes.add(closest)
        for x in range(1, len(graph[start])):
            if abs(end - graph[start][x]) < abs(end - closest):
                closest = graph[start][x]
        numSteps += 1
    if closest == end:
        return numSteps
    return -1



def shortestDistance(graph, start, end):
    queue = [(start, 0)]
    seen = set([start])
    while len(queue) > 0:
        (vertex, steps) = queue.pop(0)

        if vertex == end:
            return steps

        for next in graph[vertex]:
            if next not in seen:
                seen.add(next)
                queue.append((next,steps + 1))
    return -1

def getAveDistFromFile(s):
    numSamples = 20
    successfulSamples = numSamples
    distanceSum = 0
    graph = {}
    graph = makeLatticeFromFile(s)
    for i in tqdm(range(1,numSamples)):
        start = random.choice(graph.keys())
        end = random.choice(graph.keys())
        d = 0
        while start == end:
            end = random.choice(graph.keys())
        #commented code to implement kleinbergSearch algorithm
        # if s == "livejournal.txt":
        #     d = kleinbergSearch(graph, start, end)
        # else:
        #     d = shortestDistance(graph, start, end)
        d = shortestDistance(graph, start, end)
        if d == -1:
            successfulSamples -= 1
        else:
            distanceSum += d
    return float(distanceSum)/float(successfulSamples)




def part3():
    #set s to the name of the text file and put file in directory of py file
    s = "enron.txt"
    #s = "epinions.txt"
    #s = "livejournal.txt"
    print "{}: This might take a minute :)".format(s)
    print "Average shortest distance: {}".format((getAveDistFromFile(s)))



def main():
    #part1()
    #part2()
    part3()
    #getAveDistance(2)

if __name__ == '__main__':
    main()
