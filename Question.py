from wordData import *
from tkExtensions import *
from sequenceGenerator import SequenceGenerator
from constants import *
import random
from commonFunctions import *

#Set the wordData object
wordData = None
def setWordData(data):
    global wordData
    wordData = data


#Question base class
class Question:
    def __init__(self, daysToComplete = None):
        self.answer = ""
        self.wordsToLookup = []
        self.correct = False
        self.dateSet = datetime.datetime.now()
        self.correctAnswer = ""
        self.submitButtonSettings = {
            "hoverColour":BUTTONACTIVEBACKGROUND,
            "hoverText":BUTTONACTIVETEXT,
            "fg":BUTTONIDLETEXT,
            "bg":BUTTONIDLEBACKGROUND,
            "activeforeground":BUTTONCLICKEDTEXT, 
            "activebackground":BUTTONCLICKEDBACKGROUND,
            "bd":BUTTONBORDERWIDTH,
            "highlightbackground":BUTTONBORDER,
            "relief":"solid",
            "width":10,
            "height":1,
            "font":(FONT, 15)
        }
        if daysToComplete is not None:
            self.dateDue = self.dateSet + ONEDAY
        else:
            self.dateDue = None
    #Generate the question
    def generate(self):
        pass
    #Check if the answer was correct
    def verify(self, answer):
        self.answer=answer
        return answer != ""
    #Wrapper display function
    def display(self, endFunction, parent, submitNow = True):
        pass

    #View the question and its result after doing it
    def view(self, parent):
        pass
        


#A question about completeing sequences 
class SequenceQuestion(Question):
    def __init__(self, min = -100, max = 100, step = 10, maxEndStep = 100, maxStepChange = 10, maxMultiDivisionFactor = 10, minDegree = 2, maxDegree = 10, minStartValue = -10, maxStartValue = 10):
        #kwargs for the sequence generator
        self.kwargs = {"min":min,
                       "max":max,
                       "step":step,
                       "maxEndStep":maxEndStep,
                       "maxStepChange":maxStepChange,
                       "maxMultiDivisionFactor":maxMultiDivisionFactor,
                       "minDegree":minDegree,
                       "maxDegree":maxDegree,
                       "minStartValue":minStartValue,
                       "maxStartValue":maxStartValue                       
        }
        super().__init__()
        self.sequence = []
        self.nextTerm = 0 
        self.timeToForm = 0
        self.answer = None
        self.correctAnswer = None
        self.correct = False
        self.options = []
        self.seqtype = None
        self.typeExplaination = None #Explains what type of sequence is used
        self.type = "Complete the sequence" #Title of the question
        self.generate()

    #Generate the question
    def generate(self):
        s = SequenceGenerator(**self.kwargs) #Create a new sequence generator
        fullsequence = []
        while len(fullsequence) < 10: #Get a sequence with a length less than 10
            fullsequence, self.seqtype = s.random() #Generate a random sequence
        self.typeExplaination = s.typeDescriptions[self.seqtype] #Get an explanation of the type of sequence
        sequenceLength = randomNumber(5,7) #Generate a final sequence length
        sequenceStart = randomNumber(0,len(fullsequence)-(sequenceLength + 2)) #Generate a position in the full sequence to start the final sequence
        self.sequence = []
        i = None

        #Generate the final sequence
        for i in range(sequenceStart, sequenceStart + sequenceLength):
            self.sequence.append(fullsequence[i])
        self.correctAnswer = fullsequence[i + 1] #Get the correct answer


        #Generate the options for the multiple choice question

        #Set the bounds for the options
        minValue = self.sequence[0]
        maxValue = self.sequence[-1]
        if minValue > maxValue:
            temp = minValue
            minValue = maxValue
            maxValue = temp

        #Get the options
        self.options = [self.correctAnswer]
        for i in range(4):
            x = randomNumber(minValue, maxValue, exclude = self.options)
            while x == (minValue - 1):
                minValue -= 1
                x = randomNumber(minValue, maxValue, exclude = self.options)
            self.options.append(x)
        random.shuffle(self.options)

        


        
 
    #Check if the answer was correct
    def verify(self, answer):
        if not super().verify(answer):
            return False
        return answer == str(self.correctAnswer)

    #Display the question on android
    def displayAndroid():
        pass

    #Display the question on windows
    def displayWindows(self, endFunction, parent, submitNow = True):

        #Question Description
        tk.Label(parent, text = "In each question, find the number that continues the series in the most sensible way and write it in the box", font=(FONT, 13, "bold", "underline")).pack(padx=5, pady=5)
        tk.Label(parent, text=", ".join([str(s) for s in self.sequence]), font=(FONT, 12, "bold")).pack(padx=5, pady=5)
        optionsFrame = tk.Frame(parent)
        for i in range(len(self.options)):
            tk.Label(optionsFrame, text=str(self.options[i]), font=(FONT, 12)).grid(row = 0, column = i, padx=5, pady=5)
        optionsFrame.pack(padx=5, pady=5)

        #Answer box
        answerBox = tk.Entry(parent, font=(FONT, 12))
        answerBox.pack(padx=5, pady=5)
        submitButton = None

        #Show the result after marking
        def showResult():
            if answerBox.get() != "":
                self.correct = self.verify(answerBox.get()) #Mark the question

                #Display the result
                if(self.correct):
                    tk.Label(parent, text="Correct!", font=(FONT, 12)).pack(padx=5, pady=5)
                else:
                    tk.Label(parent, text="Incorrect :( The right answer was: '" + str(self.correctAnswer) + "'", font=(FONT, 12)).pack(padx=5, pady=5)
                submitButton.destroy()
                endFunction(self, [], self.type)
        
        #Create the submit button if the question is to be marked immediately after doing it
        if submitNow:
            submitButton = HoverButton(parent, text = "Submit", command=showResult, **self.submitButtonSettings)
            submitButton.pack(padx=5, pady=5)
        parent.pack()
        return answerBox

    #Wrapper display function
    def display(self, useragent, *args, **kwargs):
        if useragent == ANDROID:
            self.displayAndroid()
        else:
            self.displayWindows(*args, **kwargs)
        
    
    #View the question and its result after doing it
    def view(self, parent):
        tk.Label(parent, text = "In each question, find the number that continues the series in the most sensible way and write it in the box", font=(FONT, 13, "bold", "underline")).pack(padx=5, pady=5)
        tk.Label(parent, text=", ".join([str(s) for s in self.sequence]), font=(FONT, 12, "bold")).pack(padx=5, pady=5)
        optionsFrame = tk.Frame(parent)
        for i in range(len(self.options)):
            tk.Label(optionsFrame, text=str(self.options[i]), font=(FONT, 12)).grid(row = 0, column = i, padx=5, pady=5)
        optionsFrame.pack(padx=5, pady=5)
        tk.Label(parent, text="Answer of '" + str(self.correctAnswer) + "' gives the sequence '" + ", ".join([str(s) for s in self.sequence] + [str(self.correctAnswer)]) + "'\nThe type of sequence is " + self.seqtype + ". This sequence is solved like this:\n" + self.typeExplaination ).pack(padx=5, pady=5)
        parent.pack()


