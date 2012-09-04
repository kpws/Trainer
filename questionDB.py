from time import time
import random

askAgainCorrect = 1*60*60
askAgainWrong = 4*60
knowTime = 3*24*60*60
actuallyKnownRatio=0.95
measurePrec=0.05
maxNewPerSession=10

qMode = {0:'untried', 1:'active', 2:'known'}
fileWords = {'0':False, '1':True}
toFileWords = dict([(fileWords[k], k) for k in fileWords])

class QuestionHist():
    def __init__(self):
        self.hist=[]

    def add(self, correct, time):
       self.hist.append((correct,time))

    def lastTime(self):
        return self.hist[-1][1]

    def lastCorrect(self):
        return self.hist[-1][0]

    def untried(self):
        return len(self.hist)==0
    
    def known(self):
        if self.untried():
            return False
        lwt=[h[1] for h in self.hist if not h[0]]
        if lwt==[]:
            return True
        lct=[h[1] for h in self.hist if h[0]]
        if lct==[]:
            return False
        return lct[-1] - lwt[-1] > knowTime

    def active(self):
        return not self.untried() and not self.known()

    def getMode(self):
        if self.untried(): return 0
        elif self.known(): return 2
        else: return 1

class QuestionDB():
    def __init__(self, questions, histFile):
        self.histFile=histFile
        self.hist=[l.rstrip('\n').rsplit('\t') for l in self.histFile if not '#' in  l[0]]
        for h in self.hist:
            h[1] = fileWords[h[1]]
            h[2] = float(h[2])
        self.makeSets(questions)

    def writeHist(self, qId, result):
        ct=time()
        self.histFile.write(qId+'\t'+toFileWords[result]+'\t'+str(ct)+'\n')
        self.hist.append((qId,result,ct))
        self.tot[qId].add(result, ct)
        self.updateSets(qId)
        self.stats.append((ct, len(self.active), len(self.known)))
        if len(self.stats)>=2:
            oldActive=self.stats[-2][1]
            oldKnown=self.stats[-2][2]
        else:
            oldActive=0
            oldKnown=0
        return (self.stats[-1][1]-oldActive, self.stats[-1][2]-oldKnown)

    def undo(self):
        self.histFile.seek(-2,2)
        while self.histFile.read(1)!='\n':
            self.histFile.seek(-2,1)
        self.histFile.truncate()
        ret=self.hist.pop(-1)[0]
        self.tot[ret].hist.pop(-1)
        if len(self.stats)>=2:
            dActive=self.stats[-2][1]-self.stats[-1][1]
            dKnown=self.stats[-2][2]-self.stats[-1][2]
        else:
            dActive=-self.stats[-1][1]
            dKnown=-self.stats[-1][2]
        self.updateSets(ret)
        self.stats.pop()
        return (ret, dActive, dKnown)

    def makeSets(self, questions):
        self.tot=dict([(q, QuestionHist()) for q in questions])
        self.untried=dict([(q, QuestionHist()) for q in questions])
        self.active={}
        self.known={}
        self.sets=(self.untried, self.active, self.known)
        self.stats=[]
        for h in self.hist:
            self.tot[h[0]].add(*h[1:])
            self.updateSets(h[0])
            self.stats.append((h[2], len(self.active), len(self.known)))

    def updateSets(self,key):
        if key in self.active:
            del self.active[key]
        if key in self.known:
            del self.known[key]
        if key in self.untried:
            del self.untried[key]
        self.sets[self.tot[key].getMode()][key]=self.tot[key]

    def getQuestion(self):
        last=None
        ct=time()
        for k,q in self.active.items():
            s=(ct-q.lastTime())/(askAgainCorrect if q.lastCorrect() else askAgainWrong)
            if s>=1 and (last==None or s>last[1]):
                    last=(k,s)
        if last==None:
            return self.getNonActive()
        else:
            return last[0]
                    
    def getNonActive(self):
        return random.choice(self.untried.keys())
