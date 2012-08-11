''' Copyright 2011 Petter Saeterskog

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.'''

import time, os
from random import random, randrange
from colorPrint import printInCol

correct=1
wrong=0
cats=[]

import putonghuaListen
cats.append(putonghuaListen.PutonghuaListen)
import putonghua
cats.append(putonghua.Putonghua)
import year
cats.append(year.Year)
import country
cats.append(country.Country)

questions=[]
for c in cats:
    questions+=c.getQuestions()

with open(os.path.expanduser('~/.trainerHist'),'a+') as histFile:
    hist=[l.rstrip('\n').rsplit('\t') for l in histFile]
    def writeHist(qId,result):
                ct=time.time()
                wr=str([wrong,correct][int(result)])
                histFile.write(qId+'\t'+wr+'\t'+str(ct)+'\n')
                hist.append([qId,wr,ct])

    lastTime=lambda qId,p:max([float(h[2]) for h in hist if h[:2]==[qId,str(p)]]+[-1])
    active=lambda qId:lastTime(qId,wrong)!=-1 or lastTime(qId,correct)!=-1
    probDecay=lambda qId:max(min(0.5*len(chars),5e4/(lastTime(qId,correct)-lastTime(qId,wrong))),1.0)
    prob=lambda qId:(2.0*len(chars) if lastTime(qId,correct)<lastTime(qId,wrong) else probDecay(qId)) if active(qId) else 1.0
    getQ=lambda n=20,r=0,i=0:getQ(n=n-1,r=randrange(len(questions)),i=r if random()<prob(r)/prob(i) else i) if n else i
    while True:
        i=getQ()
        try:
            writeHist(questions[i].getId(),questions[i]())
        except KeyboardInterrupt:
            countType=lambda t:sum(1 for i in range(len(questions)) if t(questions[i].getId()))
            printInCol('blue','\nTotal: '+str(countType(lambda i:correct)))
            printInCol('green','Known: '+str(countType(lambda i:lastTime(i,correct)-lastTime(i,correct)>5e4)))
            printInCol('yellow','Used: '+str(countType(active)))
            printInCol('red','Never correct: '+str(countType(lambda i:lastTime(i,correct)==-1)))
            printInCol('turquoise','Goodbye!')
            break
