import threading
import collections
from math import exp
from os import startfile

from PIL import ImageTk ,Image
from sys import maxsize
from tkinter import Button, Widget, font
from tkinter.constants import BOTTOM, W
import time
import tkinter.ttk as ttk
import tkinter as tk
import random
import re
from typing import Sized
from PyDictionary import PyDictionary
import datetime
import os.path
import operator

from nltk.corpus.reader import toolbox
from sequenceGenerator import SequenceGenerator
from UserData import UserData
from Question import *
from tkExtensions import *
import sys
from constants import *
from Test import *
from wordData import *
try:
    wordData = loadWordData()
    setWordData(wordData)
except Exception as e:
    print(e)
    raise FileNotFoundError("No word data found, please redownload program files")




USERAGENT = WINDOWS #Set the user agent

#Different types of question
QuestionTypes = {"Same letter four words" : SameLetterFourWordsQuestion,
                 "Switch the letter" : SwitchTheLetterQuestion,
                 "Mix the words in the same way question" : MixTheWordsInTheSameWayQuestion, 
                 "Find the opposite" : MostOppositeInMeaningWordsQuestion, 
                 "Find the synonym" : MostNearInMeaningWordsQuestion,
                 "Complete the sequence":SequenceQuestion,
                 "One word in another sentences" : ThreeLetterWordCompletesSentenceQuestion, 
                 "Find a word in a sentence question": WordInASentenceQuestion,
                 "Make one word from two question": CompoundWordQuestion,
                 "Letter Calculations" : AlgebraSubstitutionQuestion,
                 "Complete the calculation":SumQuestion}
 
#Map of how long it takes to generate each question
timeToForm = {"Same letter four words" : 0.01,
                 "Switch the letter" : 0.01,
                 "Mix the words in the same way question" : 0.01, 
                 "Find the opposite" : 0.3, 
                 "Find the synonym" : 0.3,
                 "Complete the sequence":0.01,
                 "One word in another sentences" : 0.01, 
                 "Find a word in a sentence question": 0.9,
                 "Make one word from two question": 2.8,
                 "Letter Calculations" : 1,
                 "Complete the calculation":0.1}



#Format a date
def dateFormat(date):
    date = str(date)
    return date[8:] + "/" + date[5:7] + "/" + date[:4]    

        
#Get the number of seconds in an HH:mm:ss time
def secs(time):
    return int(time[:2]) * 60 * 60 + int(time[3:5]) * 60 + int(time[6:])

        

