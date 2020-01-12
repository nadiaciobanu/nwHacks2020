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
        related = GetEntitiesAPI(s)
        matrix = SetRelations(related, matrix)
    return matrix

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

if __name__ == '__main__':
    allLines = LoadBookAndGetLines("test_story.txt")
    matrix = GetEntityGraph(allLines)
    print(matrix)