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
import plot
from questionDB import QuestionDB
import readline

#add categories here
cats=[]
import putonghuaListen, putonghua, year, country
cats.append(putonghuaListen.PutonghuaListen)
cats.append(putonghua.Putonghua)
cats.append(year.Year)
cats.append(country.Country)

#Load questions
questions={}
for c in cats:
    for q in c.getQuestions():
        if q.getId() in questions:
            raise Exception('Two questions with same id loaded. Id: '+q.getId())
        questions[q.getId()]=q

def printStats(qdb):
    print('')
    printInCol('blue','Total: '+str(len(qdb.tot)))
    printInCol('green','Known: '+str(len(qdb.known)))
    printInCol('yellow','Active: '+str(len(qdb.active)))
    printInCol('red','Never tried: '+str(len(qdb.untried)))

with open(os.path.expanduser('~/.trainerHist'),'a+') as histFile:
    qdb=QuestionDB(questions, histFile)
    running=True
    while running:
        qId=qdb.getQuestion()
        try:
            while True:
                questions[qId].pose()
                inp=raw_input()
                if len(inp)>0 and inp[0]==':':
                    command=inp[1:]
                    if command in ['again', 'a']:
                        continue
                    elif command=='exit':
                        running=False
                        break
                    elif command=='stat':
                        printStats(qdb)
                    elif command=='undo':
                        if len(qdb.hist)==0:
                            printInCol('red','No answers to undo...')
                        else:
                            printInCol('blue','Undid question: '+qdb.undo())
                    elif command=='plot':
                        plot.learningCurve(qdb)
                    else:
                        printInCol('red','Unknown command: '+command)
                else:
                    if inp=='.':
                        qdb.writeHist(qId, True)
                    else:
                        if questions[qId].verify(inp):
                            printInCol('green','Correct!')
                            qdb.writeHist(qId, True)
                        else:
                            #It is the questions responsibility to tell the user shle was wrong
                            #and inform on whats correct in q.printMessage()
                            qdb.writeHist(qId, False)
                        questions[qId].printMessage()
                    break
        except (KeyboardInterrupt, EOFError):
            running=False
        finally:
            print('')
    try:
        printStats(qdb)
    except (KeyboardInterrupt, EOFError):
        printInCol('green','Ok, got it!! You want to leave NOW.')
    finally:
        printInCol('turquoise','Goodbye!')
