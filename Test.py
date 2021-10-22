from constants import *
from tkExtensions import *



#A test
class Test:
    def __init__(self, questions, mark, timeForTest, timeLeft, dateSet):
        self.questions = questions
        self.percentage = int((mark/len(questions))*100)
        self.mark = mark
        self.time = timeForTest
        self.timeLeft = timeLeft
        self.dateSet = dateSet
        self.timeTaken = subtractTimes(timeForTest, timeLeft)


    #View the test on windows
    def viewWindows(self, parent):

        #View a test question
        def viewQuestion(question):

            #Button display parameters
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
            puw = PopupWindow(parent, buttonSettings=buttonSettings, hoverButton=True)
            puw.pack()
            qparent = tk.Frame(puw.body)
            question.view(qparent)
        p = ScrollableFrame(parent, width=400, height = 500)
        innerFrame = p.scrollableFrame
        viewQuestionsFrame=tk.Frame(innerFrame)
        row = 0
        col = 0
        questionNum = 1

        #Style of a button for a question that is correct
        correctButton = {
            "hoverColour":CORRECTBUTTONACTIVEBACKGROUND,
            "hoverText":CORRECTBUTTONACTIVETEXT,
            "fg":CORRECTBUTTONIDLETEXT,
            "bg":CORRECTBUTTONIDLEBACKGROUND,
            "activeforeground":CORRECTBUTTONCLICKEDTEXT, 
            "activebackground":CORRECTBUTTONCLICKEDBACKGROUND,
            "bd":CORRECTBUTTONBORDERWIDTH,
            "highlightbackground":CORRECTBUTTONBORDER,
            "relief":"solid",
            "width":3,
            "height":2,
            "font":(FONT, 20)
        }

        #Style of a button for a question that is incorrect
        incorrectButton = {
            "hoverColour":INCORRECTBUTTONACTIVEBACKGROUND,
            "hoverText":INCORRECTBUTTONACTIVETEXT,
            "fg":INCORRECTBUTTONIDLETEXT,
            "bg":INCORRECTBUTTONIDLEBACKGROUND,
            "activeforeground":INCORRECTBUTTONCLICKEDTEXT, 
            "activebackground":INCORRECTBUTTONCLICKEDBACKGROUND,
            "bd":INCORRECTBUTTONBORDERWIDTH,
            "highlightbackground":INCORRECTBUTTONBORDER,
            "relief":"solid",
            "width":3,
            "height":2,
            "font":(FONT, 20)
        }

        #Display test score
        tk.Label(parent, text = "Your test score is in...\nYou got " + str(self.mark) + " out of " + str(len(self.questions)) +"\nThat gives you a percentage of " + str(self.percentage) + "%" + "\nAnd you had " + self.timeLeft + " left on the clock out of " +self.time).pack(padx=5, pady=5)
        
        #View each question after completion
        for question in self.questions:
            if question.correct:
                HoverButton(viewQuestionsFrame, text = str(questionNum), command=lambda e=question:viewQuestion(e), **correctButton).grid(row=row, column=col, padx=5, pady=5)
            else:
                HoverButton(viewQuestionsFrame, text = str(questionNum), command=lambda e=question:viewQuestion(e), **incorrectButton).grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col == 6:
                col = 0
                row += 1
            questionNum += 1
        viewQuestionsFrame.pack()
        p.pack()

    #Implementation for android display
    def viewAndroid(self, parent):
        pass

    #View wrapper
    def view(self, parent, useragent):
        if useragent == ANDROID:
            self.viewAndroid(parent)
        else:
            self.viewWindows(parent)