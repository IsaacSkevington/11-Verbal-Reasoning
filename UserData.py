#Stores the user's data
class UserData:
    def __init__(self):
        self.setQuestions = []
        self.doneQuestions = []
        self.wordsNotKnown = []
        self.testsDone = []
        self.nextQuestion = {}
    
    #Remove a new word
    def removeNewWord(self, index):
        try:
            self.wordsNotKnown.pop(index)
            return True
        except Exception as e:
            print(e)
            return False