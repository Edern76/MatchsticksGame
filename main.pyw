#!/usr/bin/env python3
# -*- coding: utf8 -*-

import os, sys, name, threading
sys.path.append(os.path.dirname(__file__))
from utils import curDir, assetsDir, imageDir
from tkinter import *


root = Tk() #Initialisation de la fenètre principale
root.geometry("400x600+0+0") #Réglage de la résolution de la fenêtre principale
root.title("Ryuga no Allumette | Menu")

if sys.platform.startswith('win') or sys.platform.startswith('win32') or sys.platform.startswith('win64'):
    pythonCommand = 'python'
else:
    pythonCommand = 'python3'

############Creation de l'image############
photo = PhotoImage(file= os.path.join(imageDir, "logo_sd.png")) #On accède à l'image nommée "logo_sd.png" dans le dossier des images
logoFrame = Frame(root, width = 400, height = photo.height()) #On crée une frame occupant toute la largeur de l'écran destinée à contenir l'image
canvas = Canvas(logoFrame, width= photo.width(), height= photo.height()) #On crée un canvas dans cette frame ayant les dimensions de l'image
canvas.create_image(0, 0, anchor=NW, image=photo) #On crée l'image dans le canvas
canvas.place(height = photo.height(), width = photo.width(), x = 75) #On place le canvas à 125 pixels du bord gauche de la frame (afin de donner l'impression que l'image est centrée)
logoFrame.grid(row = 0, column = 0, sticky = NW, columnspan = 3) #On place la frame contenant l'image dans la fenêtre principale selon une grille, et on lui fait occuper trois colonnes de cette grille
###########################################

class SingleplayerStarter(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        fenetreNom = Toplevel(root)
        nomRetourne = name.askSimpleName(fenetreNom, root)
        print(nomRetourne)
        if nomRetourne is not None:
            shellCommand = pythonCommand + " game.pyw 0 " + nomRetourne
            os.system(shellCommand)
        else:
            pass

class MultiplayerStarter(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        fenetreNom = Toplevel(root)
        tupleRetourne = name.askMultipleNames(fenetreNom, root)
        if tupleRetourne is not None:
            nom1, nom2 = tupleRetourne
            shellCommand = pythonCommand + " game.pyw 1 " + nom1 + " " + nom2
            os.system(shellCommand)
        else:
            pass

############Création du menu###############
menuFrame = Frame(root) #On crée une frame contenant les éléments du menu
solo = SingleplayerStarter()
multi = MultiplayerStarter()
bouton1 = Button(menuFrame, text = "Jouer contre l'IA", command = solo.start)
bouton2 = Button(menuFrame, text = "Jouer contre un autre joueur", command = multi.start)
bouton1.pack()
bouton2.pack()
menuFrame.grid(row = 4, column = 1) #On place cette frame dans la colonne centrale et quelques lignes en dessous de la frame précédente
###########################################

colNum, rowNum = root.grid_size() #On récupère le nombre de colonnes et de lignes de la grille (le nombre de colonnes n'est pas utilisé, mais on doit le récupérer pour récupérer le nombre de lignes puisque la méthode grid_size() renvoie un tuple de deux éléments où le nombre de lignes est en deuxième position)
for x in range(rowNum):
    root.grid_rowconfigure(x, minsize = 20) #On fait en sorte que les lignes vides aient une hauteur de 20 pixels. Sinon, elles ont par défaut une hauteur de 0 pixel et ne sont pas affichées (et on ne pourrait par conséquent pas espacer les frames)

root.mainloop()