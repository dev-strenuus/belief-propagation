import numpy as np
import random

def generateRandomDistribution():
    sum = 0
    v = [0]*8
    for i in range(8):
        v[i] = random.randint(1,100)
        sum = sum + v[i]
    for i in range(8):
        v[i] = v[i] / sum
    return v[i]
n = 100
test = 0

q = []
q.append(0)
g = [ [] for i in range(n)]
cont = 1
while(len(q) > 0):
    curr = q.pop(0)
    children = min(np.random.randint(1,5), n-cont)
    for i in range(children):
        g[curr].append(cont)
        q.append(cont)
        cont = cont + 1

graph = [ [] for i in range(n)]
mapping = [-1]*n

def renameVariable(node, type, cont):
    if type == 0:
        mapping[node] = cont
        cont = cont + 1
    greatest = cont
    for child in g[node]:
        greatest = max(greatest, renameVariable(node, 1-type, cont))
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

fp = open("input"+str(test)+".txt", "w+")
fp.write()
