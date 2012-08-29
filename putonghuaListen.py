import os
import subprocess
import question
from colorPrint import printInCol
from makePListenSounds import charToFileName
class PutonghuaListen(question.Question):
    def __init__(self, char, pinyin, english):
        self._char=char
        self._answer=english
        self._pinyin=pinyin

    def printMessage(self):
        if not self._wasCorrect:
            printInCol('red','Wrong, the correct answer is: '+self._answer+'.')
        printInCol('blue','Character: '+self._char+'\nPinyin: '+self._pinyin)

    @staticmethod
    def getQuestions():
        with open(os.path.join(os.path.dirname(__file__), 'data','putonghua'),'r') as charFile:
            l=[PutonghuaListen(*l.replace('\t','').rstrip('\n').rsplit(',')) for l in charFile if l[0]!='#']
        r=[]
        u=[]
        for il in l:
            if not il._pinyin in u:
                u.append(il._pinyin)
                r.append(il)
        return r
    def pose(self):
        path=os.path.dirname(__file__)
        subprocess.Popen(('mpg123',path+'/data/putonghuaListen/'+charToFileName(self._char)),
                stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    def getId(self):
        return 'putonghuaListen/'+self._char
