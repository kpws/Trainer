# -*- coding: utf-8 -*-
#File made by Alexander Mostovenko, edited by petter
"""
Module for voicing string data.
"""
import urllib
import urllib2
import subprocess
import os
#----------------------------------------------------------------------
def get_google_voice(phrase,language,file_name):
    """
    Function that will send http request to google translate
    and save audio file from responce with voiced input phrase.
    Parameters:
    @phrase: phrase to voice.
    Returns:
    If ok - name of created file, else - returns None.
    """
    
    #language='zh-CN' #Setting language.  ##Changed language to chinese putonghua here
    url = "http://translate.google.com/translate_tts" #Google translate url for getting sound.
    user_agent="Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5." 
    #file_name="/tmp/tempForSpeak.mp3" #Temp file for saving our voiced phrase.

    params = urllib.urlencode({'q':phrase, 'tl':language}) #query parameters.
    request = urllib2.Request(url, params) #http request.
    request.add_header('User-Agent', user_agent) #adding agent as header.
    response = urllib2.urlopen(request) 
    
    if response.headers['content-type'] == 'audio/mpeg':
        with open(file_name, 'wb') as file:
            file.write(response.read())
        return True
    else:
        return False
