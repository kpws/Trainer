import os
import subprocess
import question
from levenshtein import almostEqual
from colorPrint import printInCol

class City(question.Question):
    def __init__(self, fileName,name):
        self._filename=fileName
        self._name=name

    @staticmethod
    def getQuestions():
        qList=[]
        for dirname, dirnames, filenames in os.walk(os.path.join(os.path.dirname(__file__), 'data','cities')):
            qList+=[City(os.path.join(dirname,f).replace(' ','\ '),f.rsplit('.')[0]) for f in filenames]
        return qList

    def pose(self):
        os.system('eog --new-instance '+self._filename)

    def verify(self,inp):
        self._wasCorrect=almostEqual(inp.lower(),self._name.lower())
        self._wasFullyCorrect=inp.lower()==self._name.lower()
        return self._wasCorrect

    def printMessage(self):
        if self._wasCorrect:
            if not self._wasFullyCorrect:
                printInCol('blue','It is actually spelled '+self._name+'.')
        else:
            printInCol('red','Wrong, the correct city is '+self._name+'.')

    def getId(self):
        return 'city/'+self._name
