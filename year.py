import os

import question
from colorPrint import printInCol

class Year(question.Question):
    def __init__(self, event, year):
        self._event=event
        self._year=year

    @staticmethod
    def getQuestions():
        with open(os.path.join(os.path.dirname(__file__), 'data','year'),'r') as charFile:
            return [Year(*l.rstrip('\n').rsplit('\t')) for l in charFile if l[0]!='#']

    def __call__(self):
        printInCol('yellow',self._event)
        if raw_input()==self._year:
            ret = True
        else:
            printInCol('red','Wrong, the correct answer is '+self._year)
            ret = False
        return ret
    def getId(self):
        return 'years/'+self._event
