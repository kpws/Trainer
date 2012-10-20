from time import time
import random
import numpy as np
from scipy.special import btdtri

askAgainCorrect = 1*60*60 #sec
askAgainWrong = 4*60 #sec
knowTime = 3*24*60*60 #sec
actuallyKnownRatio=0.95
conf=0.95
actuallyKnownTime= 2*7*24*60*60 #sec
auxWrongTime=365*24*60*60 #sec

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

    def knownRatio(self,t):
        lwt=[h[1] for h in self.hist if not h[0]]
        if lwt==[]:
            lwt=[auxWrongTime]
        lct=[h[1] for h in self.hist if h[0]]
        assert(lct!=[])
        return (t-lwt[-1])/(t-lct[-1])

    def active(self):
        return not self.untried() and not self.known()

    def getMode(self):
        if self.untried(): return 0
        elif self.known(): return 2
        else: return 1

class QuestionDB():
    def __init__(self, questions, histFile):
        self.actuallyKnownHist=[]
        self.histFile=histFile
        self.hist=[l.rstrip('\n').rsplit('\t') for l in self.histFile if not '#' in  l[0]]
        for h in self.hist:
            h[1] = fileWords[h[1]]
            h[2] = float(h[2])
        self.makeSets(questions)

    def writeHist(self, qId, result, outputDiff=True, ct=None, writeFile=True):
        if ct==None:
            ct=time()
        if writeFile:
            self.histFile.write(qId+'\t'+toFileWords[result]+'\t'+str(ct)+'\n')
            self.hist.append((qId,result,ct))
        wasKnown=self.tot[qId].known()
        self.tot[qId].add(result, ct)
        if wasKnown:
            self.actuallyKnownHist.append((self.tot[qId].known(),ct))
        self.updateSets(qId)
        self.stats.append((ct, len(self.active), len(self.known)))
        if outputDiff:
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
        if self.tot[ret].known():
            self.actuallyKnownHist.pop(-1)
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
            self.writeHist(h[0],h[1],ct=h[2],writeFile=False,outputDiff=False)
            #self.tot[h[0]].add(*h[1:])
            #self.updateSets(h[0])
            #self.stats.append((h[2], len(self.active), len(self.known)))

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
    def getActuallyKnownRatio(self, ct=None):
        if ct==None:
            ct=time()
        tot=sum(1 for v,t in self.actuallyKnownHist if t>ct-actuallyKnownTime)
        actuallyKnown=sum(1 for v,t in self.actuallyKnownHist if t>ct-actuallyKnownTime and v)
        if tot==0:
            return 0., 0., 1.
        else:
            r=float(actuallyKnown)/tot
            alpha=1-conf
            return (r,0. if actuallyKnown==0 else btdtri(actuallyKnown,tot-actuallyKnown+1,alpha/2),
                    1. if actuallyKnown==tot else btdtri(actuallyKnown+1,tot-actuallyKnown,1-alpha/2))

    def getNonActive(self):
        a,b,c=self.getActuallyKnownRatio()
        if b<actuallyKnownRatio or len(self.untried)==0:
            ratio=float('inf')
            ct=time()
            for k in self.known.keys():
               tRatio=self.known[k].knownRatio(ct)
               if tRatio<ratio:
                   worst=k
                   ratio=tRatio
            return worst
        else:
            return random.choice(self.untried.keys())