#A question were the student must put the same letter to complete 2 words and start 2 others
class SameLetterFourWordsQuestion(Question):
    def __init__(self, minLength = 4, maxLength = 8):
        super().__init__()
        self.word1 = ""
        self.word2 = ""
        self.word3 = ""
        self.word4 = ""
        self.letter = ""
        self.type = "Same letter four words" #Title of the question
        self.timeToForm = 0
        self.generate(minLength, maxLength)

    #Generate the question
    def generate(self, minLength, maxLength):
        word1 = randomWord(minLength, maxLength) #Get the first word
        self.letter = word1[-1]
        regexStart = "^" + self.letter
        regexEnd = self.letter + "$"

        #Get the other 3 words by searching the word bank using regex
        word2 = randomWord(minLength, maxLength, format = regexStart, exclude=[word1])
        word3 = randomWord(minLength, maxLength, format = regexEnd, exclude=[word1, word2])
        word4 = randomWord(minLength, maxLength, format = regexStart, exclude=[word1, word2, word3])

        #Remove the correct letter
        self.word1 = word1[:-1]
        self.word2 = word2[1:]
        self.word3 = word3[:-1]
        self.word4 = word4[1:]

        #Set the answer
        self.correctAnswer = self.letter

    #Check if the answer was correct
    def verify(self, answer):
        if not super().verify(answer):
            return False
        #Check if the student got the answer the program found
        if self.correctAnswer == answer:
            return True
        if len(answer) != 1:
            return False

        #Check if the student could still be right
        word1 = self.word1 + answer
        word2 = answer + self.word2
        word3 = self.word3 + answer
        word4 = answer + self.word4
        if(word1 in words and word2 in words and word3 in words and word4 in words):
            self.correctAnswer=answer
            self.letter=self.correctAnswer
            return True
        return False

    #Display the question on windows
    def displayWindows(self, endFunction, parent, submitNow = True):
        tk.Label(parent, text = "In this question, the same letter must fit into both sets of brackets, to complete the word in front of the brackets and begin the word after the brackets.", font=(FONT, 13, "bold", "underline")).pack(padx=5, pady=5)
        tk.Label(parent, text=self.word1 + " [  ?  ] " + self.word2 + "    " + self.word3 + " [  ?  ] " + self.word4, font=(FONT, 12)).pack(padx=5, pady=5)
        #Answer box
        answerBox = tk.Entry(parent, font=(FONT, 12))
        answerBox.pack(padx=5, pady=5)
        submitButton = None
        #Show the result after marking
        def showResult():
            if answerBox.get() != "":
                self.correct = self.verify(answerBox.get())
                #Display the result
                if(self.correct):
                    tk.Label(parent, text="Correct!", font=(FONT, 12)).pack(padx=5, pady=5)
                else:
                    tk.Label(parent, text="Incorrect :( The right answer was: '" + self.letter + "'", font=(FONT, 12)).pack(padx=5, pady=5)
                letter = self.letter
                word1 = self.word1 + letter
                word2 = letter + self.word2
                word3 = self.word3 + letter
                word4 = letter + self.word4
                submitButton.destroy()
                endFunction(self, [word1, word2, word3, word4], self.type)
            
        #Create the submit button if the question is to be marked immediately after doing it
        if submitNow:
            submitButton = HoverButton(parent, text = "Submit", command=showResult, **self.submitButtonSettings)
            submitButton.pack(padx=5, pady=5)
        parent.pack()
        return answerBox

    #Wrapper display function
    def display(self, useragent, *args, **kwargs):
        if useragent == ANDROID:
            self.displayAndroid()
        else:
            self.displayWindows(*args, **kwargs)

    #View the question and its result after doing it
    def view(self, parent):
        tk.Label(parent, text = "In this question, the same letter must fit into both sets of brackets, to complete the word in front of the brackets and begin the word after the brackets.").pack(padx=5, pady=5)
        tk.Label(parent, text=self.word1 + " [  ?  ] " + self.word2 + "    " + self.word3 + " [  ?  ] " + self.word4).pack(padx=5, pady=5)
        word1 = self.word1 + self.letter
        word2 = self.letter + self.word2
        word3 = self.word3 + self.letter
        word4 = self.letter + self.word4
        tk.Label(parent, text="Answer of '" + self.correctAnswer + "' gives the words '" + word1 + "', '" + word2 + "', '" + word3 + "' and '" + word4 + "'").pack(padx=5, pady=5)
        parent.pack()

#Question where you have to find a word spread across 2 words in a sentence      
class WordInASentenceQuestion(Question):
    def __init__(self, minLength = 4, maxLength = 10):
        super().__init__()
        self.word = ""
        self.sentence = ""
        self.twoWords = ""
        self.options = []
        self.type = "Find a word in a sentence question" #Title of the question
        self.timeToForm = 1
        self.generate(minLength, maxLength)

    #Generate the question
    def generate(self, minLength, maxLength):
        while True:
            word = randomWord(minLength, maxLength) #Get a random word
            sentence = getRandomSentence(word, maxLength=10) #Get a sentence with that word in
            if sentence is None:
                continue
            sentenceWords = sentence.split() #Get each word in the sentence

            #Check if there are any words hidden in the sentence
            for i in range(len(sentenceWords) - 1):
                combinWord = sentenceWords[i] + sentenceWords[i+1]
                if len(combinWord) < minLength + 2:
                    continue
                for j in range(1, len(combinWord)):
                    for k in range(j, len(combinWord)):
                        if combinWord[j:k] in allwords and combinWord[j:k] not in sentenceWords[i] and combinWord[j:k] not in sentenceWords[i + 1] and len(combinWord[j:k]) >= minLength and len(combinWord[j:k]) <= maxLength:

                            #If a word is found, set the question and answer parameters
                            self.word = combinWord[j:k]
                            self.sentence = sentence[:1].upper() + sentence[1:] #Capitalise the sentence
                            self.twoWords = sentenceWords[i] + " " + sentenceWords[i+1]
                            self.correctAnswer=self.word

                            #Create options to select from
                            for l in range(len(sentenceWords) - 1):
                                self.options.append(sentenceWords[l] + " " + sentenceWords[l+1])
                            return None


    #Check if the answer was correct
    def verify(self, answer):
        if not super().verify(answer):
            return False
        
        #Check if the student got the program answer
        if answer == self.correctAnswer:
            return True
        if answer not in self.options:
            return False
        index = answer.find(" ")
        if index == -1:
            return False
        #Check if the student was still right
        combinWord = answer[:index] + answer[index + 1:]
        for i in range(1, len(combinWord)):
            for j in range(i, len(combinWord)):
                if combinWord[i:j] in words and combinWord[i:j] not in answer[:index] and combinWord not in answer[index + 1:]:
                    self.word = combinWord[i:j]
                    self.correctAnswer = answer
                    return True
        return False


    #Display the question on windows
    def displayWindows(self, endFunction, parent, submitNow = True):
        tk.Label(parent, text = "In these sentences, a word is hidden at the end of one word and the beginning of the next word.\nWrite the hidden word in the box below", font=(FONT, 13, "bold", "underline")).pack(padx=5, pady=5)
        tk.Label(parent, text=self.sentence, font=(FONT, 12)).pack(padx=5, pady=5)
        tk.Label(parent, text="Options:", font=(FONT, 12)).pack(padx=5, pady=5)
        optionsFrame = tk.Frame(parent)
        for i in range(len(self.options)):
            tk.Label(optionsFrame, text=self.options[i], font=(FONT, 12)).grid(row = 0, column = i, padx=5, pady=5)
        optionsFrame.pack(padx=5, pady=5)
        #Answer box
        answerBox = tk.Entry(parent, font=(FONT, 12))
        answerBox.pack(padx=5, pady=5)
        submitButton = None
        #Show the result after marking
        def showResult():
            if answerBox.get() != "":
                self.correct=self.verify(answerBox.get())
                #Display the result
                if(self.correct):
                    tk.Label(parent, text="Correct!", font=(FONT, 12)).pack(padx=5, pady=5)
                else:
                    tk.Label(parent, text="Incorrect :( The right answer was: '" + self.correctAnswer + "'", font=(FONT, 12)).pack(padx=5, pady=5)
                submitButton.destroy()
                endFunction(self, [self.word] + self.sentence.split(), self.type)
        #Create the submit button if the question is to be marked immediately after doing it
        if submitNow:
            submitButton = HoverButton(parent, text = "Submit", command=showResult, **self.submitButtonSettings)
            submitButton.pack(padx=5, pady=5)
        parent.pack()
        return answerBox

    #Wrapper display function
    def display(self, useragent, *args, **kwargs):
        if useragent == ANDROID:
            self.displayAndroid()
        else:
            self.displayWindows(*args, **kwargs)

    #View the question and its result after doing it
    def view(self, parent):
        tk.Label(parent, text = "In these sentences, a word is hidden at the end of one word and the beginning of the next word.\nWrite the hidden word in the box below", font=(FONT, 13, "bold", "underline")).pack(padx=5, pady=5)
        tk.Label(parent, text=self.sentence).pack(padx=5, pady=5)
        tk.Label(parent, text="Options:").pack(padx=5, pady=5)
        optionsFrame = tk.Frame(parent)
        for i in range(len(self.options)):
            tk.Label(optionsFrame, text=self.options[i]).grid(row = 0, column = i)
        optionsFrame.pack(padx=5, pady=5)
        tk.Label(parent, text="Answer is '" + self.correctAnswer + "' to make the word '" + self.word + "'").pack(padx=5, pady=5)
        parent.pack()

    


