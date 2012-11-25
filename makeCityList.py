def getHitCount(query):
  #query = urllib.urlencode({'q': term})
  #url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
  #search_response = urllib.urlopen(url)
  #search_results = search_response.read()
  #results = json.loads(search_results)
  #data = results['responseData']
  #print data
  #return int(data['cursor']['estimatedResultCount'])
      
    import os, urllib, sys
    filename = 'http://www.google.com/search?q='+query
    cmd = os.popen("lynx -dump %s" % filename)
    output = cmd.read()
    cmd.close()
    #print output
    i=output.find(' of about ')
    if i==-1: return -1
    output=output[i+10:]
    i=output.find(' for ')
    if i==-1: return -1
    return int(output[:i].replace(',',''))

import time
import random
with open('bigCities.csv') as f:
    for l in f:
        q='"'+l[:-1]+'"'
        print(q+'\t'+str(getHitCount(q)))
        time.sleep(random.random()*2.)
