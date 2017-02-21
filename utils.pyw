# -*- coding: utf8 -*-
import os, sys


def findCurrentDir():
    """
    @author: Gawein LE GOFF
    @author: Erwan CASTIONI
    @warning: Si cette fonction ne fonctionne pas correctement, utiliser os.path.dirname(os.path.abspath(foo)) au lieu de os.path.dirname(foo)
    
    Fonction retournant le dossier dans lequel le programme est situé et tirée de notre projet 'DementiaRL'.
    """
    
    if getattr(sys, 'frozen', False): #Si le programme a été "compilé" ("freeze") à l'aide de cx_Freeze, on ne peut pas utiliser la methode "habituelle" (celle dans le bloc else), il faut donc procéder autrement 
        datadir = os.path.dirname(sys.executable) #Puisque cx_Freeze génère un executable, on peut récupérer le dossier dans lequel l'executable est situé
    else:
        datadir = os.path.dirname(__file__)  #Si le programme n'a pas été compilé, on récupère à la place le dossier dans lequel est situé le fichier main.py
    return datadir

curDir = findCurrentDir()
assetsDir = os.path.join(curDir, "assets") #Correspond au dossier "assets"
imageDir = os.path.join(assetsDir, "images") #Correspond au dossier "assets/images"