#Form a word by putting 2 together
class CompoundWordQuestion(Question):
    def __init__(self, minLength = 2, maxLength = 10):
        super().__init__()
        self.word1 = ""
        self.word2 = ""
        self.answer = ""
        self.options = [[], []]
        self.type = "Make one word from two question" #Title of the question
        self.timeToForm = 3 #The time taken for a question to be generated in seconds
        self.generate(minLength, maxLength)
    
    #Generate the question
    def generate(self, minLength, maxLength):
        w = wordDict
        while True:
            #Get two words which make one
            word1 = randomWord(minLength, maxLength)
            word2 = randomWord(minLength, maxLength, exclude=[word1])
            if w.get(word1 + word2) != None:
                self.word1 = word1
                self.word2 = word2
                self.options = [[word1], [word2]]
                break
            if w.get(word2 + word1) != None:
                self.word2 = word1
                self.word1 = word2
                self.options = [[word2], [word1]]
                break
        #Get the correct answer and options
        self.correctAnswer = self.word1 + self.word2
        for i in range(2):
            for j in range(2):
                self.options[i].append(randomWord(minLength, maxLength, exclude=self.options[0] + self.options[1]))
        random.shuffle(self.options[0])
        random.shuffle(self.options[1])

    #Check if the answer was correct
    def verify(self, answer):
        if not super().verify(answer):
            return False
        if answer == self.correctAnswer:
            return True

        #Check if the student was still right
        for word1 in self.options[0]:
            for word2 in self.options[1]:
                if word1 + word2 == answer:
                    self.word1 = word1
                    self.word2 = word2
                    self.correctAnswer=self.answer
                    return True
        return False


    #Display the question on windows
    def displayWindows(self, endFunction, parent, submitNow = True):
        tk.Label(parent, text = "In these questions, find two words, one from each group, that together make one correctly spelt word, without changing the order of the letters.\nThe word from the first group always comes first.\nWrite the word you make in the answer box", font=(FONT, 13, "bold", "underline")).pack(padx=5, pady=5)
        tk.Label(parent, text="Options:", font=(FONT, 12)).pack(padx=5, pady=5)
        optionsFrame = tk.Frame(parent)
        for i in range(2):
            for j in range(len(self.options[i])):
                tk.Label(optionsFrame, text=self.options[i][j], font=(FONT, 12)).grid(row = j, column = i)            
        optionsFrame.pack(padx=5, pady=5)
        #Answer box
        answerBox = tk.Entry(parent, font=(FONT, 12))
        answerBox.pack(padx=5, pady=5)
        submitButton = None
        #Show the result after marking
        def showResult():
            if answerBox.get() != "":
                self.correct=self.verify(answerBox.get())
                #Display the result
                if(self.correct):
                    tk.Label(parent, text="Correct!", font=(FONT, 12)).pack(padx=5, pady=5)
                else:
                    tk.Label(parent, text="Incorrect :( The right answer was: '" + self.correctAnswer + "'", font=(FONT, 12)).pack(padx=5, pady=5)
                submitButton.destroy()
                endFunction(self, [self.answer] + self.options[0] + self.options[1], self.type)
        submitButton = HoverButton(parent, text = "Submit", command=showResult, **self.submitButtonSettings)
        submitButton.pack(padx=5, pady=5)
        parent.pack()
        return answerBox
    
    #Wrapper display function
    def display(self, useragent, *args, **kwargs):
        if useragent == ANDROID:
            self.displayAndroid()
        else:
            self.displayWindows(*args, **kwargs)

    #View the question and its result after doing it
    def view(self, parent):
        tk.Label(parent, text = "In these questions, find two words, one from each group, that together make one correctly spelt word, without changing the order of the letters.\nThe word from the first group always comes first.\nWrite the word you make in the answer box").pack(padx=5, pady=5)
        tk.Label(parent, text="Options:").pack(padx=5, pady=5)
        optionsFrame = tk.Frame(parent)
        for i in range(2):
            for j in range(len(self.options[i])):
                tk.Label(optionsFrame, text=self.options[i][j]).grid(row = j, column = i)            
        optionsFrame.pack(padx=5, pady=5)
        tk.Label(parent, text="Answer is '" + self.word1 + " and " + self.word2 + "' to make the word '" + self.correctAnswer + "'").pack(padx=5, pady=5)
        parent.pack()


