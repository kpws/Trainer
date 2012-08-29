import pylab as pl

def learningCurve(qdb):
    t=[i[0] for i in qdb.stats]
    known=[i[2] for i in qdb.stats]
    knownOrActive=[i[1]+i[2] for i in qdb.stats]
    tot=[len(qdb.tot) for i in qdb.stats]
    bottom=[0 for i in qdb.stats]
    pl.fill_between(t, bottom, known, facecolor='green')
    pl.fill_between(t, knownOrActive, tot, facecolor='red')
    pl.fill_between(t, known, knownOrActive, facecolor='yellow')
    pl.xlim(t[0],t[-1])
    pl.ylim(0,tot[0])
    pl.show()
