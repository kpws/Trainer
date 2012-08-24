import pylab as pl
from trainer import correct, wrong
def learningCurve(hist):
    d={}
    for h in hist:
        if h[1]==str(wrong): continue
        if h[0] in d:
            d[h[0]]+=1
        else:
            d[h[0]]=0
    vals=d.values()
    vals.sort()
    pl.plot(vals)
    pl.show()