#Simple equation solving question
class AlgebraSubstitutionQuestion(Question):
    def __init__(self):
        super().__init__()
        self.numberMap = {}
        self.operations = [" + ", " * ", " / ", " - "]
        self.expression = ""
        self.answer = ""
        self.type = "Letter Calculations"
        self.timeToForm = 0
        self.generate()
    
    #Generate the question
    def generate(self):
        while True:
            numberMap = {}
            letters = ["A", "B", "C", "D", "E"] #Set the letters used to A-E
            numbers = []

            #Map each letter to a number
            for letter in letters:
                number = randomNumber(1, 100, exclude=[numbers])
                numberMap[number] = letter
                numbers.append(number)
            #Select the number of operators to have in the calculation
            operationNumber = randomNumber(3, 6)

            #Set up the operations check to make sure they don't cancel
            expression = ""
            usedoperations = []
            usednumbers = []
            used = {" + " : [False, False, False, False, False],
                   " * " : [False, False, False, False, False],
                   " - " : [False, False, False, False, False],
                   " / " : [False, False, False, False, False]}
            oppositeop = {" + ": " - ", " - ":" + ", " * ": " / ", " / " : " * "}
            complete = True
            prevOp = " + "

            #Formulate an expression
            for i in range(operationNumber):
                #Add the number
                letterIndex = random.randint(0,4)
                currentNumber = numbers[letterIndex]
                expression += str(currentNumber)
                usednumbers.append(currentNumber)

                #Form the operation
                currentoperation = self.operations[random.randint(0,3)]

                #Update the used dictionary
                if prevOp == " * " or prevOp == " / ":
                    used[prevOp][letterIndex] = True
                elif currentoperation == " * " or currentoperation == " / ":
                    used[" * "][letterIndex] = True
                else:
                    used[prevOp][letterIndex] = True

                

                
                #Check the operation
                if used[oppositeop[currentoperation]][letterIndex]:
                    complete = False
                    break
                if currentNumber == 1:
                    if prevOp == " * " or currentoperation == " * " or prevOp == " / ":
                        complete = False
                        break   
                #Add the operation
                if i != operationNumber - 1:
                    expression += currentoperation
                    usedoperations.append(currentoperation)
                
                #Set the previous operation
                prevOp = currentoperation

            if not complete:
                continue

            #Evaluate the expression
            result = eval(expression)
            if result in numbers:
                if result in usednumbers:
                    correctExpression = True
                    for number in usednumbers:
                        if number == result:
                            if occurences(result, usednumbers) % 2 != 0:
                                correctExpression = False
                                break
                        else:
                            if occurences(number, usednumbers) % 2 != 0:
                                break
                        correctExpression = False
                    if not correctExpression:
                        continue

                #Make the expression into a string
                expression = ""
                for i in range(operationNumber - 1):
                    expression += str(numberMap[usednumbers[i]])
                    expression += usedoperations[i]
                expression += str(numberMap[usednumbers[-1]])

                #Make the expression more readable
                str.replace(expression, "*", " x ")
                str.replace(expression, "/", "÷")
                self.expression = expression
                self.numberMap = numberMap
                self.correctAnswer = numberMap[result]
                if len(self.numberMap) == 5:
                    return 0
    
    
    #Check if the answer was correct
    def verify(self, answer):
        if not super().verify(answer):
            return False
        return answer.upper() == self.correctAnswer


    #Display the question on windows
    def displayWindows(self, endFunction, parent, submitNow = True):
        tk.Label(parent, text = "In these questions, letters stand for numbers.\nWork out the answer to each sum, then find its letter and write it in the box.", font=(FONT, 13, "underline", "bold")).pack(padx=5, pady=5)
        n = list(self.numberMap.keys())
        nm = self.numberMap
        text = ("If " +  nm[n[0]] + " = " +  str(n[0]) + " and " +
                  nm[n[1]] + " = " +  str(n[1]) + " and " +
                  nm[n[2]] + " = " +  str(n[2]) + " and " +
                  nm[n[3]] + " = " +  str(n[3]) + " and " +
                  nm[n[4]] + " = " +  str(n[4]) + "\nWhat is the answer to\n" + self.expression)
        tk.Label(parent, text=text, font=(FONT, 12)).pack(padx=5, pady=5)
        #Answer box
        answerBox = tk.Entry(parent, font=(FONT, 12))
        answerBox.pack(padx=5, pady=5)
        submitButton = None
        #Show the result after marking
        def showResult():
            if answerBox.get() != "":
                self.correct=self.verify(answerBox.get())
                #Display the result
                if(self.correct):
                    tk.Label(parent, text="Correct!", font=(FONT, 12)).pack(padx=5, pady=5)
                else:
                    tk.Label(parent, text="Incorrect :( The right answer was: '" + self.correctAnswer + "'", font=(FONT, 12)).pack(padx=5, pady=5)
                submitButton.destroy()
                endFunction(self, [], self.type)
        #Create the submit button if the question is to be marked immediately after doing it
        if submitNow:
            submitButton = HoverButton(parent, text = "Submit", command=showResult, **self.submitButtonSettings)
            submitButton.pack(padx=5, pady=5)
        parent.pack()
        return answerBox
    
    #Wrapper display function
    def display(self, useragent, *args, **kwargs):
        if useragent == ANDROID:
            self.displayAndroid()
        else:
            self.displayWindows(*args, **kwargs)

    #View the question and its result after doing it
    def view(self, parent):
        tk.Label(parent, text = "In these questions, letters stand for numbers.\nWork out the answer to each sum, then find its letter and write it in the box.").pack(padx=5, pady=5)
        n = list(self.numberMap.keys())
        nm = self.numberMap
        text = ("If " +  nm[n[0]] + " = " +  str(n[0]) + " and " +
                  nm[n[1]] + " = " +  str(n[1]) + " and " +
                  nm[n[2]] + " = " +  str(n[2]) + " and " +
                  nm[n[3]] + " = " +  str(n[3]) + " and " +
                  nm[n[4]] + " = " +  str(n[4]) + "\nWhat is the answer to\n" + self.expression)
        tk.Label(parent, text="Answer is '" + self.correctAnswer + "'").pack(padx=5, pady=5)
        parent.pack()



            
                
                


#Mix two words to form another, based on a mix defined in the question
class MixTheWordsInTheSameWayQuestion(Question):
    def __init__(self, minLength = 3, maxLength = 3):
        super().__init__()
        self.word1 = ""
        self.word2 = ""
        self.word12Combine = ""
        self.word3 = ""
        self.word4 = ""
        self.word34Combine = ""
        self.type = "Mix the words in the same way question"
        self.timeToForm = 0
        self.generate(minLength, maxLength)

    #Generate the question
    def generate(self, minLength, maxLength):
        while True:

            #Get two random words
            randomWord1 = randomWord(minLength, maxLength)
            randomWord2 = randomWord(len(randomWord1), len(randomWord1), exclude=[randomWord1])

            #Generate the length of the words to be formed
            firstWordLength = random.randint(4, 7)
            secondWordLength = random.randint(4, 7)
            numberinWord1 = random.randint(1, len(randomWord1) - 1)

            #Get a list of the letters to be made into a word
            listofletterpositions = [i for i in range(len(randomWord1))]
            random.shuffle(listofletterpositions)

            #Set up formatting for each word to a default a-z
            format1 = ["[a-z]" for i in range(firstWordLength)]
            format2 = ["[a-z]" for i in range(secondWordLength)]
            format3 = ["[a-z]" for i in range(firstWordLength)]
            format4 = ["[a-z]" for i in range(secondWordLength)]

            #Correct the format for letters already defined
            for i in range(numberinWord1):
                format1[listofletterpositions[i]] = randomWord1[listofletterpositions[i]]
                format3[listofletterpositions[i]] = randomWord2[listofletterpositions[i]]
            for i in range(numberinWord1, len(randomWord1)):
                format2[listofletterpositions[i]] = randomWord1[listofletterpositions[i]]
                format4[listofletterpositions[i]] = randomWord2[listofletterpositions[i]]
            format1 = "".join(format1)
            format2 = "".join(format2)
            format3 = "".join(format3)
            format4 = "".join(format4)

            #Generate 4 words following the format
            word1 = randomWord(firstWordLength, firstWordLength, format1, wordsList=words)
            if word1 != None:
                word2 = randomWord(secondWordLength, secondWordLength, format2, [word1], wordsList=words)
                if word2 != None:
                    word3 = randomWord(firstWordLength, firstWordLength, format3, [word1, word2], wordsList=words)
                    if word3 != None:
                        word4 = randomWord(secondWordLength, secondWordLength, format4, [word1, word2, word3], wordsList=words)
                        if word4 != None:
                            #If 4 words can be found set them as the answers
                            self.word1 = word1
                            self.word2 = word2
                            self.word3 = word3
                            self.word4 = word4
                            self.word12Combine = randomWord1
                            self.word34Combine = randomWord2
                            self.correctAnswer = randomWord2
                            return 0



    
    #Check if the answer was correct
    def verify(self, answer):
        if not super().verify(answer):
            return False
        if self.correctAnswer == answer:
            return True

        #Check if the student could still be right
        positions = {}
        for letter in self.word12Combine:
            positions[letter] = []
            for pos in findall(self.word1, letter):
                positions[letter].append((pos, 1))
            for pos in findall(self.word2, letter):
                positions[letter].append((pos, 2))
        
        #Recursively find all the possible combinations of the letters over the words
        def formulateCombinations(currentLetter, possibleCombinations):
            if currentLetter != len(self.word12Combine):
                newPossibleCombinations = []
                for i in range(len(possibleCombinations)):
                    for pos in positions[self.word12Combine[currentLetter]]:
                        if pos not in possibleCombinations[i]:
                            newPossibleCombinations.append([pos] + possibleCombinations[i])
                return formulateCombinations(currentLetter + 1, newPossibleCombinations)
            else:
                return possibleCombinations
        

        possibleCombinations = formulateCombinations(0, [[]])
        possibleWords = []
        for combination in possibleCombinations:
            possibleWord = ""
            for pos in combination:
                if pos[1] == 1:
                    possibleWord += self.word3[pos[0]]
                else:
                    possibleWord += self.word4[pos[0]]
            possibleWords.append(possibleWord)

        actualWords = []
        for word in possibleWords:
            if word in words:
                actualWords.append(word)
        
        
        #Check if the word entered is a possible solution
        if answer in actualWords:
            self.correctAnswer=answer
            return True
        else:
            return False


    #Display the question on windows
    def displayWindows(self, endFunction, parent, submitNow = True):
        tk.Label(parent, text = "In these questions, the three words in the second group should go together in the same way as the three in the first group.", font=(FONT, 13, "underline", "bold")).pack(padx=5, pady=5)
        tk.Label(parent, text=self.word1 + " [" + self.word12Combine + "] " + self.word2 + "    " + self.word3 + " [  ?  ] " + self.word4, font=(FONT, 12)).pack(padx=5, pady=5)
        #Answer box
        answerBox = tk.Entry(parent, font=(FONT, 12))
        answerBox.pack(padx=5, pady=5)
        submitButton = None
        #Show the result after marking
        def showResult():
            if answerBox.get() != "":
                self.correct=self.verify(answerBox.get())
                #Display the result
                if(self.correct):
                    tk.Label(parent, text="Correct!", font=(FONT, 12)).pack(padx=5, pady=5)
                    self.letter = self.answer
                else:
                    tk.Label(parent, text="Incorrect :( The right answer was: '" + self.correctAnswer + "'", font=(FONT, 12)).pack(padx=5, pady=5)
                submitButton.destroy()
                endFunction(self, [self.word1, self.word12Combine, self.word2, self.word3, self.word34Combine, self.word4], self.type)

            
        #Create the submit button if the question is to be marked immediately after doing it
        if submitNow:
            submitButton = HoverButton(parent, text = "Submit", command=showResult, **self.submitButtonSettings)
            submitButton.pack(padx=5, pady=5)
        parent.pack()
        return answerBox
    
    #Wrapper display function
    def display(self, useragent, *args, **kwargs):
        if useragent == ANDROID:
            self.displayAndroid()
        else:
            self.displayWindows(*args, **kwargs)

    #View the question and its result after doing it
    def view(self, parent):
        tk.Label(parent, text = "In these questions, the three words in the second group should go together in the same way as the three in the first group.").pack(padx=5, pady=5)
        tk.Label(parent, text=self.word1 + " [" + self.word12Combine + "] " + self.word2 + "    " + self.word3 + " [  ?  ] " + self.word4).pack(padx=5, pady=5)
        tk.Label(parent, text="Answer is '" + self.correctAnswer + "'").pack(padx=5, pady=5)
        parent.pack()

