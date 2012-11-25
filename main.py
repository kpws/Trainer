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

import time, os, sys
from random import random, randrange
from colorPrint import printInCol
import plot
import questionDB
import readline

silent='-s' in sys.argv

#add categories here
cats=[]
import putonghuaListen, putonghua, year, country, city
cats.append(putonghuaListen.PutonghuaListen)
cats.append(putonghua.Putonghua)
cats.append(year.Year)
cats.append(country.Country)
cats.append(city.City)

#Load questions
questions={}
for c in cats:
    if silent and hasattr(c,'hasSound') and c.hasSound:
        continue
    for q in c.getQuestions():
        if q.getId() in questions:
            raise Exception('Two questions with same id loaded. Id: '+q.getId())
        questions[q.getId()]=q

def printStats(qdb):
    print('')
    printInCol('green','Learnt this session: '+str(learnt))
    printInCol('red','Forgotten this session: '+str(forgotten)+'\n')
    printInCol('blue','Total: '+str(len(qdb.tot)))
    r,low,up=qdb.getActuallyKnownRatio()
    printInCol('green','Known, [%.0f%%'%(low*100)+', %.0f%%]'%(up*100)+' %d%% c.i.: '%(questionDB.conf*100)+str(len(qdb.known)))
    printInCol('yellow','Active: '+str(len(qdb.active)))
    printInCol('red','Never tried: '+str(len(qdb.untried)))

with open(os.path.expanduser('~/.trainerHist'),'a+') as histFile:
    qdb=questionDB.QuestionDB(questions, histFile)
    learnt=0
    forgotten=0
    running=True
    oldQId=None
    while running:
        qId=qdb.getQuestion()
        while True:
            questions[qId].pose()
            try:
                inp=raw_input()
            except (KeyboardInterrupt, EOFError):
                running=False
                break
            if len(inp)>0 and inp[0]==':':
                command=inp[1:]
                if command=='again':
                    continue
                elif command=='exit':
                    running=False
                    break
                elif command=='stat':
                    printStats(qdb)
                elif command=='undo':
                    if len(qdb.hist)==0:
                        printInCol('red','No answers to undo...')
                if len(inp)>0 and inp[0]==':':
                    command=inp[1:]
                    if command in ['again', 'a']:
                        continue
                    if command in ['last', 'l']:
                        if oldQId==None:
                            printInCol('red','This was the first question during this session...')
                        else:
                            qId=oldQId
                    elif command=='exit':
                        running=False
                        break
                    elif command=='stat':
                        printStats(qdb)
                    elif command in ['undo','u']:
                        if len(qdb.hist)==0:
                            printInCol('red','No answers to undo...')
                        else:
                            undoId, dActive, dKnown=qdb.undo()
                            if dKnown==-1:
                                learnt=max(0,learnt-1)
                            elif dKnown==1:
                                forgotten=max(0,forgotten-1)
                            else:
                                assert(dKnown==0)
                            printInCol('blue','Undid question: '+undoId)
                    elif command=='plot':
                        plot.learningCurve(qdb)
                    else:
                        printInCol('red','Unknown command: '+command)
                elif command=='plot':
                    plot.learningCurve(qdb)
                else:
                    printInCol('red','Unknown command: '+command)
            else:
                if inp=='.':
                    dActive,dKnown=qdb.writeHist(qId, True)
                    if dKnown==1:
                        learnt+=1
                    else:
                        assert(dKnown==0)
                else:
                    if questions[qId].verify(inp):
                        printInCol('green','Correct!')
                        dActive,dKnown=qdb.writeHist(qId, True)
                        if dKnown==1:
                            learnt+=1
                        else:
                            assert(dKnown==0)
                    else:
                        #It is the questions responsibility to tell the user shle was wrong
                        #and inform on whats correct in q.printMessage()
                         dActive,dKnown=qdb.writeHist(qId, False)
                         if dKnown==-1:
                             forgotten+=1
                         else:
                             assert(dKnown==0)
                    questions[qId].printMessage()
                break
            print('')
        oldQId=qId
    try:
        printStats(qdb)
    except (KeyboardInterrupt, EOFError):
        printInCol('green','Ok, got it!! You want to leave NOW.')
    finally:
        printInCol('turquoise','Goodbye!')
