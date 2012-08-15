import os
import subprocess
import question
from colorPrint import printInCol
from levenshtein import almostEqual

class Country(question.Question):
    def __init__(self, fileName,continent,name):
        self._filename=fileName
        self._name=name
        self._continent=continent

    @staticmethod
    def getQuestions():
        qList=[]
        for dirname, dirnames, filenames in os.walk(os.path.join(os.path.dirname(__file__), 'data','countries')):
            qList+=[Country(os.path.join(dirname,f).replace(' ','\ '),*f.rsplit('.')[0].rsplit('_')) for f in filenames]
        return qList

    def __call__(self):
        os.system('eog --new-instance '+self._filename)
        inp=raw_input()
        if almostEqual(inp.lower(),self._name.lower()):
            ret = True
            printInCol('green','Correct!')
            if inp.lower()!=self._name.lower():
                printInCol('blue','It is actually spelled '+self._name+'.')
        else:
            printInCol('red','Wrong, the correct answer is '+self._name+'.')
            ret = False
        return ret
    def getId(self):
        return 'country/'+self._name
