import os
import speak
import question
from colorPrint import printInCol

class PutonghuaListen(question.Question):
    def __init__(self, char, pinyin, english):
        self.char=char
        self.english=english
        self.pinyin=pinyin

    @staticmethod
    def getQuestions():
        with open(os.path.join(os.path.dirname(__file__), 'data','putonghua'),'r') as charFile:
            return [PutonghuaListen(*l.replace('\t','').rstrip('\n').rsplit(',')) for l in charFile if l[0]!='#']

    def __call__(self):
        while True:
            printInCol('yellow',"Listen and write in english, type :again to here again.")
            speak.speak(self.char)
            inp=raw_input()
            if inp==':again':
                continue
            elif inp==self.english:
                ret = True
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