#Add a 3 letter word into a part word in order to make a sentence make sense
class ThreeLetterWordCompletesSentenceQuestion(Question):
    def __init__(self, minLength = 5, maxLength = 10):
        super().__init__()
        self.sentence = ""
        self.wordIn = ""
        self.fullWord = ""
        self.withRemoved = ""
        self.type = "One word in another sentences"
        self.options = []
        self.timeToForm = 0
        self.generate(minLength, maxLength)

    #Generate the question
    def generate(self, minLength, maxLength):
        while True:
            fullWord = randomWord(5, maxLength) #Get the full word
            halfWord = None
            withRemoved = None

            #Generate a half word
            for i in range(1, len(fullWord) - 3):
                if fullWord[i:i+3] in words:
                    halfWord = fullWord[i:i+3]
                    withRemoved = fullWord[:i] + fullWord[i+3:]
                    break
            if halfWord is None:
                continue

            #Get a sentence with the full word in
            sentence = getRandomSentence(fullWord, minLength = 4)
            if sentence is None:
                continue

            #Check the word, rather than a derivative, is in the sentence
            index = sentence.find(fullWord)
            if index == -1:
                continue

            #Capitalise the first word in the sentence
            if index != 0:
                sentence = sentence[:1].upper() + sentence[1:]
            endWord = sentence.find(" ", index + 1)

            #Remove the 3 letters from the word in the sentence
            startWord = sentence.rfind(" ", 0, index)
            if startWord == -1:
                startWord = 0
            if endWord == -1:
                fullWord = sentence[startWord:]
            else:
                fullWord = sentence[startWord:endWord]
            sentence = sentence[:startWord] + " " + withRemoved.upper() + sentence[startWord + len(fullWord):]
            break
        #Set the correct answer and options
        self.withRemoved = withRemoved
        self.fullWord = fullWord
        self.wordIn = halfWord
        self.correctAnswer = self.wordIn
        self.sentence = sentence
        self.options = [self.wordIn]
        for i in range(4):
            self.options.append(randomWord(3,3, exclude = self.options))
        random.shuffle(self.options)

    #Check if the answer was correct
    def verify(self, answer):
        if not super().verify(answer):
            return False
        if answer == self.correctAnswer:
            return True
        if len(answer) != 3:
            return False
        if answer not in self.options:
            return False
        substring = ""
        for i in range(1, len(self.withRemoved) - 1):
            newWord = self.withRemoved[:i] + answer + self.withRemoved[i:]
            if newWord in words:
                self.correctAnswer=answer
                self.fullWord=newWord
                return True
        return False


    #Display the question on windows
    def displayWindows(self, endFunction, parent, submitNow = True):
        tk.Label(parent, text = "In these sentences, the word in capitals has had three letters next to each other taken out.\nThese three letters will make one correctly-spelt word without changing their order.\nThe sentence that you make must make sense.", font=(FONT, 13, "underline", "bold")).pack(padx=5, pady=5)
        tk.Label(parent, text=self.sentence, font=(FONT, 12)).pack(padx=5, pady=5)
        tk.Label(parent, text="Options:", font=(FONT, 12)).pack(padx=5, pady=5)
        optionsFrame = tk.Frame(parent)
        for i in range(5):
            tk.Label(optionsFrame, text=self.options[i], font=(FONT, 12)).grid(row = 0, column = i)
        optionsFrame.pack(padx=5, pady=5)
        #Answer box
        answerBox = tk.Entry(parent, font=(FONT, 12))
        answerBox.pack(padx=5, pady=5)
        submitButton = None
        #Show the result after marking
        def showResult():
            if answerBox.get() != "":
                self.correct=self.verify(answerBox.get())
                #Display the result
                if(self.correct):
                    tk.Label(parent, text="Correct!", font=(FONT, 12)).pack(padx=5, pady=5)
                    self.answer = self.wordIn
                else:
                    tk.Label(parent, text="Incorrect :( The right answer was: '" + self.correctAnswer + "'", font=(FONT, 12)).pack(padx=5, pady=5)
                submitButton.destroy()
                endFunction(self, [self.fullWord] + self.options, self.type)

            
        #Create the submit button if the question is to be marked immediately after doing it
        if submitNow:
            submitButton = HoverButton(parent, text = "Submit", command=showResult, **self.submitButtonSettings)
            submitButton.pack(padx=5, pady=5)
        parent.pack()
        return answerBox

    #Wrapper display function
    def display(self, useragent, *args, **kwargs):
        if useragent == ANDROID:
            self.displayAndroid()
        else:
            self.displayWindows(*args, **kwargs)    

    #View the question and its result after doing it
    def view(self, parent):
        tk.Label(parent, text = "In these sentences, the word in capitals has had three letters next to each other taken out.\nThese three letters will make one correctly-spelt word without changing their order.\nThe sentence that you make must make sense.").pack(padx=5, pady=5)
        tk.Label(parent, text=self.sentence).pack(padx=5, pady=5)
        tk.Label(parent, text="Options:").pack(padx=5, pady=5)
        optionsFrame = tk.Frame(parent)
        for i in range(5):
            tk.Label(optionsFrame, text=self.options[i]).grid(row = 0, column = i)
        optionsFrame.pack(padx=5, pady=5)
        tk.Label(parent, text="Answer is '" + self.correctAnswer + "' to make the word '" + self.fullWord + "'").pack(padx=5, pady=5)
        parent.pack()

    


