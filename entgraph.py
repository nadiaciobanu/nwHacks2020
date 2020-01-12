# Utility Functions for Entity Graph
# Nadia Ciobanu and Adam Bignell

from collections import defaultdict
from itertools import permutations

def GetEntityGraph(allLines):
    sentences = []
    for line in allLines:
        sentences.extend(line.split('.'))
    matrix = defaultdict(set)
    for s in sentences:
        related = GetEntities(s)
        matrix = SetRelations(related, matrix)
    return matrix

def GetEntities(sentence):
    # Dummy version below ===================
    words = sentence.split()
    entities = []
    for word in words:
       if word[0].isupper():
           entities.append(word)

    # API Call below ========================
    #entities = []

    return entities

def SetRelations(related, matrix):
    for (u,v) in permutations(related,2):
        if u != v:
            matrix[u].add(v)
    return matrix

def LoadBookAndGetLines(filename):
    allLines = []
    with open(filename, 'r') as file:
        allLines.extend(file.readlines())
    return allLines

if __name__ == '__main__':
    allLines = LoadBookAndGetLines("test_story.txt")
    matrix = GetEntityGraph(allLines)
    print(matrix)