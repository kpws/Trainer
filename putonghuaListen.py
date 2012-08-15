import os
import subprocess
import question
from colorPrint import printInCol
from makePListenSounds import charToFileName
class PutonghuaListen(question.Question):
    def __init__(self, char, pinyin, english):
        self.char=char
        self.english=english
        self.pinyin=pinyin

    @staticmethod
    def getQuestions():
        with open(os.path.join(os.path.dirname(__file__), 'data','putonghua'),'r') as charFile:
            l=[PutonghuaListen(*l.replace('\t','').rstrip('\n').rsplit(',')) for l in charFile if l[0]!='#']
        r=[]
        u=[]
        for il in l:
            if not il.pinyin in u:
                u.append(il.pinyin)
                r.append(il)
        return r
    def __call__(self):
        while True:
            subprocess.Popen(('mpg123','data/putonghuaListen/'+charToFileName(self.char)),
                    stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            inp=raw_input()
            if inp==':again':
                continue
            elif inp==self.english:
                ret = True
                printInCol('green','Correct!')
                break
            else:
                printInCol('red','Wrong, the correct answer is '+self.english)
                ret = False
                break
        printInCol('blue','Pinyin: '+self.pinyin)
        printInCol('blue','Character: '+self.char)
        return ret
    def getId(self):
        return 'putonghuaListen/'+self.char
