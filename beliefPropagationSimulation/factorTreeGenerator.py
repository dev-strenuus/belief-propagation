import numpy as np
import random
import sys
sys.setrecursionlimit(10000)


minNumberOfChildren = 5
maxNumberOfChildren = 6
n = 1000000
test = 0

def generateRandomDistribution(length):
    sum = 0
    v = [0]*length
    for i in range(length):
        v[i] = random.randint(1, 500)
        sum = sum + v[i]
    for i in range(length):
        v[i] = v[i] / sum
    return v

q = []
q.append(0)
g = [ [] for i in range(n)]
cont = 1
while(len(q) > 0):
    curr = q.pop(0)
    children = min(np.random.randint(minNumberOfChildren,maxNumberOfChildren), n-cont)
    for i in range(children):
        g[curr].append(cont)
        q.append(cont)
        cont = cont + 1

graph = [ [] for i in range(n)]
mapping = [-1]*n

def renameVariable(node, type, newId):
    if type == 0:
        mapping[node] = newId
        newId = newId + 1
    greatest = newId
    for child in g[node]:
        greatest = max(greatest, renameVariable(child, 1-type, greatest))
    return greatest




variablesNumber = renameVariable(0 ,0 , 0)
factorsNumber = n - variablesNumber
cont = variablesNumber
for i in range(n):
    if mapping[i] == -1:
        mapping[i] = cont
        cont = cont + 1

for i in range(n):
    for j in g[i]:
        graph[mapping[i]].append(mapping[j])
        graph[mapping[j]].append(mapping[i])

fp = open("../data/input"+str(test)+".txt", "w+")
fp.write(str(variablesNumber)+ " " + str(factorsNumber) + "\n")
for i in range(factorsNumber):
    for j in graph[variablesNumber+i]:
        fp.write(str(j))
        if j != graph[variablesNumber+i][len(graph[variablesNumber+i])-1]:
            fp.write(" ")
    fp.write("\n")
    temp = generateRandomDistribution(2**len(graph[variablesNumber+i]))
    for j in range(2**len(graph[variablesNumber+i])):
        fp.write(str(temp[j]))
        if j != 2**len(graph[variablesNumber+i]) - 1:
            fp.write(" ")
    fp.write("\n")
fp.close()