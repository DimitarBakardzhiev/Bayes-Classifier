import re
import requests
import json
import math

sportFileName = 'texts/sport.txt'
financeFileName = 'texts/finance.txt'
stemmingApi = 'http://text-processing.com/api/stem/'


# stems given text using an online api -> http://text-processing.com/docs/stem.html
def stemText(text):
    r = requests.post(stemmingApi, data = {'text': text})
    stemmed = json.loads(r.text)
    return stemmed['text']

# extracts each word with repetions from a text and returns a list
def getOnlyWords(text):
    words = []
    splitLine = text.split()
    for word in splitLine:
        if re.match('[a-zA-Z]', word):
            words.append(word)
    
    return words
     
def countDifferentWords(wordsList):
    return len(set(wordsList))

# analyzes a given file and return its bag of words after stemming the whole text
def getBagOfWords(fileName):
    file = open(fileName)

    allWordsList = []

    lines = file.readlines()
    for line in lines:
        line = line.lower()
        line = stemText(line)
        allWordsList += getOnlyWords(line)

    file.close()

    return allWordsList

# gets a list of words and returns a dictionary with a word as a key and its occurrence as value
def getWordsOccurrences(wordsList):
    wordsOccurrences = {}
    for word in wordsList:
        if wordsOccurrences.has_key(word):
            wordsOccurrences[word] += 1
        else:
            wordsOccurrences[word] = 1

    return wordsOccurrences

def laplasFormula(occurrenceInClass, allWordsCount, differentWordsCount):
    return math.log10(occurrenceInClass + 1) - math.log10(allWordsCount + differentWordsCount)
    #return (occurrenceInClass + 1) / (allWordsCount + differentWordsCount)

sportWords = getBagOfWords(sportFileName)
financeWords = getBagOfWords(financeFileName)

allWords = sportWords + financeWords
occurrences = getWordsOccurrences(allWords)
sportOccurrences = getWordsOccurrences(sportWords)
financeOccurrences = getWordsOccurrences(financeWords)

totalWordsCount = len(allWords)
differentWordsCount = len(occurrences)

while True:
    str = raw_input("Enter your input: ")
    str = str.lower()
    str = stemText(str)
    words = getOnlyWords(str)

    sportsProbability = math.log10(0.5)
    for word in words:
        if sportOccurrences.has_key(word):
            sportsProbability += laplasFormula(sportOccurrences[word], totalWordsCount, differentWordsCount)
        else:
            sportsProbability += laplasFormula(0, totalWordsCount, differentWordsCount)

    financeProbability = math.log10(0.5)
    for word in words:
        if financeOccurrences.has_key(word):
            financeProbability += laplasFormula(financeOccurrences[word], totalWordsCount, differentWordsCount)
        else:
            financeProbability += laplasFormula(0, totalWordsCount, differentWordsCount)

    if sportsProbability > financeProbability:
        print 'sport'
    else:
        print 'finance'