#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
* Copyright (c) 2012 University of Ljubljana, Faculty of Electrical Engineering.
* All rights reserved. Licensed under the Academic Free License version 3.0.
*
* @author Miha Gazvoda
* @version 25/04/2016
*
* Program makes information analysis of a file and produce Markov chain out of it.
'''

from collections import defaultdict, Counter
from re import findall
from math import log
from random import choice
import codecs


# naredi analizo besedila samo z lastnimi verjetnostmi besed
def basicFileAnalysis(fileName):
    # prestej besede
    wordCount = Counter(data)

    # izracun lastnih verjetnosti
    wordProbability = {}
    allWords = float(sum(wordCount.values()))
    for word in wordCount:
        wordProbability[word] = wordCount[word] / allWords

    # entropija enakomerno verjetnih besed
    uniformEntropy = -log(float(1) / len(wordCount), 2)

    # prava entropija
    entropy = 0
    for probability in wordProbability.values():
        entropy = -probability * log(probability, 2) + entropy

    return wordCount, wordProbability, uniformEntropy, entropy


# naredi analizo besedila relativno na prejsnjo besedo
def advancedFileAnalysis(fileName):
    # izracuna relativne frekvence
    wordRelativeCount = defaultdict(lambda: defaultdict(int))
    prevWord = data[0]
    for word in data[1:]:
        wordRelativeCount[prevWord][word] += 1
        prevWord = word

    # pogojna verjetnost & pogojna entropija
    wordRelativeProbability = defaultdict(lambda: defaultdict(int))
    relativeEntropy = {}
    ent = 0
    for parentWord in wordRelativeCount.keys():
        ent = 0
        for childWord in wordRelativeCount[parentWord].keys():
            # pogojna verjetnost
            wordRelativeProbability[parentWord][childWord] = float(wordRelativeCount[parentWord][childWord]) / sum(
                wordRelativeCount[parentWord].values())
            # racunanje pogojne entropije
            ent = -wordRelativeProbability[parentWord][childWord] * \
                  log(wordRelativeProbability[parentWord][childWord], 2) + ent
        relativeEntropy[parentWord] = ent

    return wordRelativeCount, wordRelativeProbability, relativeEntropy


# ustvari Markovovo verigo slovenskih besed
def createMarkovChain(wordCount, wordRelativeCount, textLength):
    text = []
    for i in range(textLength):
        if i == 0:
            # izbira prve besede
            word = choice([x for x in wordCount for y in range(wordCount[x])])
        else:
            # izbira ostalih besede
            word = choice([x for x in wordRelativeCount[prevWord]
                           for y in range(wordRelativeCount[prevWord][x])])
        text.append(word)
        prevWord = word
    return text


textLength = 25
fileName = 'trdina.txt'

data = codecs.open(fileName, 'r', 'utf-8')
data = data.read()
data = findall(r"[\w']+|[.,!?;:]", data)

wordCount, wordProbability, uniformEntropy, entropy = basicFileAnalysis(data)
wordRelativeCount, wordRelativeProbability, relativeEntropy = advancedFileAnalysis(data)
text = createMarkovChain(wordCount, wordRelativeCount, textLength)

print(wordRelativeCount['Gorjanci'])
print(relativeEntropy['Gorjanci'])

for word in text:
    print(word, end=' ')
