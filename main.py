# -*- coding: utf8 -*-

import game, os, sys
from tkinter import *


def findCurrentDir():
    """
    @author: Gawein LE GOFF
    @author: Erwan CASTIONI
    
    Fonction retournant le dossier dans lequel le programme est situe et tiree de notre projet 'DementiaRL'.
    """
    
    if getattr(sys, 'frozen', False): #Si le programme a été "compile" ("freeze") à l'aide de cx_Freeze, on ne peut pas utiliser la methode "habituelle" (celle dans le bloc else), il faut donc proceder autrement 
        datadir = os.path.dirname(sys.executable) #Puisque cx_Freeze genere un executable, on peut recuperer le dossier dans lequel l'executable est situé
    else:
        datadir = os.path.dirname(__file__) 
    return datadir

root = Tk() #Initialisation de la fenètre principale
root.mainloop()