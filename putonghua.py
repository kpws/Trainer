import os

import question
from colorPrint import printInCol

class Putonghua(question.Question):
    def __init__(self, char, pinyin, english):
        self._pinyin=pinyin
        self._question=char
        self._answer=english

    @staticmethod
    def getQuestions():
        with open(os.path.join(os.path.dirname(__file__), 'data','putonghua'),'r') as charFile:
            return [Putonghua(*l.replace('\t','').rstrip('\n').rsplit(',')) for l in charFile if l[0]!='#']

    def printMessage(self):
        if not self._wasCorrect:
            printInCol('red','Wrong, this character is in English: '+self._answer+'.')
        printInCol('blue','Pinyin: '+self._pinyin)

    def getId(self):
        return 'putonghua/'+self._question