#Find antonyms from a group of words
class MostOppositeInMeaningWordsQuestion(Question):
    def __init__(self, minLength = 3, maxLength = 10):
        super().__init__()
        self.group1 = []
        self.group2 = []
        self.answer1 = ""
        self.answer2 = ""
        self.correctanswer1 = ""
        self.correctanswer2 = ""
        self.type = "Find the opposite" #Title of the question
        self.timeToForm = 1
        self.generate(minLength, maxLength)

    #Generate the question
    def generate(self, minLength, maxLength):
        while True:

            #Get an adjective
            answer1 = randomWord(minLength, maxLength)
            while not wordData.isAdjective(answer1):
                answer1 = randomWord(minLength, maxLength)

            #Get a list of antonyms
            antonyms = wordData.antonym(answer1)
            if antonyms is None:
                continue

            #Get the correct antonym from the list
            random.shuffle(antonyms)
            answer2 = None
            for antonym in antonyms:
                x = wordData.antonym(antonym)
                if x is not None:
                    if answer1 not in x:
                        continue
                    else:
                        answer2 = antonym
                        break
                else:
                    continue
            if answer2 is None:
                continue


            
            #Get a list of other plausible options
            synonyms1 = wordData.synonym(answer1)
            synonyms2 = wordData.synonym(answer2)
            synonyms1Ex = []
            synonyms2Ex = []

            for syn in synonyms1:
                x = wordData.synonym(syn)
                if x is not None:
                    synonyms1Ex += x
            for syn in synonyms2:
                x = wordData.synonym(syn)
                if x is not None:
                    synonyms2Ex += x
            
            random.shuffle(synonyms1Ex)
            random.shuffle(synonyms2Ex)
            word1 = None
            word2 = None

            #Perform a closeness check between words in options list 1
            for syn1 in synonyms1Ex:
                max, min, av = getRelation(answer1, syn1)
                if max >= 0.2 and max <= 0.8:
                    if word1 is None:
                        word1 = syn1
                    else:
                        word2 = syn1
                        break
            if word1 is None or word2 is None:
                continue
            self.group1 = [word1, word2, answer1]
            word1 = None
            word2 = None

            #Perform a closeness check between words in options list 2
            for syn2 in synonyms2Ex:
                max, min, av = getRelation(answer2, syn2)
                if max >= 0.2 and max <= 0.8:
                    if word1 is None:
                        word1 = syn2
                    else:
                        word2 = syn2
                        break
            if word1 is None or word2 is None:
                continue

            #Set the options
            self.group2 = [word1, word2, answer2]
            cont = False
            for word in self.group1:
                if word in self.group2:
                    cont = True
            x = self.group1 + self.group2
            for word in x:
                if occurences(word, x) > 1:
                    cont = True
            if cont:
                continue
            break

        #Set the correct answers
        self.correctanswer1 = answer1
        self.correctanswer2 = answer2
        random.shuffle(self.group1)
        random.shuffle(self.group2)
            


                






    #Check if the answer was correct
    def verify(self, answer):
        answer = answer.replace(" ", "")
        answer = answer.split(";")
        if len(answer) != 2:
            return False
        answer1 = answer[0]
        answer2 = answer[1]
        self.answer1 = answer1
        self.answer2 = answer2
        try:
            x = answer1 in wordData.antonym(answer2)
        except:
            x = False
        try:
            y = answer2 in wordData.antonym(answer1)
        except:
            y = False    
        return x or y
    
 
    #Display the question on windows
    def displayWindows(self, endFunction, parent, submitNow = True):
        tk.Label(parent, text = "In these questions, find two words, one from each group, that are most opposite in meaning. Write the two words separated by a semicolon (;) in the box", font=(FONT, 13, "underline", "bold")).pack(padx=5, pady=5)
        wordFrame = tk.Frame(parent)
        count = 0
        for word in self.group1:
            tk.Label(wordFrame, text=word, font=(FONT, 12)).grid(row = count, column = 0, padx=5, pady = 5)
            count += 1
        count = 0
        for word in self.group2:
            tk.Label(wordFrame, text=word, font=(FONT, 12)).grid(row = count, column = 1, padx=5, pady=5)
            count += 1
        wordFrame.pack(padx=5, pady=5)
        submitButton = None
        #Answer box
        answerBox = tk.Entry(wordFrame, font=(FONT, 12))
        answerBox.grid(row = count, column = 0, columnspan=2, padx=5, pady=5)

        #Show the result after marking
        def showResult():
            if answerBox.get() != "":
                self.correct=self.verify(answerBox.get())
                #Display the result
                if(self.correct):
                    tk.Label(parent, text="Correct!", font=(FONT, 12)).pack(padx=5, pady=5)
                else:
                    tk.Label(parent, text="Incorrect :( The right answers were: '" + self.correctanswer1 + "' and '" + self. correctanswer2 + "'", font=(FONT, 12)).pack(padx=5, pady=5)
                submitButton.destroy()
                endFunction(self, self.group1 + self.group2, self.type)
                
        #Create the submit button if the question is to be marked immediately after doing it
        if submitNow:
                submitButton = HoverButton(parent, text = "Submit", command=showResult, **self.submitButtonSettings)
                submitButton.pack(padx=5, pady=5)
        parent.pack()
        return answerBox

    #Wrapper display function
    def display(self, useragent, *args, **kwargs):
        if useragent == ANDROID:
            self.displayAndroid()
        else:
            self.displayWindows(*args, **kwargs)

    #View the question and its result after doing it
    def view(self, parent):
        tk.Label(parent, text = "In these questions, find two words, one from each group, that are most opposite in meaning.").pack(padx=5, pady=5)
        wordFrame = tk.Frame(parent)
        count = 0
        for word in self.group1:
            tk.Label(wordFrame, text=word).grid(row = count, column = 0)
            count += 1
        count = 0
        for word in self.group2:
            tk.Label(wordFrame, text=word).grid(row = count, column = 1)
            count += 1
        wordFrame.pack(padx=5, pady=5)
        tk.Label(parent, text="Answer was '" + self.correctanswer1 + "' and '" + self.correctanswer2 + "'").pack(padx=5, pady=5)
        parent.pack()


