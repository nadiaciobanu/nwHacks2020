# Utility Functions for Entity Graph
# Nadia Ciobanu and Adam Bignell

from collections import defaultdict
from itertools import permutations

# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

import numpy as np

import matplotlib.pyplot as plt
import networkx as nx


def drawGraph(matrix, adjList):
    nodes = adjList.keys()
    indexToNode = {}
    for i, node in enumerate(nodes):
        indexToNode[i] = node

    rows, cols = np.where(matrix == 1)
    edges = zip(rows.tolist(), cols.tolist())
    gr = nx.Graph()
    gr.add_edges_from(edges)
    nx.draw(gr, node_size=0, labels=indexToNode, with_labels=True)
    plt.show()


def GetEntityGraph(allLines):
    sentences = []
    for line in allLines:
        sentences.extend(line.split('.'))
    adjList = defaultdict(set)
    for s in sentences:
        if s != "":
            #related = GetEntitiesAPI(s)
            related = GetEntitiesDummy(s)
            adjList = SetRelations(related, adjList)

    matrix = makeMatrix(adjList)
    drawGraph(matrix, adjList)

    return adjList


def makeMatrix(adjList):
    numEnts = len(adjList)
    nodes = adjList.keys()

    nodeToIndex = {}
    i = 0
    for node in nodes:
        nodeToIndex[node] = i
        i = i + 1

    matrix = np.zeros((numEnts, numEnts))

    for node in nodes:
        for neigh in adjList[node]:
            nodeIndex = nodeToIndex[node]
            neighIndex = nodeToIndex[neigh]
            matrix[nodeIndex][neighIndex] = 1
    return matrix


def GetEntitiesDummy(text):
    ent_set = set()
    words = text.split()
    for w in words:
        if w[0].isupper():
            ent_set.add(w)
    return ent_set


def GetEntitiesAPI(text):
    # Instantiates a client
    client = language.LanguageServiceClient()

    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Get entities in text
    entities = client.analyze_entities(document=document, encoding_type='UTF32').entities
    ent_set = set()

    # e has e.name, e.type plus others
    for e in entities:
        if e.type in {1}:
            ent_set.add(e.name)
    return ent_set


def SetRelations(related, adjList):
    for (u,v) in permutations(related,2):
        if u != v:
            adjList[u].add(v)
    return adjList


def LoadBookAndGetLines(filename):
    allLines = []
    with open(filename, 'r') as file:
        allLines.extend(file.readlines())
    return allLines


def PreProcessGutenbergBook(lines):
    goodLines = []
    beforeStart = True
    for line in lines:
        if ("*** START" in line):
            beforeStart = False
        if beforeStart or (line == "\n"):
            continue
        if "*** END " not in line:
            goodLines.append(line)
        else:
            goodLines.pop(0)
            return goodLines
    return goodLines


if __name__ == '__main__':
    allLines = LoadBookAndGetLines("alice.txt")

    # Be careful with the below! You'll want to throttle as this actually uses API credits
    adjList = GetEntityGraph(allLines[1000:1200])
    
    #allLines = LoadBookAndGetLines("alice.txt")
    #goodLines = PreProcessGutenbergBook(allLines)
    #print(goodLines[0:20])
