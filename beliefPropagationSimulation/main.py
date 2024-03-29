import numpy as np
from message import Message
import sys
sys.setrecursionlimit(10000)

fp = open("../data/input0.txt", "r")

def dfs(node, parent):
    #print(node)
    ctrl = 0
    for child in graph[node]:
        if child != parent:
            ctrl = 1
            dfs(child, node)
    if ctrl == 0:
        leaves.append(node)


def getDistribution(nodeId, states):
    index = 0
    cont = 1
    for state in states:
        index = index + cont*int(state)
        cont = cont * 2
    return distributions[nodeId-variablesNumber][index]

def computeProductOfMessagesForVariableNode(observation, node):
    value = 1
    for message in collectedMessages[observation][node]:
        value = value * message.value
    return value

def computeProductOfMessagesForFactorNode(node, states, destinationNode):
    value = 1
    for i in range(len(states)):
        neighbor = graph[node][i]
        state = states[i]
        if neighbor != destinationNode:
            for message in collectedMessages[state][node]:
                if message.source == neighbor:
                    value = value * message.value
    return value


def computeFactorToVariableMessageSummation(pos, observation, factorNode, destinationNode, states):
    if pos == len(graph[factorNode]):
        return getDistribution(factorNode, states)*computeProductOfMessagesForFactorNode(factorNode, states, destinationNode)

    if graph[factorNode][pos] == destinationNode:
        states.append(observation)
        temp = computeFactorToVariableMessageSummation(pos+1, observation, factorNode, destinationNode, states)
        states.pop()
        return temp

    temp = 0
    states.append(0)
    temp = temp + computeFactorToVariableMessageSummation(pos + 1, observation, factorNode, destinationNode, states)
    states.pop()
    states.append(1)
    temp = temp + computeFactorToVariableMessageSummation(pos + 1, observation, factorNode, destinationNode, states)
    states.pop()
    return temp




def computeFactorToVariableMessage(observation, factorNode, destinationNode):
    return computeFactorToVariableMessageSummation(0, observation, factorNode, destinationNode, [])


def findDestinationNode(observation, node):
    destinationNode = -1
    for neighbor in graph[node]:
        temp = 0
        for message in collectedMessages[observation][node]:
            if message.source == neighbor:
                temp = 1
        if temp == 0:
            destinationNode = neighbor
            break
    return destinationNode

def sendMessageFromFactorToVariable(message, observation):
    #print(str(message.source) + " " + str(message.destination) + " " + str(observation))
    variableNode = message.destination
    collectedMessages[observation][variableNode].append(message)
    if len(graph[variableNode]) == 1: #if a leaf don't proceede
        return
    if len(collectedMessages[observation][variableNode]) == len(graph[variableNode]) - 1:
        destinationNode = findDestinationNode(observation, variableNode)
        firstDestination[variableNode] = destinationNode
        sendMessageFromVariableToFactor(Message(variableNode, destinationNode, computeProductOfMessagesForVariableNode(observation, variableNode)), observation)
    elif len(collectedMessages[observation][variableNode]) == len(graph[variableNode]):
        value = computeProductOfMessagesForVariableNode(observation, variableNode)
        for neighbor in graph[variableNode]: #try all the neighbors
            if neighbor != firstDestination[variableNode]: # but not the one that I tried in the first if statement
                for message in collectedMessages[observation][variableNode]: # need to find the message (whose destination is current neighbor) that I want to remove from the product I will send as a message
                    if message.source == neighbor:
                        sendMessageFromVariableToFactor(Message(variableNode, neighbor, value/message.value), observation)
                        break



def sendMessageFromVariableToFactor(message, observation):
    factorNode = message.destination
    collectedMessages[observation][factorNode].append(message)
    if len(graph[factorNode]) == 1: #if a leaf don't proceede
        return
    if len(collectedMessages[0][factorNode])  >= (len(graph[factorNode]) - 1) and len(collectedMessages[1][factorNode]) >= (len(graph[factorNode]) - 1):
        destinationNode = findDestinationNode(0, factorNode)
        destinationNode1 = findDestinationNode(1, factorNode)
        if destinationNode == destinationNode1 and destinationNode != -1:
            firstDestination[factorNode] = destinationNode
            sendMessageFromFactorToVariable(Message(factorNode, destinationNode, computeFactorToVariableMessage(0, factorNode, destinationNode)), 0)
            sendMessageFromFactorToVariable(Message(factorNode, destinationNode, computeFactorToVariableMessage(1, factorNode, destinationNode)), 1)
        elif destinationNode == destinationNode1 and destinationNode == -1:
            for neighbor in graph[factorNode]:
                if neighbor != firstDestination[factorNode]:
                    sendMessageFromFactorToVariable(Message(factorNode, neighbor, computeFactorToVariableMessage(0, factorNode, neighbor)), 0)
                    sendMessageFromFactorToVariable(Message(factorNode, neighbor, computeFactorToVariableMessage(1, factorNode, neighbor)), 1)


variablesNumber, factorsNumber = list(map(int, fp.readline().split(" ")))
graph = [0]*(variablesNumber + factorsNumber)
collectedMessages = [ [ [] for i in range(variablesNumber + factorsNumber) ] for j in range(2) ]
firstDestination = [-1]*(variablesNumber + factorsNumber)
leaves = []
leaves.append(0)

for i in range(len(graph)):
    graph[i] = []
distributions = []
for i in range(factorsNumber):
    nodeId = variablesNumber + i
    adjacentNodes = list(map(int, fp.readline().split(" ")))
    distributions.append(np.array(list(map(float, fp.readline().split(" ")))))
    for node in adjacentNodes:
        graph[nodeId].append(node)
        graph[node].append(nodeId)

dfs(0, -1)

for leaf in leaves:
    if leaf < variablesNumber:
        sendMessageFromVariableToFactor(Message(leaf, graph[leaf][0], 1), 0)
        sendMessageFromVariableToFactor(Message(leaf, graph[leaf][0], 1), 1)
    else:
        sendMessageFromFactorToVariable(Message(leaf, graph[leaf][0], getDistribution(leaf, "0")), 0)
        sendMessageFromFactorToVariable(Message(leaf, graph[leaf][0], getDistribution(leaf, "1")), 1)

for variable in range(variablesNumber):
    marginal = [1,1]
    for observation in range(2):
        for message in collectedMessages[observation][variable]:
            marginal[observation] = marginal[observation]*message.value
    for observation in range(2):
        print("Marginal distribution p(x"+str(variable)+" = "+str(observation)+") = "+str(marginal[observation]/(marginal[0]+marginal[1])))
    print("Normalization costant: "+str((marginal[0]+marginal[1])))



