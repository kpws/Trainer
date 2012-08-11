import os
import subprocess
import question
from colorPrint import printInCol

class Country(question.Question):
    def __init__(self, fileName,continent,name):
        self._filename=fileName
        self._name=name
        self._continent=continent

    @staticmethod
    def getQuestions():
        qList=[]
        for dirname, dirnames, filenames in os.walk(os.path.join(os.path.dirname(__file__), 'data','countries')):
            qList+=[Country(os.path.join(dirname,f),*f.rsplit('.')[0].lower().replace('-',' ').rsplit('_')) for f in filenames]
        return qList

    def __call__(self):
        os.system('eog '+self._filename)
        if raw_input().lower()==self._name:
            ret = True
        else:
            printInCol('red','Wrong, the correct answer is '+self._name)
            ret = False
        return ret
    def getId(self):
        return 'years/'+self._name
