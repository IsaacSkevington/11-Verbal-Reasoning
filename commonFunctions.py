import random
import pickle
import re
import nltk
import sys
import os

try:
    from nltk.corpus import wordnet
except:
    nltk.download('wordnet')
    from nltk.corpus import wordnet

#Load a binary file
def getWords(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)

#Set the correct path for resources
def resourcePath(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

#Get the word list and dictionary
words = getWords(resourcePath("Data\\commonwords.bin"))
allwords = getWords(resourcePath("Data\\allwords.bin"))
wordDict = {}
for word in words:
    wordDict[word] = ""

allwordDict = {}
for word in allwords:
    allwordDict[word] = ""

#Add zeros to a string
def az(string):
    if len(string) == 1:
        return "0"+string
    return string

#Subtract one time (HH:mm:ss) from another
def subtractTimes(larger, smaller):
    lhours = int(larger[:2])
    lmins = int(larger[3:5])
    lsecs = int(larger[6:])
    shours = int(smaller[:2])
    smins = int(smaller[3:5])
    ssecs = int(smaller[6:])
    ltotSecs = lhours * 60 * 60 + lmins * 60 + lsecs
    stotSecs = shours * 60 * 60 + smins * 60 + ssecs
    totSecs = ltotSecs - stotSecs
    hours = totSecs // 3600
    totSecs -= hours * 3600
    mins = totSecs//60
    totSecs -= mins * 60
    secs = totSecs
    return az(str(hours)) + ":" + az(str(mins)) + ":" + az(str(secs))


#Boolean to string
def btos(bool):
    if bool:
        return "Yes"
    else:
        return "No"

#Find all occurences of a letter in a string
def findall(string, letter):
    indexes = []
    for i in range(len(string)):
        if string[i] == letter:
            indexes.append(i)
    return indexes

#Generate a random word based on a number of condtions
def randomWord(minLength = 0, maxLength = 100, format = "", exclude = [], wordsList = None):
    if wordsList is None:
        wordsList = allwords
    if format == "":
        for i in range(len(wordsList)):
            word = wordsList[random.randint(0, len(wordsList) - 1)]
            if len(word) >= minLength and len(word) <= maxLength and word not in exclude:
                return word
        return None
    else:
        for i in range(len(wordsList)):
            word = wordsList[random.randint(0, len(wordsList) - 1)]
            if(re.search(format, word)) and len(word) >= minLength and len(word) <= maxLength and word not in exclude:
                return word
        return None

#Round a number 'x' to a number of decimal places 'places'
def dp(x, places):
    x = str(x)
    p = x.find(".")
    if p == -1:
        return x
    newx = x[:p]
    for i in range(p, p+ places + 1):
        try:
            newx += x[i]
        except:
            return newx
    return newx


#Get a random word that occurs in both lists
def randomWordTwoLists(minLength, maxLength, wordList, checkList = None, format = "", exclude = []):
    if checkList is None:
        checkList = allwords

    for i in range(len(wordList) * 2):
        word = randomWord(minLength, maxLength, format=format, exclude=exclude, wordsList=wordList)
        if word in checkList:
            return word
    return None

#Generate a random number excluding values in 'exclude'
def randomNumber(min, max, exclude = []):
    x = [i for i in range(min, max + 1)]
    viable = False
    if len(exclude) >= len(x):
        for num in x:
            if num not in exclude:
                viable = True
        if not viable:
            return min - 1
    while True:
        num = random.randint(min, max)
        if num not in exclude:
            return num

#Check if a string contains all characters in an array
def containsAll(string, array):
    for char in array:
        if(len(re.findall(char, string)) < array.count(char)):
            return False
        
    return True
            

#Find the number of occurences of value i in a list l
def occurences(i, l):
    occurenceDict = {i : 0}
    for x in l:
        occurenceDict[x] = 0
    for x in l:
        occurenceDict[x] += 1
    return occurenceDict[i]


#Get the lower of 2 variables
def lower(x, y):
    if x < y:
        return x
    else:
        return y

#Get the higher of two variables
def higher(x, y):
    if x < y:
        return y
    else:
        return x

#Insert a string into another string at a specific position
def insert(string, insert, position):
    if position >= len(string):
        return string + insert
    part1 = string[:position]
    part2 = string[position:]
    return part1 + insert + part2

#Remove a character at position from string
def pop(string, position):
    if position == len(string) - 1:
        return string[:-1]
    return string[:position] + string[position + 1:]

#Import a new list of words in filename, process them, and store them in newFile
def importWords(filename, newFile):
    with open(filename, 'r') as file:
        words = file.readlines()
    for i in range(len(words)):
        words[i] = words[i].replace("\n", "")
    with open(newFile, 'wb') as file:
        pickle.dump(words, file)

#Get the number of words in a sentence
def numberOfWords(sentence):
    count = 0
    for char in sentence:
        if char == ' ':
            count += 1
    return count + 1

#Get a random sentence containing a specific word. Length is measured in words
def getRandomSentence(word, minLength = 0, maxLength = 1000):
    try:
        lemmas = wordnet.lemmas(word)
    except:
        return None
    if len(lemmas) == 0:
        return None
    lemma = lemmas[random.randint(0, len(lemmas) - 1)]
    syn = lemma.synset()
    sentences = syn.examples()
    if len(sentences) == 0:
        return None
    random.shuffle(sentences)
    for sentence in sentences:
        numwords = numberOfWords(sentence)
        if numwords > minLength and numwords < maxLength:
            return sentence 
    return None