#The user interface
class UI:
    def __init__(self):
        self.mainwindow = tk.Tk()
        self.mainwindow.title("11+ Verbal Reasoning")
        self.mainwindow.state('zoomed')
        try:
            icon = ImageTk.PhotoImage(Image.open(resourcePath("11+Logo.ico")))
            icon.image = resourcePath("11+Logo.ico")
            self.mainwindow.iconphoto(False, icon)
        except:
            pass
        self.mainwindow.minsize(900, 450)

        self.startFrame = tk.Frame(self.mainwindow)
        self.UserData = self.load("UserData.bin") #Load the user data
        self.mainloop = self.mainwindow.mainloop

        #Variables initalised for use in the course of use
        self.currentQuestionDoing = None
        self.setQuestionsSinceLastSet = 0
        self.currentTestQuestion = 0
        self.testQuestions = {}
        self.timer = None
        self.tests = []
        self.questionCreationThread = None


        self.home() #Go to home by default
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()
        pass


    def home(self):
        self.currentQuestionDoing=None
        self.startFrame.destroy()
        self.startFrame = tk.Frame(self.mainwindow)

        #Title
        tk.Label(self.startFrame, text="11+ Verbal Reasoning", font = (FONT, 50)).grid(row=0, columnspan=3, pady=30)

        #Menu
        buttonSettings = {
            "hoverColour":BUTTONACTIVEBACKGROUND,
            "hoverText":BUTTONACTIVETEXT,
            "fg":BUTTONIDLETEXT,
            "bg":BUTTONIDLEBACKGROUND,
            "activeforeground":BUTTONCLICKEDTEXT, 
            "activebackground":BUTTONCLICKEDBACKGROUND,
            "bd":BUTTONBORDERWIDTH,
            "highlightbackground":BUTTONBORDER,
            "relief":"solid",
            "width":15,
            "height":5,
            "font":(FONT, 20)
        }
        HoverButton(
            self.startFrame, 
            text="Practice", 
            command=self.PracticeQuestions,
            **buttonSettings
        ).grid(row = 1, column = 0, padx=5, pady=5)
        HoverButton(
            self.startFrame, 
            text="Tasks", 
            command=self.doSetMain,
            **buttonSettings
        ).grid(row = 1, column = 1, padx=5, pady=5)
        HoverButton(
            self.startFrame, 
            text="Results", 
            command=self.ViewResults,
            **buttonSettings
        ).grid(row = 1, column = 2, padx=5, pady=5)
        HoverButton(
            self.startFrame, 
            text="Set Questions", 
            command=self.SetQuestions,
            **buttonSettings
        ).grid(row = 2, column = 0, padx=5, pady=5)
        self.startFrame.pack(anchor="center", expand=True)
        HoverButton(
            self.startFrame, 
            text="Take test", 
            command=self.test,
            **buttonSettings
        ).grid(row = 2, column = 1, padx=5, pady=5)
        self.startFrame.pack(anchor="center", expand=True)
        HoverButton(
            self.startFrame, 
            text="Dictionary", 
            command=self.lookupWord,
            **buttonSettings
        ).grid(row = 2, column = 2, padx=5, pady=5)
        self.startFrame.pack(anchor="center", expand=True)

    #Load the userdata
    def load(self, file):
        if os.path.isfile(file):
            with open(file, 'rb') as file:
                return pickle.load(file)
        else:
            return UserData()

    #Save the userdata
    def save(self):
        with open("UserData.bin", 'wb') as file:
            pickle.dump(self.UserData, file)

    #Dictionary
    def lookupWord(self):
        buttonSettings = {
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
            "height":2,
            "font":(FONT, 20)
        }
        self.startFrame.destroy()
        self.startFrame = tk.Frame(self.mainwindow)
        HoverButton(self.startFrame, text="⌂ Home", command=self.home, **buttonSettings).pack()
        self.startFrame.pack(fill = "both", expand=True)
        defWin = None
        def lookup(word):
            word = word.lower()
            if word is None or word == "": 
                return 0
            global defWin
            try:
                defWin.destroy()
            except:
                pass
            defWin = tk.Frame(self.startFrame)
            if word not in self.UserData.wordsNotKnown:
                self.UserData.wordsNotKnown.append(word)
            tk.Label(defWin, text = word.upper() + "\n\n" + formatDefinition(wordData.definition(word))).pack(padx = 5, pady=5)
            defWin.pack()
        tk.Label(self.startFrame, text="Enter a word to look up:").pack(pady=5, padx=5)
        wordBox = tk.Entry(self.startFrame)
        wordBox.pack(pady=5, padx=5)
        buttonSettings = {
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
        HoverButton(self.startFrame, text="Lookup", command=lambda: lookup(wordBox.get()), **buttonSettings).pack(padx = 5, pady=5)


    #Practice questions by type
    def PracticeQuestions(self):
        self.startFrame.destroy()
        self.startFrame = tk.Frame(self.mainwindow)

        #Menu
        buttonSettings = {
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
            "height":2,
            "font":(FONT, 20)
        }
        HoverButton(self.startFrame, text="⌂ Home", command=self.home, **buttonSettings).pack()
        self.startFrame.pack(fill = "both", expand=True)
        questionOptionFrameMain = ScrollableFrame(self.startFrame)
        questionOptionFrame = tk.Frame(questionOptionFrameMain.scrollableFrame)

        count = 0
        buttonSettings["font"] = 12
        buttonSettings["width"] = 40
        for questionType in QuestionTypes.keys():
            HoverButton(questionOptionFrame, text=questionType, command=lambda type=QuestionTypes[questionType]:self.doSpecific(type), **buttonSettings).grid(row=count, column=1, pady=5,padx=5)
            count += 1
        buttonSettings["height"] *= len(QuestionTypes.keys()) + 5
        HoverButton(questionOptionFrame, text = "Do set questions", command=self.doSetMain, **buttonSettings).grid(row = 0, column = 0, rowspan = len(QuestionTypes.keys()), padx=5, pady=5)
        questionOptionFrame.pack(anchor="center", side = "top")
        questionOptionFrameMain.pack(fill = "both", expand = True)
        
    #Take a test
    def test(self):
        self.startFrame.destroy()
        self.startFrame = tk.Frame(self.mainwindow)
        
        buttonSettings = {
            "hoverColour":BUTTONACTIVEBACKGROUND,
            "hoverText":BUTTONACTIVETEXT,
            "fg":BUTTONIDLETEXT,
            "bg":BUTTONIDLEBACKGROUND,
            "activeforeground":BUTTONCLICKEDTEXT, 
            "activebackground":BUTTONCLICKEDBACKGROUND,
            "bd":BUTTONBORDERWIDTH,
            "highlightbackground":BUTTONBORDER,
            "relief":"solid",
            "width":20,
            "height":2,
            "font":(FONT, 20)
        }
        HoverButton(self.startFrame, text="⌂ Home", command=self.home, **buttonSettings).pack()

        #Decide parameters for the test
        questionSettingFrame = tk.Frame(self.startFrame)
        params = {"Number of questions" : None, "Time for test (minutes)": None}
        row = 0
        for param in params.keys():
            tk.Label(questionSettingFrame, text=param).grid(row = row, column= 0, padx =5, pady= 5)
            params[param] = tk.Entry(questionSettingFrame)
            params[param].grid(row = row, column = 1, padx=5, pady=5)
            row += 1 
        HoverButton(questionSettingFrame, text = "Generate Questions", command= lambda e = params:self.generateQuestions(e), **buttonSettings).grid(row = row, columnspan= 2, column=0)
        questionSettingFrame.pack()
        self.startFrame.pack()

    #Generate questions for a test
    def generateQuestions(self, params):
        params["Number of questions"] = params["Number of questions"].get()
        params["Time for test (minutes)"] = params["Time for test (minutes)"].get()
        buttonSettings = {
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
            "height":2,
            "font":(FONT, 20)
        }

        #Generate the questions
        try:
            params["Number of questions"] = int(params["Number of questions"])
            params["Time for test (minutes)"] = int(params["Time for test (minutes)"])
        except Exception as e:
            PopupWindow(self.mainwindow, text="Incorrect Values entered").pack()
            self.test()
        questions = {}
        
        #Progress display
        progressFrame=tk.Frame(self.startFrame)
        progress = ttk.Progressbar(progressFrame, orient = tk.HORIZONTAL, length = 200, mode = 'determinate', maximum=params["Number of questions"] - 1)
        numberOfQuestions = int(params["Number of questions"])
        types = []
        timeLeft = 0
        qTypes = list(QuestionTypes.keys())
        for i in range(numberOfQuestions):
            t = qTypes[random.randint(0, len(qTypes) - 1)]
            types.append(t)
            timeLeft += timeToForm[t]
        label = tk.Label(progressFrame, text="Creating Test...\nTime left approximately " + dp(timeLeft,2) + " seconds", font=(FONT,15))
        label.pack()
        progress.pack()
        progressFrame.pack()
        self.mainwindow.update_idletasks()

        #Generate 1 question
        numberThreads = 1
        def generate(number, type):
            question = QuestionTypes[type]()
            questions[number] = [question, ""]
            return 0


        #Update progress
        for i in range(numberOfQuestions):
            generate(i, types[i])
            progress['value'] += 1
            timeLeft -= timeToForm[types[i]]
            label['text'] = "Creating Test...\nTime left approximately " + dp(timeLeft,2) + " seconds"
            self.mainwindow.update_idletasks()


        self.currentTestQuestion = 0
        self.testQuestions = questions
        self.startFrame.destroy()
        self.startFrame = tk.Frame(self.mainwindow)
        self.timer = Timer(self.mainwindow, self.startFrame, int(params["Time for test (minutes)"]), self.finishTest)
        self.timer.pack(padx=5, pady=5)
        doTestFrame = tk.Frame(self.startFrame)
        tk.Label(doTestFrame, text="There are "+ str(params["Number of questions"]) + " questions in this test. Press the button below to start the timer.").pack(padx= 5, pady=5)
        def dotest():
            self.timer.start()
            self.doTestQuestion(doTestFrame)
        HoverButton(doTestFrame, text="Start test", command = dotest, **buttonSettings).pack(padx=5, pady=5)
        self.startFrame.pack()
        doTestFrame.pack()


    #Take the test
    def doTestQuestion(self, previousFrame):
        buttonSettings = {
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
            "height":2,
            "font":(FONT, 20)
        }
        previousFrame.destroy()
        questionTakingFrame = tk.Frame(self.startFrame)
        currentQuestion = self.testQuestions[self.currentTestQuestion][0]
        currentAnswer = self.testQuestions[self.currentTestQuestion][1]
        currentQFrameTmp = tk.Frame(questionTakingFrame)
        currentQFrame = tk.Frame(currentQFrameTmp)
        answerBox = currentQuestion.display(None, USERAGENT, currentQFrame, submitNow = False)
        currentQFrame.pack()
        currentQFrameTmp.grid(row = 1, column = 0, columnspan=4)
        answerBox.delete(0,"end")
        answerBox.insert(0, currentAnswer)
        self.mainwindow.update()

        #Go to the next question
        def nextQuestion():
            self.currentTestQuestion += 1
            self.testQuestions[self.currentTestQuestion][1] = answerBox.get()
            self.doTestQuestion(questionTakingFrame)

        #Go to the previous question
        def prevQuestion():
            self.currentTestQuestion -= 1
            self.testQuestions[self.currentTestQuestion][1] = answerBox.get()
            self.doTestQuestion(questionTakingFrame)
        tk.Label(questionTakingFrame, text="Question " + str(self.currentTestQuestion + 1) + " out of " + str(len(self.testQuestions))).grid(row = 0, columnspan=4, column = 0, padx=5,pady=5)
        questionTakingFrame.pack(padx=5, pady=5)
        if self.currentTestQuestion != len(self.testQuestions) - 1:
            HoverButton(questionTakingFrame, text="Next>", command=nextQuestion, **buttonSettings).grid(row = 2, column=2, padx=5, pady=5)
        if self.currentTestQuestion != 0:
            HoverButton(questionTakingFrame, text="<Previous", command=prevQuestion, **buttonSettings).grid(row = 2, column=1,padx=5, pady=5)
    
        #Finish the test 
        def checkForFinish():
            questionTakingFrame.destroy()
            checkFrame = tk.Frame(self.startFrame)
            tk.Label(checkFrame, text = "Are you sure you want to finish and mark the test now?").grid(row = 0, columnspan=2, column=0, padx =5, pady=5)
            HoverButton(checkFrame, text = "Yes", command = self.finishTest, ** buttonSettings).grid(row = 1, column = 0,padx =5, pady=5)
            HoverButton(checkFrame, text = "No", command = lambda e = checkFrame:self.doTestQuestion(checkFrame), **buttonSettings).grid(row=1, column = 1,padx =5, pady=5)
            checkFrame.pack()
        HoverButton(questionTakingFrame, text="Finish Test", command=checkForFinish, **buttonSettings).grid(row = 3, column=1, columnspan = 2, padx=5, pady=5)

    #Mark the test
    def finishTest(self):
        timeWhenStopped = self.timer.stop()
        buttonSettings = {
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
            "height":2,
            "font":(FONT, 20)
        }
        self.startFrame.destroy()
        self.startFrame = tk.Frame(self.mainwindow)
        progressFrame = tk.Frame(self.startFrame)
        progress = ttk.Progressbar(progressFrame, orient = tk.HORIZONTAL, length = 200, mode = 'determinate', maximum=len(self.testQuestions)-1)
        tk.Label(progressFrame, text="Marking questions...", font=(FONT,15)).pack()
        progress.pack()
        progressFrame.pack()
        self.startFrame.pack()

        self.mainwindow.update_idletasks()
        markedQuestions = []
        correctQuestions = 0
        for i in range(len(self.testQuestions)):
            result = self.testQuestions[i][0].verify(self.testQuestions[i][1])
            self.testQuestions[i][0].correct = result
            markedQuestions.append(self.testQuestions[i][0])
            if result:
                correctQuestions += 1
            progress['value'] += 1
            self.mainwindow.update_idletasks()
        progressFrame.destroy()
        self.startFrame.destroy()
        self.startFrame = tk.Frame(self.mainwindow)
        resultsFrame = tk.Frame(self.startFrame)

        HoverButton(resultsFrame, text="⌂ Home", command=self.home, **buttonSettings).pack(padx=5, pady=5)
        test = Test(markedQuestions, correctQuestions, self.timer.startTime, timeWhenStopped, dateFormat(datetime.datetime.today().date()))
        self.UserData.testsDone.append(test)

        #View the test and the answers
        test.view(USERAGENT, resultsFrame)
        resultsFrame.pack(expand=True, fill="both")
        self.startFrame.pack(expand=True, fill = "both")






    #Do preset question
    def doSet(self):
        random.shuffle(self.UserData.setQuestions)
        self.startFrame.destroy()
        self.startFrame = tk.Frame(self.mainwindow)
        buttonSettings = {
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
            "height":2,
            "font":(FONT, 20)
        }
        HoverButton(self.startFrame, text="⌂ Home", command=self.home, **buttonSettings).pack(padx=5, pady=5)
        if len(self.UserData.setQuestions) > 0:
            questionFrame = tk.Frame(self.startFrame)
            question = self.UserData.setQuestions[0]
            self.currentQuestionDoing = "SET"
            question.display(USERAGENT, self.answerHandler, questionFrame)    
            questionFrame.pack()
        else:
            tk.Label(self.startFrame, text = "You have completed you assigned questions!").pack(padx=5, pady=5)
            HoverButton(self.startFrame, text="Finish", command=self.home, **buttonSettings).pack(padx=5, pady=5)
        self.startFrame.pack()

    #Overview of preset questions
    def doSetMain(self):
        self.startFrame.destroy()
        self.startFrame = tk.Frame(self.mainwindow)
        buttonSettings = {
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
            "height":2,
            "font":(FONT, 20)
        }
        HoverButton(self.startFrame, text="⌂ Home", command=self.home, **buttonSettings).pack(padx=5, pady=5)
        tk.Label(self.startFrame, text="You have " + str(len(self.UserData.setQuestions))  + " questions to do",font=(FONT,15)).pack(padx = 5, pady=5)
        tk.Label(self.startFrame, text= "Question breakdown:", font=(FONT,18, 'underline', 'bold')).pack(padx=5, pady=5)
        questionBreakdownFrame = tk.Frame(self.startFrame)
        questionNumbers = {}
        for questionType in QuestionTypes:
            questionNumbers[questionType] = 0
        for question in self.UserData.setQuestions:
            questionNumbers[question.type]+=1
        count = 0
        for questionType in QuestionTypes:
            tk.Label(questionBreakdownFrame, text=questionType + ":", font=(FONT, 13)).grid(row=count, column = 0, padx=5, pady=5)
            tk.Label(questionBreakdownFrame, text=str(questionNumbers[questionType]), font=(FONT, 13)).grid(row=count, column = 1, padx=5, pady=5)
            count += 1
        questionBreakdownFrame.pack(padx=5, pady=5)
        buttonSettings["width"] = 11
        HoverButton(self.startFrame, text="Do Questions", command=self.doSet, **buttonSettings).pack(padx=5, pady=5)
        self.startFrame.pack()

            


    #Do a specific type of question
    def doSpecific(self, type):
        self.startFrame.destroy()
        self.startFrame = tk.Frame(self.mainwindow)
        buttonSettings = {
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
            "height":2,
            "font":(FONT, 20)
        }
        HoverButton(self.startFrame, text="⌂ Home", command=self.home, **buttonSettings).pack()
        questionDoFrame = tk.Frame(self.startFrame)
        def setNextQuestion():
            self.UserData.nextQuestion[type] = type()
            return 0
        try:
            x = self.UserData.nextQuestion[type]
            self.questionCreationThread.join()
            question = self.UserData.nextQuestion[type]
        except:
            question = type()
        self.questionCreationThread = threading.Thread(target=setNextQuestion)
        self.questionCreationThread.start()
            
        self.currentQuestionDoing = "SPECIFIC"
        question.display(USERAGENT, self.answerHandler, questionDoFrame)
        self.startFrame.pack()
        questionDoFrame.pack()

    #Handle the answer to a question
    def answerHandler(self, question, wordstolookup, type):
        
        
        answerHandlingFrame = tk.Frame(self.startFrame)
        
        count = 1
        wordsDone = []
        for word in wordstolookup:
            if word.lower() not in wordsDone and word != "":
                buttonSettings = {
                    "hoverColour":BUTTONACTIVEBACKGROUND,
                    "hoverText":BUTTONACTIVETEXT,
                    "fg":BUTTONIDLETEXT,
                    "bg":BUTTONIDLEBACKGROUND,
                    "activeforeground":BUTTONCLICKEDTEXT, 
                    "activebackground":BUTTONCLICKEDBACKGROUND,
                    "bd":BUTTONBORDERWIDTH,
                    "highlightbackground":BUTTONBORDER,
                    "relief":"solid",
                    "width":higher(len(word) + 2, 10),
                    "height":2,
                    "font":(FONT, 12)
                }
                HoverButton(answerHandlingFrame, text = word.lower(), command=lambda e=word:self.lookupDisplay(e.lower()), **buttonSettings).grid(row = 2, column = count, padx=5, pady=5)
                wordsDone.append(word.lower())
                count += 1
        
        buttonSettings = {
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
            "height":2,
            "font":(FONT, 12)
        }
        question.wordsToLookup = wordsDone
        self.UserData.doneQuestions.append(question)
        if count != 1:
            tk.Label(answerHandlingFrame, text="Lookup word:", font=(FONT, 12)).grid(row = 1, column = 0, columnspan=count, padx=5, pady=5)
        if self.currentQuestionDoing =="SET":
            HoverButton(answerHandlingFrame, text="Next>", command=self.doSet, **buttonSettings).grid(row = 0, column=0, columnspan=count, padx=5, pady=5)
            self.setQuestionsSinceLastSet += 1
            self.UserData.setQuestions.pop(0)
        else:
            HoverButton(answerHandlingFrame, text="Next>", command=lambda e=type: self.doSpecific(QuestionTypes[e]), **buttonSettings).grid(row = 0, column=0, columnspan=count, padx=5, pady=5)
        answerHandlingFrame.pack()
        self.currentQuestionDoing=None


    #Dictionary popup window in question
    def lookupDisplay(self, word):
        if word not in self.UserData.wordsNotKnown:
            self.UserData.wordsNotKnown.append(word)
        buttonSettings = {
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

        PopupWindow(self.startFrame, word.upper() + "\n\n" + formatDefinition(wordData.definition(word)), buttonSettings=buttonSettings, hoverButton=True).pack()

    #Set questions for the student to do
    def SetQuestions(self):
        self.startFrame.destroy()
        self.startFrame = tk.Frame(self.mainwindow)
        buttonSettings = {
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
        HoverButton(self.startFrame, text="⌂ Home", command=self.home, **buttonSettings).pack()
        tk.Label(self.startFrame, text="There are currently " + str(len(self.UserData.setQuestions)) + " questions set.", font = (FONT, 15)).pack(padx=5,pady=5)
        tk.Label(self.startFrame, text=str(self.setQuestionsSinceLastSet) + " questions done since last set.", font = (FONT, 15)).pack(padx=5,pady=5)
        questionSetFrame = tk.Frame(self.startFrame)
        count = 0
        questionTypeEntryMap = {}
        
        for questionType in QuestionTypes.keys():
            tk.Label(questionSetFrame, text=questionType, font=(FONT, 15)).grid(row = count, column = 0, padx=5, pady=5)
            questionTypeEntryMap[questionType] = tk.Entry(questionSetFrame, font=(FONT, 15))
            questionTypeEntryMap[questionType].grid(row = count, column = 1, padx=5, pady=5)
            count += 1
        def setExecute():
            try:
                questionsTotal=0
                numberOfEach = {}
                for questionType in QuestionTypes.keys():            
                    number = questionTypeEntryMap[questionType].get()
                    if number == "":
                        number = 0
                    questionsTotal += int(number)
                    numberOfEach[questionType] = int(number)
                progressFrame=tk.Frame(self.startFrame)
                progress = ttk.Progressbar(progressFrame, orient = tk.HORIZONTAL, length = 200, mode = 'determinate', maximum=questionsTotal)
                timeLeft = 0
                
                for questionType in QuestionTypes.keys():
                    for i in range(numberOfEach[questionType]):
                        timeLeft += timeToForm[questionType]
                label = tk.Label(progressFrame, text="Setting...\nTime left approximately " + dp(timeLeft,2) + " seconds", font=(FONT,15))
                label.pack()
                progress.pack()
                progressFrame.pack()
                self.mainwindow.update_idletasks()
                for questionType in QuestionTypes.keys():
                    for i in range(numberOfEach[questionType]):
                        self.UserData.setQuestions.append(QuestionTypes[questionType]())
                        timeLeft -= timeToForm[questionType]
                        progress['value'] += 1
                        label['text'] = "Setting...\nTime left approximately " + dp(timeLeft,2) + " seconds"
                        self.mainwindow.update_idletasks()
                PopupWindow(self.mainwindow, str(questionsTotal) + " questions set!").pack()
                self.home()
            except:
                tk.Label(questionSetFrame, text="Please enter a whole number in each box, or leave them blank", font=(FONT,15)).grid(row=count+2, column = 0, columnspan=2, padx=5, pady=5)
            
        HoverButton(questionSetFrame, text="Set", command=setExecute, **buttonSettings).grid(row=count, column=1, padx=5, pady=5)
        questionSetFrame.pack()
        self.startFrame.pack()

            
            


    #Remove a word from the words to learn list
    def removeNewWord(self, index):
        self.UserData.removeNewWord(index)
        self.ViewResults()
    
    #View all results
    def ViewResults(self):
        buttonSettings = {
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
        xButtonSettings = {
            "hoverColour":REMOVEBUTTONACTIVEBACKGROUND,
            "hoverText":REMOVEBUTTONACTIVETEXT,
            "fg":REMOVEBUTTONIDLETEXT,
            "bg":REMOVEBUTTONIDLEBACKGROUND,
            "activeforeground":REMOVEBUTTONCLICKEDTEXT, 
            "activebackground":REMOVEBUTTONCLICKEDBACKGROUND,
            "bd":REMOVEBUTTONBORDERWIDTH,
            "highlightbackground":REMOVEBUTTONBORDER,
            "relief":"solid",
            "height":1,
            "font":(FONT, 15)
        }
        self.startFrame.destroy()
        self.startFrame = tk.Frame(self.mainwindow)
        resultsViewFrame = tk.Frame(self.startFrame)



        newWordsFrame = tk.Frame(resultsViewFrame)
        newWordsBody = ScrollableFrame(newWordsFrame)
        tk.Label(newWordsFrame, text="New Words", font=(FONT, 20, "bold", "underline")).pack(fill="both", pady=5, padx=5)
        count = 0
        newWordsBody.scrollableFrame.grid_anchor("center")
        wordsNotKnown = self.UserData.wordsNotKnown
        wordsNotKnown.reverse()
        if len(wordsNotKnown) == 0:
            tk.Label(newWordsFrame, text="You know all your words for now!", font=(FONT, 15)).pack(fill="both", pady=5, padx=5)
        else:
            for word in wordsNotKnown:
                HoverButton(newWordsBody.scrollableFrame, text = word[:1].upper() + word[1:], command=lambda e=word:self.lookupDisplay(e), **buttonSettings).grid(row = count, column = 0, padx=5, pady=5)
                HoverButton(newWordsBody.scrollableFrame, text= "X", command=lambda e=count:self.removeNewWord(e), **xButtonSettings).grid(row = count, column = 1)
                count += 1

        newWordsBody.pack(side="right", expand=True, fill="y", pady=5, anchor="center")
        newWordsFrame.pack(side="right",fill="y", anchor="e", pady=5)


        middleBorder = tk.Frame(resultsViewFrame, highlightbackground="#000000", borderwidth=2, background="#000000", width=1)
        middleBorder.pack(fill="y", side="right", anchor="ne")

        
        leftSideFrame = tk.Frame(resultsViewFrame)
        HoverButton(leftSideFrame, text="⌂ Home", command=self.home, **buttonSettings).pack()
        questionsAnsweredFrame = tk.Frame(leftSideFrame)

        questionsDisplayFrame = ScrollableFrame(questionsAnsweredFrame, vside="left")
        tk.Label(questionsDisplayFrame.scrollableFrame, text="Questions Answered", font=(FONT,20, "underline", "bold")).grid(row=0, column=1, columnspan=3, padx = 5, pady=5)
        tk.Label(questionsDisplayFrame.scrollableFrame, text = "Type", font=(FONT,15, "underline")).grid(row=1, column=0, padx = 5, pady=5)
        tk.Label(questionsDisplayFrame.scrollableFrame, text = "Answer Given", font=(FONT,15, "underline")).grid(row = 1, column=1, padx = 5, pady=5)
        tk.Label(questionsDisplayFrame.scrollableFrame, text = "Correct Answer", font=(FONT,15, "underline")).grid(row = 1, column = 2, padx = 5, pady=5)
        tk.Label(questionsDisplayFrame.scrollableFrame, text = "Correct?", font=(FONT,15, "underline")).grid(row = 1, column = 3, padx = 5, pady=5)
        count = 2


        
        doneQuestions = self.UserData.doneQuestions
        doneQuestions.reverse()
        for question in doneQuestions:
            tk.Label(questionsDisplayFrame.scrollableFrame, text = question.type).grid(row=count, column=0, padx = 5, pady=5)
            tk.Label(questionsDisplayFrame.scrollableFrame, text = question.answer).grid(row = count, column=1, padx = 5, pady=5)
            tk.Label(questionsDisplayFrame.scrollableFrame, text = question.correctAnswer).grid(row = count, column = 2, padx = 5, pady=5)
            tk.Label(questionsDisplayFrame.scrollableFrame, text = btos(question.correct)).grid(row = count, column = 3, padx = 5, pady=5)
            HoverButton(questionsDisplayFrame.scrollableFrame, text = "View", command=lambda e=question:self.viewQuestion(e), **buttonSettings).grid(row=count, column=4, sticky="E", padx=5, pady=5)
            count +=1 
        questionsDisplayFrame.pack(expand=True, side="top", fill="both", anchor="w",pady=5)
        colsizes = {0:300,
                    1:150,
                    2:150,
                    3:150,
                    4:150
                    }
        for i in range(0,4):
            questionsDisplayFrame.scrollableFrame.grid_columnconfigure(i, minsize=colsizes[i])
            questionsDisplayFrame.scrollableFrame.grid_columnconfigure(4, minsize=colsizes[4])
        questionsAnsweredFrame.pack(side="top", expand=True, fill="both", anchor="nw", pady=5)
        
        
        middleBorderleft = tk.Frame(leftSideFrame, highlightbackground="#000000", borderwidth=2, background="#000000", width=1)
        middleBorderleft.pack(fill="x", side="top", pady = 5)

        
        
        testViewFrame = tk.Frame(leftSideFrame)



        testsDisplayFrame = ScrollableFrame(testViewFrame, vside="left")
        HoverButton(testsDisplayFrame.scrollableFrame, text = "Analyse", command=self.testAnalyse, **buttonSettings).grid(row=0, column=0, sticky="E", padx=5, pady=5)
        tk.Label(testsDisplayFrame.scrollableFrame, text="Tests done", font=(FONT,20, "underline", "bold")).grid(row=0, column=1, columnspan=3, padx = 5, pady=5)
        tk.Label(testsDisplayFrame.scrollableFrame, text = "Date taken", font=(FONT,15, "underline")).grid(row=1, column=0, padx = 5, pady=5)
        tk.Label(testsDisplayFrame.scrollableFrame, text = "Questions in test", font=(FONT,15, "underline")).grid(row = 1, column=1, padx = 5, pady=5)
        tk.Label(testsDisplayFrame.scrollableFrame, text = "Time taken", font=(FONT,15, "underline")).grid(row = 1, column = 2, padx = 5, pady=5)
        tk.Label(testsDisplayFrame.scrollableFrame, text = "Percentage", font=(FONT,15, "underline")).grid(row = 1, column = 3, padx = 5, pady=5)
        count = 2


        
        doneQuestions = self.UserData.doneQuestions
        doneQuestions.reverse()
        for test in self.UserData.testsDone:
            tk.Label(testsDisplayFrame.scrollableFrame, text = test.dateSet).grid(row=count, column=0, padx = 5, pady=5)
            tk.Label(testsDisplayFrame.scrollableFrame, text = len(test.questions)).grid(row = count, column=1, padx = 5, pady=5)
            tk.Label(testsDisplayFrame.scrollableFrame, text = test.timeTaken).grid(row = count, column = 2, padx = 5, pady=5)
            tk.Label(testsDisplayFrame.scrollableFrame, text = test.percentage).grid(row = count, column = 3, padx = 5, pady=5)
            HoverButton(testsDisplayFrame.scrollableFrame, text = "View", command=lambda e=test:self.viewQuestion(e), **buttonSettings).grid(row=count, column=4, sticky="E", padx=5, pady=5)
            count +=1 
        testsDisplayFrame.pack(expand=True, side="bottom", fill="both", anchor="w")
        colsizes = {0:200,
            1:150,
            2:300,
            3:150,
            4:150
            }
        for i in range(0,4):
            testsDisplayFrame.scrollableFrame.grid_columnconfigure(i, minsize=colsizes[i])
            testsDisplayFrame.scrollableFrame.grid_columnconfigure(4, minsize=colsizes[4])
        testViewFrame.pack(side="bottom", expand=True, fill="both", anchor="sw", pady=5)


        leftSideFrame.pack(side="left", expand=True, fill="both", anchor="w", pady=5)




        self.startFrame.pack(expand=True, fill="both")
        resultsViewFrame.pack(expand=True, fill="both")
    
    #Perform analysis on tests
    def testAnalyse(self):
        buttonSettings = {
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
        puw = PopupWindow(self.mainwindow, buttonSettings=buttonSettings, hoverButton=True, fullScreen = True)
        sf = ScrollableFrame(puw.body, horizontalSB=True, verticalSB=True)
        parent = sf.scrollableFrame
        dateList = [t.dateSet for t in self.UserData.testsDone]
        markList = [t.mark for t in self.UserData.testsDone]


        timeTakenList = [(int((secs(t.timeTaken)/len(t.questions)) * 10)) / 10 for t in self.UserData.testsDone]
        marksAgainstTime = Graph(parent)
        marksAgainstTime.datePlot(dateList, markList, title = "Marks over time", xaxis = "Date", yaxis = "Mark")
        marksAgainstTime.grid(row = 0, column = 0)

        Line(parent).grid('y', row=0, column=1, rowspan=3)

        marksAgainstTimeTaken = Graph(parent)
        marksAgainstTimeTaken.plot(timeTakenList, markList, title="Marks depending on time spent per question", xaxis = "Time spent per question/secs", yaxis = "Mark", rotation=45)
        marksAgainstTimeTaken.grid(row=0, column=2)

        Line(parent).grid('x', row=1, column=0, colspan=3)

        timeTakenAgainstTime = Graph(parent)
        timeTakenAgainstTime.datePlot(dateList, timeTakenList, title = "Time spent per question over time", xaxis = "Date", yaxis = "Time spend per question/secs")
        timeTakenAgainstTime.grid(row=2, column = 0)
        sf.pack(expand=True, fill="both")
        puw.pack(expand=True, fill="both", pady=5, padx=5)









    #View a question
    def viewQuestion(self, question):
        buttonSettings = {
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
        puw = PopupWindow(self.mainwindow, buttonSettings=buttonSettings, hoverButton=True)
        parent = tk.Frame(puw.body)
        question.view(USERAGENT, parent)
        parent.pack(expand=True, fill="both")
        puw.pack()


#Get the word data
words = getWords(resourcePath("commonwords.bin"))
allwords = getWords(resourcePath("allwords.bin"))
with UI() as ui:
    ui.mainloop()

