# -*- coding: utf-8 -*-
"""
Module for keeping b logic for speaker object.
"""
import os
########################################################################
class Speaker(object):
    """Class for voicing string messages"""

    #----------------------------------------------------------------------
    def __init__(self, get_file_func, play_func):
        """
        Parameters:
        @get_file_func : delegate that will accept string to voice, and return audio file name.
        @play_func : delegate that plays music file(mp3, wav, e.t.c.).
        """
        
        self.get_file_func = get_file_func
        self.play_func = play_func    
            
    def voice(self, message):
        """ 
        Function that will voice our string message.
        Parameters:
        @message: message for voicing.
        """
            
        file = self.get_file_func(message)
        if file is not None:
            self.play_func(file)