#Find synonyms from a group of words
class MostNearInMeaningWordsQuestion(Question):
    def __init__(self, minLength = 3, maxLength = 10):
        super().__init__()
        self.group1 = []
        self.group2 = []
        self.answer1 = ""
        self.answer2 = ""
        self.correctanswer1 = ""
        self.correctanswer2 = ""
        self.type = "Find the synonym" #Title of the question
        self.timeToForm = 1
        self.generate(minLength, maxLength)


    #Generate the question
    def generate(self, minLength, maxLength):
        wordList1 = []
        wordList2 = []
        while True:

            #Generate an adjective
            answer1 = randomWord(minLength, maxLength)
            while not wordData.isAdjective(answer1):
                answer1 = randomWord(minLength, maxLength)

            #Get synonyms of the adjective
            synonyms = wordData.synonym(answer1)
            if synonyms is None:
                continue
            random.shuffle(synonyms)
            answer2 = None
            for synonym in synonyms:
                x = wordData.synonym(synonym)
                if x is not None:
                    if answer1 not in x:
                        continue
                    else:
                        answer2 = synonym
                        break
                else:
                    continue
            if answer2 is None:
                continue


            
            #Get a list of other plausible options
            synonyms1 = wordData.synonym(answer1)
            synonyms2 = wordData.synonym(answer2)
            synonyms1Ex = []
            synonyms2Ex = []

            for syn in synonyms1:
                x = wordData.synonym(syn)
                if x is not None:
                    synonyms1Ex += x
            for syn in synonyms2:
                x = wordData.synonym(syn)
                if x is not None:
                    synonyms2Ex += x
            
            random.shuffle(synonyms1Ex)
            random.shuffle(synonyms2Ex)
            word1 = None
            word2 = None

            #Perform a closeness check between words in options list 1
            for syn1 in synonyms1Ex:
                max, min, av = getRelation(answer1, syn1)
                if max >= 0.2 and max <= 0.8:
                    if word1 is None:
                        word1 = syn1
                    else:
                        word2 = syn1
                        break
            if word1 is None or word2 is None:
                continue
            self.group1 = [word1, word2, answer1]
            word1 = None
            word2 = None

            #Perform a closeness check between words in options list 2
            for syn2 in synonyms2Ex:
                max, min, av = getRelation(answer2, syn2)
                if max >= 0.2 and max <= 0.8:
                    if word1 is None:
                        word1 = syn2
                    else:
                        word2 = syn2
                        break
            if word1 is None or word2 is None:
                continue
        
            #Set the groups
            self.group2 = [word1, word2, answer2]
            cont = False
            for word in self.group1:
                if word in self.group2:
                    cont = True
            x = self.group1 + self.group2
            for word in x:
                if occurences(word, x) > 1:
                    cont = True
            if cont:
                continue
            break

        #Set the correct answers
        self.correctanswer1 = answer1
        self.correctanswer2 = answer2
        random.shuffle(self.group1)
        random.shuffle(self.group2)
            
            


                






    #Check if the answer was correct
    def verify(self, answer):
        answer = answer.replace(" ", "")
        answer = answer.split(";")
        if len(answer) != 2:
            return False
        answer1 = answer[0]
        answer2 = answer[1]
        self.answer1 = answer1
        self.answer2 = answer2
        try:
            x = answer1 in wordData.synonym(answer2)
        except:
            x = False
        try:
            y = answer2 in wordData.synonym(answer1)
        except:
            y = False    
        return x or y
    
 
    #Display the question on windows
    def displayWindows(self, endFunction, parent, submitNow = True):
        tk.Label(parent, text = "In these questions, find two words, one from each group, that are most similar in meaning. Write the two words separated by a semicolon (;) in the box", font=(FONT, 13, "underline", "bold")).pack(padx=5, pady=5)
        wordFrame = tk.Frame(parent)
        count = 0
        for word in self.group1:
            tk.Label(wordFrame, text=word, font=(FONT, 12)).grid(row = count, column = 0, padx=5, pady = 5)
            count += 1
        count = 0
        for word in self.group2:
            tk.Label(wordFrame, text=word, font=(FONT, 12)).grid(row = count, column = 1, padx=5, pady=5)
            count += 1
        wordFrame.pack(padx=5, pady=5)
        submitButton = None
        #Answer box
        answerBox = tk.Entry(wordFrame, font=(FONT, 12))
        answerBox.grid(row = count, column = 0, columnspan=2, padx=5, pady=5)

        #Show the result after marking
        def showResult():
            if answerBox.get() != "":
                self.correct=self.verify(answerBox.get())
                #Display the result
                if(self.correct):
                    tk.Label(parent, text="Correct!", font=(FONT, 12)).pack(padx=5, pady=5)
                else:
                    tk.Label(parent, text="Incorrect :( The right answers were: '" + self.correctanswer1 + "' and '" + self. correctanswer2 + "'", font=(FONT, 12)).pack(padx=5, pady=5)
                submitButton.destroy()
                endFunction(self, self.group1 + self.group2, self.type)
            
        #Create the submit button if the question is to be marked immediately after doing it
        if submitNow:
            submitButton = HoverButton(parent, text = "Submit", command=showResult, **self.submitButtonSettings)
            submitButton.pack(padx=5, pady=5)
        parent.pack()
        return answerBox

    #Wrapper display function
    def display(self, useragent, *args, **kwargs):
        if useragent == ANDROID:
            self.displayAndroid()
        else:
            self.displayWindows(*args, **kwargs)

    #View the question and its result after doing it
    def view(self, parent):
        tk.Label(parent, text = "In these questions, find two words, one from each group, that are most similar in meaning.").pack(padx=5, pady=5)
        wordFrame = tk.Frame(parent)
        count = 0
        for word in self.group1:
            tk.Label(wordFrame, text=word).grid(row = count, column = 0)
            count += 1
        count = 0
        for word in self.group2:
            tk.Label(wordFrame, text=word).grid(row = count, column = 1)
            count += 1
        wordFrame.pack(padx=5, pady=5)
        tk.Label(parent, text="Answer was '" + self.correctanswer1 + "' and '" + self.correctanswer2 + "'").pack(padx=5, pady=5)
        parent.pack()


#Move one letter from a word to another word to form a third new word
class SwitchTheLetterQuestion(Question):
    def __init__(self, minLength = 4, maxLength = 8):
        super().__init__()
        self.word1 = ""
        self.word2 = ""
        self.newWord1 = ""
        self.newWord2 = ""
        self.switchletter = ""
        self.timeToForm = 0
        self.type = "Switch the letter" #Title of the question
        self.generate(minLength, maxLength)

    #Generate the question
    def generate(self, minLength, maxLength):
        generated = False
        w = wordDict
        while not generated:
            #Generate 2 words
            firstWord = randomWord(minLength, maxLength)
            secondWord = randomWord(len(firstWord) - 1, len(firstWord) - 1, exclude=[firstWord])

            #Check if a letter can be moved from the first word to the second to form a new word
            for i in range(len(firstWord)):
                letter = firstWord[i]
                for j in range(0, len(secondWord) - 1):
                    if(w.get(insert(secondWord, letter, j)) != None and w.get(pop(firstWord, i))!=None):
                        self.word1 = firstWord
                        self.word2 = secondWord
                        self.switchletter = letter
                        self.newWord1 = pop(firstWord, i)
                        self.newWord2 = insert(secondWord, letter, j)
                        generated = True
                        break

        #Set the correct answer
        self.correctAnswer = self.switchletter
    
    #Check if the answer was correct
    def verify(self, answer):
        if not super().verify(answer):
            return False
        if answer == self.correctAnswer:
            return True
        if answer == "":
            return False
        for j in [m.start() for m in re.finditer(answer, self.word1)]:
            if pop(self.word1, j,) in words:
                for i in range(0, len(self.word2) + 1):
                    if(insert(self.word2, answer, i) in words):
                        self.newWord1 = pop(self.word1, j)
                        self.newWord2 = insert(self.word2, answer, i)
                        self.switchletter = answer
                        self.correctAnswer = answer
                        return True
        return False


    #Display the question on windows
    def displayWindows(self, endFunction, parent, submitNow = True):
        tk.Label(parent, text = "In this question, one letter can be moved from the first word to the second word to make two new words.", font=(FONT, 13, "underline", "bold")).pack(padx=5, pady=5)
        tk.Label(parent, text=self.word1 + "    " + self.word2, font=(FONT, 12)).pack(padx=5, pady=5)
        #Answer box
        answerBox = tk.Entry(parent, font=(FONT, 12))
        answerBox.pack(padx=5, pady=5)
        submitButton = None
        #Show the result after marking
        def showResult():
            if answerBox.get() != "":
                self.correct = self.verify(answerBox.get())
                #Display the result
                if(self.correct):
                        tk.Label(parent, text="Correct!", font=(FONT, 12)).pack(padx=5, pady=5)
                else:
                    tk.Label(parent, text="Incorrect :( The right answer was: '" + self.correctAnswer + "'", font=(FONT, 12)).pack(padx=5, pady=5)
                submitButton.destroy()
                endFunction(self, [self.word1, self.newWord1, self.word2, self.newWord2], self.type)
                
        #Create the submit button if the question is to be marked immediately after doing it
        if submitNow:
                submitButton = HoverButton(parent, text = "Submit", command=showResult, **self.submitButtonSettings)
                submitButton.pack(padx=5, pady=5)
        parent.pack()
        return answerBox

    #Wrapper display function
    def display(self, useragent, *args, **kwargs):
        if useragent == ANDROID:
            self.displayAndroid()
        else:
            self.displayWindows(*args, **kwargs)

    #View the question and its result after doing it
    def view(self, parent):
        tk.Label(parent, text = "In this question, one letter can be moved from the first word to the second word to make two new words.").pack(padx=5, pady=5)
        tk.Label(parent, text=self.word1 + "    " + self.word2).pack(padx=5, pady=5)
        tk.Label(parent, text="Answer of '" + self.correctAnswer + "' gives the words '" + self.newWord1 + "' and '" + self.newWord2 + "'").pack(padx=5, pady=5)
        parent.pack()


