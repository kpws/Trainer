import os

import question
from colorPrint import printInCol

class Year(question.Question):
    def __init__(self, event, year):
        self._question=event
        self._answer=year

    @staticmethod
    def getQuestions():
        with open(os.path.join(os.path.dirname(__file__), 'data','year'),'r') as charFile:
            return [Year(*l.rstrip('\n').rsplit('\t')) for l in charFile if l[0]!='#']

    def getId(self):
        return 'year/'+self._question
