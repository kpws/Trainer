import os

import question
from colorPrint import printInCol

class Putonghua(question.Question):
    def __init__(self, char, pinyin, english):
        self.char=char
        self.english=english
        self.pinyin=pinyin

    @staticmethod
    def getQuestions():
        with open(os.path.join(os.path.dirname(__file__), 'data','putonghua'),'r') as charFile:
            return [Putonghua(*l.replace('\t','').rstrip('\n').rsplit(',')) for l in charFile if l[0]!='#']

    def __call__(self):
        printInCol('yellow',self.char)
        inp=raw_input()
        if inp.lower()==self.english.lower():
            ret = True
            printInCol('green','Correct!')
        else:
            printInCol('red','Wrong, the correct answer is '+self.english+'.')
            ret = False
        printInCol('blue','Pinyin: '+self.pinyin)
        return ret
    def getId(self):
        return 'putonghua/'+self.char
