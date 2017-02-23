#!/usr/bin/env python3
# -*- coding: utf8 -*-

import os, sys, name, threading, webbrowser, game
sys.path.append(os.path.dirname(__file__)) #Pour éviter des erreur sous UNIX
from utils import curDir, assetsDir, imageDir
from tkinter import *


root = Tk() #Initialisation de la fenètre principale
screenWidth = root.winfo_screenwidth() #Récupération de la résolution de l'écran
screenHeight = root.winfo_screenheight() #Récupération de la résolution de l'écran
startX = screenWidth // 2 - 200 #Détermination des coordonnées telles que la fenêtre soit au centre de l'écran
startY = screenHeight // 2 - 250 #Détermination des coordonnées telles que la fenêtre soit au centre de l'écran
root.geometry("400x500+{}+{}".format(startX, startY)) #Réglage de la résolution de la fenêtre principale
root.title("Ryuga no Allumette | Menu")


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
        self._stop = threading.Event()
        
    def stop(self):
        self._stop.set()
        
    def run(self):
        fenetreNom = Toplevel(root)
        nomRetourne = name.askSimpleName(fenetreNom, root)
        print(nomRetourne)
        if nomRetourne is not None:
            fenetreJeu = Toplevel(root)
            game.main(0, fenetreJeu, nomRetourne)
        else:
            pass
        self.stop()

class MultiplayerStarter(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._stop = threading.Event()
    
    def stop(self):
        self._stop.set()
        
    def run(self):
        fenetreNom = Toplevel(root)
        tupleRetourne = name.askMultipleNames(fenetreNom, root)
        if tupleRetourne is not None:
            nom1, nom2 = tupleRetourne
            fenetreJeu = Toplevel(root)
            game.main(1, fenetreJeu, name1 = nom1, name2 = nom2)
        else:
            pass
        self.stop()
        
def startSolo():
    solo = SingleplayerStarter()
    solo.start()
    
def startMulti():
    multi = MultiplayerStarter()
    multi.start()   
############Création du menu###############
menuFrame = Frame(root) #On crée une frame contenant les éléments du menu
bouton1 = Button(menuFrame, text = "Jouer contre l'IA", command = startSolo)
bouton2 = Button(menuFrame, text = "Jouer contre un autre joueur", command = startMulti)
bouton1.pack()
bouton2.pack(pady = 2)
menuFrame.grid(row = 4, column = 1) #On place cette frame dans la colonne centrale et quelques lignes en dessous de la frame précédente

menuFrame2 = Frame(root)
gitBouton = Button(menuFrame2, text = "Page GitHub", command = lambda : webbrowser.open("https://github.com/Edern76/MatchsticksGame", new = 2))
bouton3 = Button(menuFrame2, text = "Quitter", command = root.destroy)
gitBouton.pack()
bouton3.pack(pady = 2)
menuFrame2.grid(row = 7, column = 1)

creditsLabel = Label(root, text = "Erwan CASTIONI et Gawein LE GOFF", fg = "gray")
licenseLabel = Label(root, text = "License MIT", fg = 'gray')
creditsLabel.place(relx = 0, rely = 0.965)
licenseLabel.place(relx = 0.825, rely = 0.963)
###########################################

colNum, rowNum = root.grid_size() #On récupère le nombre de colonnes et de lignes de la grille (le nombre de colonnes n'est pas utilisé, mais on doit le récupérer pour récupérer le nombre de lignes puisque la méthode grid_size() renvoie un tuple de deux éléments où le nombre de lignes est en deuxième position)
for x in range(rowNum):
    root.grid_rowconfigure(x, minsize = 20) #On fait en sorte que les lignes vides aient une hauteur de 20 pixels. Sinon, elles ont par défaut une hauteur de 0 pixel et ne sont pas affichées (et on ne pourrait par conséquent pas espacer les frames)

root.mainloop()