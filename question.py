import trainer
from colorPrint import printInCol

class Question():
    def pose(self):
        printInCol('yellow',self._question)
    def printMessage(self):
        if not self._wasCorrect:
            printInCol('red','Wrong, the correct answer is: '+self._answer+'.')
        if self._message!='':
            printInCol('blue',self._message)
    def verify(self,answer):
        self._wasCorrect=answer.lower()==self._answer.lower()
        return self._wasCorrect
