from tkinter.constants import S
from commonFunctions import lower
import random

#Generates sequences
class SequenceGenerator:
    def __init__(self, min = -1000, max = 1000, step = 10, maxEndStep = 100, maxStepChange = 10, maxMultiDivisionFactor = 10, minDegree = 2, maxDegree = 10, minStartValue = -10, maxStartValue = 10):
        
        #Types of sequences supported
        self.types = {"linear" : lambda: self.linear(min, max, step),
                    "Negative Linear" : lambda: self.negativeLinear(min, max, step),
                    "Double Positive Linear" : lambda: self.doublePositiveLinear(min, max, step),
                    "Positive-Negative Linear" : lambda: self.positiveNegativeLinear(min, max, step),
                    "Double Negative Linear" : lambda: self.doubleNegativeLinear(min, max, step),
                    "Alternating Step" : lambda: self.alternatingStep(min, max, step),
                    "Negative Alternating Step" : lambda: self.negativeAlternatingStep(min, max, step),
                    "Increasing Step" : lambda: self.increasingStep(min, max, step, maxEndStep, maxStepChange),
                    "Decreasing Step" : lambda: self.decreasingStep(min, max, step, maxEndStep, maxStepChange),
                    "Multiply" : lambda: self.multiply(min, max, maxMultiDivisionFactor),
                    "Divide" : lambda: self.divide(min, max, maxMultiDivisionFactor),
                    "Polynomial" : lambda: self.polynomial(min, max, minDegree, maxDegree),
                    "Negative Polynomial" : lambda: self.negativePolynomial(min, max, minDegree, maxDegree),
                    "Multiply by last Number" : lambda: self.multiplyByLastNumber(minStartValue, maxStartValue, max),
                    "Divide by next Number" : lambda: self.divideByNextNumber(minStartValue, maxStartValue, max),
                    }
        #Descriptions of the different sequences
        self.typeDescriptions= {"linear" : "Each number is the last one plus a constant number",
                                "Negative Linear" : "Each number is the last one subtract a constant number",
                                "Double Positive Linear" : "Two sequences alternating positions - each sequence's next term is the last term plus a constant number",
                                "Positive-Negative Linear" : "Two sequences alternating positions - one sequence's next term is the last term plus a constant number, the other sequence's next term is the last term minus a constant number",
                                "Double Negative Linear" : "Two sequences alternating positions - each sequence's next term is the last term minus a constant number",
                                "Alternating Step" : "Each number is the last number plus a constant number, the constant number alternates between two each time",
                                "Negative Alternating Step" : "Each number is the last number minus a constant number, the constant number alternates between two each time",
                                "Increasing Step" : "Each number is the last number plus a number, the number increases each time",
                                "Decreasing Step" : "Each number is the last number plus a number, the number decreases each time""Each number is the last number plus a number, the number increases each time",
                                "Multiply" : "Each number is the last number multiplied by a constant number",
                                "Divide" : "Each number is the last number divided by a constant number",
                                "Polynomial" : "Each number is a term of a positive polynomial sequence",
                                "Negative Polynomial" : "Each number is a term of a negative polynomial sequence",
                                "Multiply by last Number" : "The next term is the last two multiplied together",
                                "Divide by last Number" : "The next term is the number before last divided by the last number"
                                }

    
    #Add two sequences together, alternating between their values
    def addSeq(self, seq1, seq2):
        seq = []
        maxIndex = lower(len(seq1) - 1, len(seq2) - 1)
        for i in range(maxIndex):
            seq.append(seq1[i])
            seq.append(seq2[i])
        return seq


    #Generate a random sequence
    def random(self, typesList = []):
        if typesList ==[]:
            typesList = list(self.types.keys())
        random.shuffle(typesList)
        return self.types[typesList[0]](), typesList[0]


    def linear(self, minValue, maxValue, maxStep):
        step = random.randint(1, maxStep)
        startValue = random.randint(minValue, maxValue)
        endValue = random.randint(startValue, maxValue)
        seq = []
        for i in range(startValue, endValue, step):
            seq.append(i)
        return seq
    
    def negativeLinear(self, minValue, maxValue, maxStep):
        seq = self.linear(minValue, maxValue, maxStep)
        seq.reverse()
        return seq

    def doublePositiveLinear(self, minValue, maxValue, maxStep):
        seq1 = self.linear(minValue, maxValue, maxStep)
        seq2 = self.linear(minValue, maxValue, maxStep)
        return self.addSeq(seq1, seq2)

    
    def positiveNegativeLinear(self, minValue, maxValue, maxStep):
        seq1 = self.linear(minValue, maxValue, maxStep)
        seq2 = self.negativeLinear(minValue, maxValue, maxStep)
        return self.addSeq(seq1, seq2)

    def doubleNegativeLinear(self, minValue, maxValue, maxStep):
        seq1 = self.negativeLinear(minValue, maxValue, maxStep)
        seq2 = self.negativeLinear(minValue, maxValue, maxStep)
        return self.addSeq(seq1, seq2)
    
    def alternatingStep(self, minValue, maxValue, maxStep):
        step1 = random.randint(1, maxStep)
        step2 = random.randint(1, maxStep)
        startValue = random.randint(minValue, maxValue)
        endValue = random.randint(startValue, maxValue)
        seq = []
        value = startValue
        while abs(value) <= endValue + step1 + step2:
            seq.append(value)
            value += step1
            seq.append(value)
            value += step2
        return seq

    def negativeAlternatingStep(self, minValue, maxValue, maxStep):
        seq = self.alternatingStep(minValue, maxValue, maxStep)
        seq.reverse()
        return seq
    
    def increasingStep(self, minValue, maxValue, maxStartStep, maxEndStep, maxStepChange):
        step = random.randint(1, maxStartStep)
        stepChange = random.randint(1,maxStepChange)
        seq = []
        startValue = random.randint(minValue, maxValue)
        endValue = random.randint(startValue, maxValue)
        value = startValue
        while abs(value) <= endValue and abs(step) <= maxEndStep:
            seq.append(value)
            value += step
            step+=stepChange
        return seq


    def decreasingStep(self, minValue, maxValue, maxStartStep, maxEndStep, maxStepChange):
        seq = self.increasingStep(minValue, maxValue, maxEndStep, maxStartStep, maxStepChange)
        seq.reverse()
        return seq
    
    def multiply(self, minValue, maxValue, maxMultiplicationFactor):
        value = random.randint(minValue, maxValue)
        while value != 0:
            value = random.randint(minValue, maxValue)
        endValue = random.randint(value, maxValue)
        multiplicationFactor = random.randint(2, maxMultiplicationFactor)
        seq = []
        while abs(value) <= endValue:
            seq.append(value)
            if value == 0:
                break
            value *= multiplicationFactor
        return seq

    def divide(self, minValue, maxValue, maxDivisionFactor):
        seq = self.multiply(minValue, maxValue, maxDivisionFactor)
        seq.reverse()
        return seq

    def polynomial(self, minValue, maxValue, minDegree, maxDegree):
        value = random.randint(minValue, maxValue)
        endValue = random.randint(value, maxValue)
        degree = random.randint(minDegree, maxDegree)
        seq = []
        count = 1
        while abs(value) <= endValue:
            seq.append(value)
            value = count ** degree
            count += 1
        return seq

    def negativePolynomial(self, minValue, maxValue, minDegree, maxDegree):
        seq = self.polynomial(minValue, maxValue, minDegree, maxDegree)
        seq.reverse()
        return seq

    def multiplyByLastNumber(self, minStartValue, maxStartValue, maxValue):
        lastValue = random.randint(minStartValue, maxStartValue)
        value = random.randint(lastValue, maxStartValue)
        seq = []
        while abs(value) <= maxValue:
            seq.append(value)
            temp = value
            if lastValue == 1 or lastValue == 0:
                break
            value *= lastValue
            lastValue = temp
        return seq

    def divideByNextNumber(self, minEndValue, maxEndValue, maxValue):
        seq = self.multiplyByLastNumber(minEndValue, maxEndValue, maxValue)
        seq.reverse()
        return seq


    





        


        




    
    