#Complete a sum to make it hold true
class SumQuestion(Question):
    def __init__(self):
        super().__init__()
        self.lhs = ""
        self.rhs = ""
        self.lrhsanswer = 0
        self.correctAnswer = 0
        self.timeToForm = 0
        self.type = "Complete the calculation" #Title of the question
        self.generate(1, 50)


    #Generate the question
    def generate(self, min, max):
        while True:
            rhs = "" #The right hand side of the equation
            questionRhs = "" #The displayed right hand side
            lhs = "" #The left hand side of the equation
            signs = ["*", "+", "-", "/"]

            #Determine a number of numbers to have on the left and right of the calculation
            numberOnLhs = random.randint(2, 4)
            numberOnRhs = random.randint(2, 4)

            #Form the left hand side
            for i in range(numberOnLhs - 1):
                random.shuffle(signs)
                x = random.randint(min, max) #random number x
                sign = signs[0]
                lhs += str(x) + " "
                lhs += sign + " "
                if lhs.find(str(x) + "/" + str(x)) != -1 or lhs.find(str(x) + "-" + str(x)) != -1:
                    continue
            lhs += str(random.randint(min, max))
            if lhs.find(str(x) + "/" + str(x)) != -1 or lhs.find(str(x) + "-" + str(x)) != -1 or lhs.find("1 x") != -1 or lhs.find("x 1") != -1:
                    continue

            #Form the right hand side
            for i in range(numberOnRhs - 1):
                random.shuffle(signs)
                x = random.randint(min, max)
                sign = signs[0]
                rhs += str(x) + " "
                rhs += sign + " "
                if rhs.find(str(x) + "/" + str(x)) != -1 or rhs.find(str(x) + "-" + str(x)) != -1:
                    continue

            #Set the right hand side to be displayed in the question
            questionRhs = rhs + "[?]"

            #Get a random answer
            finalNumber = random.randint(min, max)
            rhs += str(finalNumber)
            if rhs.find(str(x) + "/" + str(x)) != -1 or rhs.find(str(x) + "-" + str(x)) != -1  or rhs.find("1 x") != -1 or rhs.find("x 1") != -1:
                    continue
            if rhs == lhs:
                continue

            #Check if the randomly formed equation holds true
            x = eval(rhs)
            y = eval(lhs)
            if x == y:

                #Clean up the equations and set answers
                self.lhs = lhs.replace("/", "÷").replace("*", "x")
                self.rhs = questionRhs.replace("/", "÷").replace("*", "x")
                self.lrhsanswer = x
                self.correctAnswer = finalNumber
                break

    #Check if the answer was correct
    def verify(self, answer):
        if not super().verify(answer):
            return False
        return(answer == str(self.correctAnswer))


    #Display the question on windows
    def displayWindows(self, endFunction, parent, submitNow = True):
        tk.Label(parent, text = "In each question, find the number that will complete the sum correctly and write it in the box.", font=(FONT, 13, "underline", "bold")).pack(padx=5, pady=5)
        tk.Label(parent, text=self.lhs + " = " + self.rhs, font=(FONT, 12)).pack(padx=5, pady=5)
        #Answer box
        answerBox = tk.Entry(parent, font=(FONT, 12))
        answerBox.pack(padx=5, pady=5)
        submitButton = None
        #Show the result after marking
        def showResult():
            if answerBox.get() != "":
                self.correct = self.verify(answerBox.get())

                #Display the result
                if(self.correct):
                    tk.Label(parent, text="Correct!", font=(FONT, 12)).pack(padx=5, pady=5)
                else:
                    tk.Label(parent, text="Incorrect :( The right answer was: '" + str(self.correctAnswer) + "'", font=(FONT, 12)).pack(padx=5, pady=5)
                submitButton.destroy()
                endFunction(self, [], self.type)
                
            #Create the submit button if the question is to be marked immediately after doing it
        if submitNow:
            submitButton = HoverButton(parent, text = "Submit", command=showResult, **self.submitButtonSettings)
            submitButton.pack(padx=5, pady=5)
        parent.pack()
        return answerBox

    #Wrapper display function
    def display(self, useragent, *args, **kwargs):
        if useragent == ANDROID:
            self.displayAndroid()
        else:
            self.displayWindows(*args, **kwargs)

    #View the question and its result after doing it
    def view(self, parent):
        tk.Label(parent, text = "In each question, find the number that will complete the sum correctly and write it in the box.", font=(FONT, 13, "underline", "bold")).pack(padx=5, pady=5)
        tk.Label(parent, text=self.lhs + " = " + self.rhs, font=(FONT, 12)).pack(padx=5, pady=5)
        tk.Label(parent, text="Answer of '" + str(self.correctAnswer) + "' makes both sides equal to " + str(self.lrhsanswer)).pack(padx=5, pady=5)
        parent.pack()


########################################################DEVELOPMENT#####################################################

#Code between letters and numbers [IN DEVELOPMENT]
class CodeWordQuestion(Question):
    def __init__(self):
        self.originalWords = []
        self.originalCodes = []
        self.questionCodes = []
        self.correctAnswers = []
        self.generate()

    #Generate the question
    def generate(self):
        return super().generate()

    #Check if the answer was correct
    def verify(self, answers):
        super().verify(answers)
        verification = []
        for i in range(len(answers)):
            verification.append(answers[i] == self.correctAnswers[i])
        return

    #Wrapper display function
    def display(self, endFunction, parent, submitNow = True):
        tk.Label(parent, text = "[EXPLANATION HERE]", font=(FONT, 13, "underline", "bold")).pack(padx=5, pady=5)
        tk.Label(parent, text="[QUESTION HERE]", font=(FONT, 12)).pack(padx=5, pady=5)
        #Answer box
        answerBox = tk.Entry(parent, font=(FONT, 12))
        answerBox.pack(padx=5, pady=5)
        submitButton = None
        #Show the result after marking
        def showResult():
            if answerBox.get() != "":
                self.correct = self.verify(answerBox.get())

                #Display the result
                if(self.correct):
                        tk.Label(parent, text="Correct!", font=(FONT, 12)).pack(padx=5, pady=5)
                else:
                    tk.Label(parent, text="Incorrect :( The right answer was: '" + str(self.correctAnswer) + "'", font=(FONT, 12)).pack(padx=5, pady=5)
                submitButton.destroy()
                endFunction(self, [], self.type)
                
            #Create the submit button if the question is to be marked immediately after doing it
        if submitNow:
            submitButton = HoverButton(parent, text = "Submit", command=showResult, **self.submitButtonSettings)
            submitButton.pack(padx=5, pady=5)
        parent.pack()
        return answerBox

    
