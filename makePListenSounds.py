import os
from colorPrint import printInCol
from voice import get_google_voice

def charToFileName(c):
    return reduce(lambda a,b:a+b,[str(ord(x))+'_' for x in c])[:-1]+'.mp3'

if __name__=='__main__':
    with open(os.path.join(os.path.dirname(__file__), 'data','putonghua'),'r') as charFile:
        ql=[l.replace('\t','').rstrip('\n').rsplit(',') for l in charFile if l[0]!='#']
        for q in ql:
            print q[0]
            if get_google_voice(q[0],'zh-CN','data/putonghuaListen/'+charToFileName(q[0])):
                printInCol('green','Ok!')
            else:
                printInCol('red','Error!')
