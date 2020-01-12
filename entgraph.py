# Utility Functions for Entity Graph
# Nadia Ciobanu and Adam Bignell

from collections import defaultdict
from itertools import permutations

# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

def GetEntityGraph(allLines):
    sentences = []
    for line in allLines:
        sentences.extend(line.split('.'))
    matrix = defaultdict(set)
    for s in sentences:
        if s != "":
            #related = GetEntitiesAPI(s)
            related = GetEntitiesDummy(s)
            matrix = SetRelations(related, matrix)
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
    matrix = GetEntityGraph(allLines[1000:1200])
    print(matrix)
    
    #allLines = LoadBookAndGetLines("alice.txt")
    #goodLines = PreProcessGutenbergBook(allLines)
    #print(goodLines[0:20])