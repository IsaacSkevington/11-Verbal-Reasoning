from PyDictionary import PyDictionary
import datetime
import os.path
import nltk
from nltk import text
from nltk.corpus.reader.tagged import MacMorphoCorpusReader
import operator
try:
    from nltk.corpus import wordnet
except:
    nltk.download('wordnet')
    from nltk.corpus import wordnet
import pickle
import tkinter as tk
import tkinter.ttk as ttk
import threading
from tkExtensions import*
dictionary=PyDictionary()

#Get the definition of a word
def getDefinition(word):
    definition = dictionary.meaning(word)
    if definition is None:
        return {}
    return definition
    

#Correct the brackets in a string to make sure they are always closed
def correctBrackets(string):
    bracketFlag = False
    for char in string:
        if char == "(":
            bracketFlag = True
    if bracketFlag:
        string += ")"
    return string



#Format the definition to be read
def formatDefinition(definition):
    format = ""
    if definition is None or definition == {}:
        return "No Definition Available"
    for key in definition.keys():
        format += (key + ":\n")
        for i in range(len(definition[key])):
            definitionSpecific = definition[key][i]
            definitionSpecific = (definitionSpecific[0].upper()) + definitionSpecific[1:]
            definitionSpecific = correctBrackets(definitionSpecific)
            format += "  " + str(i + 1) + "." + "   " + definitionSpecific + "\n"
        format += "\n"
    return format

#Get the synomyms of a word
def getSynonyms(word):
    try:        
        return dictionary.synonym(word)
    except:
        return []
    
#Get the antonyms of a word
def getAntonyms(word):
    try:        
        return dictionary.antonym(word)
    except:
        return []



#Get the min, max and average similarity in meaning of 2 words
def getRelation(word1, word2):
    try:
        syns1 = wordnet.synsets(word1)
        syns2 = wordnet.synsets(word2)
        maxRelation = 0.0
        minRelation = 1.0
        averageRelationSum = 0.0
        relationCount = 0.0
        for syn1 in syns1:
            for syn2 in syns2:
                relation = syn1.wup_similarity(syn2)
                if relation > maxRelation:
                    maxRelation = relation
                if relation < minRelation:
                    minRelation = relation
                averageRelationSum += relation
                relationCount += 1
        if relationCount != 0:
            averageRelation = averageRelationSum / relationCount
            return maxRelation, minRelation, averageRelation
        else:
            return -1, -1, -1
    except:
        return -1, -1, -1





THREADS = 100 #Number of threads used to generate the word data

#The data about a set of words
class WordData:
    def __init__(self, words):
        self.words = words
        self.wordRelations = {}
        self.definitions = {}
        self.synonyms = {}
        self.antonyms = {}
        self.nextWord = 0
    
    #Save the data
    def save(self):
        with open("wordData.bin", 'wb') as file:
            pickle.dump(self, file)

    #Get a definition of a word in the set
    def definition(self, word):
        try:
            return self.definitions[word]
        except:
            return {}
        
    #Get the synoyms of a word in the set
    def synonym(self, word):
        try:
            return self.synonyms[word]
        except:
            return None

    #Get the antonyms of a word in the set
    def antonym(self, word):
        try:
            return self.antonyms[word]
        except:
            return None

    #Check if a word in the set is an adjective
    def isAdjective(self, word):
        try:
            return "Adjective" in self.definition(word).keys()
        except:
            return False

    ##############FUNCTIONS BELOW ARE FOR UPLOADING NEW WORD SETS ONLY AND ARENT CALLED IN DAY TO DAY USE. DON'T CALL THEM###############
    def populate(self):
        try:
            self.getDefs()
        except KeyboardInterrupt:
            print("\nExiting...")
            self.save()
        
    def getAnts(self):
        count = 0
        threads = []
        def get(start, end):
            for i in range(start, end):
                self.antonyms[self.words[i]] = getAntonyms(self.words[i])
            print("Words " + str(start) + " to " + str(end) + " done")
            return 0
        end = 0
        sizeOfCat = len(self.words)//THREADS
        for i in range(THREADS):
            start = end
            end = start + sizeOfCat
            t = threading.Thread(target=get, args=[start, end])
            t.start()                
            threads.append(t)
        t = threading.Thread(target=get, args=[end, len(self.words)])
        t.start()                
        threads.append(t)

        for t in threads:
            t.join()
        print("Saving...")
        self.save()
        print("Finished Antonyms")
  
        
        

        

    def getDefs(self):
        count = 0
        threads = []
        def get(start, end):
            for i in range(start, end):
                self.definitions[self.words[i]] = getDefinition(self.words[i])
            print("Words " + str(start) + " to " + str(end) + " done")
        end = 0
        sizeOfCat = len(self.words)//THREADS
        for i in range(THREADS):
            start = end
            end = start + sizeOfCat
            t = threading.Thread(target=get, args=[start, end])
            t.start()                
            threads.append(t)
        t = threading.Thread(target=get, args=[end, len(self.words)])
        t.start()                
        threads.append(t)
        threadsDone = True
        for t in threads:
            t.join()
        print("Saving...")
        self.save()
        print("Finished Defs")


    def getSyns(self):
        count = 0
        threads = []
        def get(start, end):
            for i in range(start, end):
                self.synonyms[self.words[i]] = getSynonyms(self.words[i])
            print("Words " + str(start) + " to " + str(end) + " done")
        end = 0
        sizeOfCat = len(self.words)//THREADS
        for i in range(THREADS):
            start = end
            end = start + sizeOfCat
            t = threading.Thread(target=get, args=[start, end])
            t.start()                
            threads.append(t)
        t = threading.Thread(target=get, args=[end, len(self.words)])
        t.start()                
        threads.append(t)
        threadsDone = True
        for t in threads:
            t.join()
        print("Saving...")
        self.save()
        print("Finished Synonyms")
    
#Get the word data in a file      
def getWords(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)

#Get the word data from the default file
def loadWordData():
    with open(resourcePath("wordData.bin"), 'rb') as file:
        return pickle.load(file)




