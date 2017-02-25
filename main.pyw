#!/usr/bin/env python3
# -*- coding: utf8 -*-

#Merci de ne SURTOUT PAS modifier les lignes ci-dessus. Elles sont utilisées par Python, et ne sont pas juste de simples commentaires.

import os, sys, name, threading, webbrowser, game
sys.path.append(os.path.dirname(__file__)) #Pour éviter des erreur sous UNIX, on ajoute le dossier actuel au chemin dans lequel Python recherche ses modules.
from utils import curDir, assetsDir, imageDir
from tkinter import *

'''
Ce programme a été divisé en modules, pour permettre une lecture plus claire. Ils sont importables comme n'importe quel module, à ceci près qu'ils doivent se trouver dans le même dossier que main.pyw, ou tout autre fichier Python nécéssitant de les importer.
Ceux-ci sont :
    - main.pyw : Celui dans lequel vous vous trouvez actuellement. Contient le menu principal. L'extension .pyw permet d'empêcher la console de s'ouvrir. Il s'agit du module à exécuter pour accéder au programme.
    - game.py : Contient l'interface et la logique du jeu en lui même. Il s'agit du coeur du programme
    - name.py : Contient les interfaces et les fonctions permettant de récupérer le ou les nom(s) du ou des utilisateur(s), pour pouvoir ensuite les afficher.
    - utils.py : Contient une fonction permettant de récupérer le chemin du dossier dans lequel se trouve le programme, ainsi que des variables utilisant cette fonction et correspondant aux différents dossier auxquels le programme a besoin d'accéder
    
Ce programme nécessite également des images, réalisées par nous mêmes sous GIMP. Celles-ci sont trouvables dans le dossier ./assets/images. Certaines d'entre elles sont des concepts, n'ayant pas été retenus pour la version finale.
Par conséquent, merci de vous assurer que vous possédez bien ce dossier dans le répertoire contenant ce fichier, et que tous les modules aient les permissions nécessaires pour y accéder, sans quoi des erreurs et des plantages peuvent survenir.
Dans le dossier ./assets/images/gimp, vous trouverez les fichiers .xcf, utilisés lors de la conception des images.

Certaines fonctions ou classes possèdent un bloc de texte tel que celui-ci, délimité par trois apostrophes au début et à la fin. Ce bloc correspond à la description de cette fonction ou cette classe.
Dans ces blocs, vous pourrez trouver des parties délimitées par des @. Elles correspondent à un certain type d'information. Par exemple, @type var correspond au type attendu de la variable var, et @param var correspond à la description de la variable var.

Ce programme a été testé sous Windows 10 64 bits et Ubuntu 64 bits. Il devrait en théorie fonctionner sous des machines exécutant OSX et/ou un système d'exploitation en 32 bits, mais n'ayant pas accès chez nous à des machines de ce type, nous n'avons pas pu nous en assurer.

Ce programme est sous license MIT, car nous avons trouvé que c'est une license très simple et permissive, qui s'adapte bien à un petit projet comme celui-ci. Pour plus d'information, merci de vous référer au fichier LICENSE.

Ce programme a été réalisé dans le cadre d'une consigne donnée en cours d'ISN, par nos professeurs Mme Cribier, Mr Delacour et Mr Le Jan.


Sur ce, nous vous souhaitons une agréable expérience avec notre programme

@author: CASTIONI Erwan
@author: LE GOFF Gawein

@date : Janvier 2017
'''


'''
@param Thread : Aussi appelé 'tâche'. Il s'agit d'une série d'instructions s'éxecutant en parallèle du reste du code. En effet, en temps normal Python exécute le code de façon linéaire, une instruction plus bas dans le code ne s'exécute pas tant que les instructions situées plus haut ne se sont pas exécutées : une seule instruction est donc exécutée en même temps. Le fait d'utiliser des threads permet d'avoir plusieurs instructions s'exécutant parallèlement, soit en même temps. Nous avons principalement appris à nous servir de ces threads grâce à cette page : https://openclassrooms.com/courses/apprenez-a-programmer-en-python/la-programmation-parallele-avec-threading
@param Classe : 'Moule' (ou 'Modèle', termes de vulgarisation donc non exacts) permettant de créer des objets (appelés des instances de cette classe), possédant leurs propres variables indépendantes de celles des autres objets (attributs) et leurs propres fonctions (méthodes), appelées en écrivant nomDeLinstance.nomDeLaMethode(args). Les classes permettent donc de définir un type d'objets, en indiquant quels types d'attributs ils possèderont et à quelles méthodes ils auront accès. Notez qu'en Python, les variables, les fonctions, les listes et autres sont des objets dépendant de classes : ainsi donc, quand on crée une liste par exemple, on crée en réalité une instance de la classe 'Liste' (qui ne s'appelle probablement pas 'Liste' en réalité, mais j'ignore son nom exact), ce qui explique que l'on puisse écrire 'maListe.append()', car append() est une méthode de la classe liste.
@param Constructeur : Méthode nommée '__init__' d'une classe, et executée lors de la création d'une instance de cette classe. Chaque classe doit posséder un constructeur.
@param Héritage : Fait qu'une classe puisse être construite d'après une autre classe (il s'agit donc d'une sorte de 'sous-classe'). Une classe héritant d'une classe mère aura accès aux méthodes et attributs de sa classe mère. Si l'on déclare dans la classe fille une méthode du même nom qu'une méthode de la classe mère, la méthode de la classe fille aura la priorité sur celle de la classe mère, et remplacera donc celle de la classe mère (dans la classe fille uniquement). Pour faire hériter une classe A d'une classe B, on met le nom de la classe B entre parenthèses après celui de la classe A; comme ceci : class A(B). Afin de faire en sorte qu'une série d'instructions s'exécute dans un Thread, il faut la placer dans la méthode run() d'une classe héritant de la classe Thread.
'''

root = Tk() #Initialisation de la fenètre principale. /!\ ATTENTION /!\ : N'appeler Tk() (et mainloop()) QU'UNE SEULE FOIS au cours d'un programme, utiliser Toplevel() (sans mainloop()) pour créer d'autres fenêtres. 
screenWidth = root.winfo_screenwidth() #Récupération de la résolution de l'écran
screenHeight = root.winfo_screenheight() #Récupération de la résolution de l'écran
startX = screenWidth // 2 - 200 #Détermination des coordonnées telles que la fenêtre soit au centre de l'écran
startY = screenHeight // 2 - 250 #Détermination des coordonnées telles que la fenêtre soit au centre de l'écran
root.geometry("400x500+{}+{}".format(startX, startY)) #Réglage de la résolution de la fenêtre principale
root.title("Ryuga no Allumette | Menu") #Réglage du tire de la fenêtre principale.


############Creation de l'image############
photo = PhotoImage(file= os.path.join(imageDir, "logo_sd.png")) #On accède à l'image nommée "logo_sd.png" dans le dossier des images
logoFrame = Frame(root, width = 400, height = photo.height()) #On crée une frame occupant toute la largeur de l'écran destinée à contenir l'image
canvas = Canvas(logoFrame, width= photo.width(), height= photo.height()) #On crée un canvas dans cette frame ayant les dimensions de l'image
canvas.create_image(0, 0, anchor=NW, image=photo) #On crée l'image dans le canvas
canvas.place(height = photo.height(), width = photo.width(), x = 75) #On place le canvas à 125 pixels du bord gauche de la frame (afin de donner l'impression que l'image est centrée)
logoFrame.grid(row = 0, column = 0, sticky = NW, columnspan = 3) #On place la frame contenant l'image dans la fenêtre principale selon une grille (çad un tableau, que l'on peut comparer par son fonctionnement à celui qu'utilisent les tableurs), et on lui fait occuper trois colonnes de cette grille
###########################################

class SingleplayerStarter(threading.Thread):
    '''
    Permet de lancer le mode joueur contre IA. On utilise un thread car sinon la fenêtre ne s'affiche pas
    '''
    def __init__(self):
        threading.Thread.__init__(self) #Initialisation de la classe Thread dont la classe SingleplayerStarter hérite
        self._stop = threading.Event()
        
    def stop(self):
        self._stop.set() #Arrêt du Thread
        
    def run(self):
        '''
        Remplace la méthode run héritée de la classe Thread, et est appelée lorsque l'on appelle la méthode start.
        Voir fichier name.py pour la fonction askSimpleName (et askMultipleNames)
        '''
        fenetreNom = Toplevel(root) #On crée une autre fenêtre, destinée à demander le nom du joueur. On ne doit en effet SURTOUT PAS appeler Tk() ou mainloop() plus d'une fois par application
        nomRetourne = name.askSimpleName(fenetreNom, root) #On demande le nom du joueur
        if nomRetourne is not None: #Si l'utilisateur a cliqué sur OK
            fenetreJeu = Toplevel(root) #On crée une nouvelle fenêtre, accueillant le jeu en lui même.
            game.main(0, fenetreJeu, nomRetourne) #On démarre le jeu en mode 1 joueur, en indiquant qu'il faut qu'il s'attache à la fenêtre précédemment crée et en lui indiquant le nom du joueur
        else: #Si l'utilisateur a cliqué sur Annuler
            pass #On n'effectue aucune action, on revient donc au menu principal
        self.stop() #On arrête le thread

class MultiplayerStarter(threading.Thread):
    '''
    Idem que pour singleplayer starter, mais en mode Joueur contre joueur
    '''
    def __init__(self):
        threading.Thread.__init__(self)
        self._stop = threading.Event()
    
    def stop(self):
        self._stop.set()
        
    def run(self):
        fenetreNom = Toplevel(root)
        tupleRetourne = name.askMultipleNames(fenetreNom, root)
        if tupleRetourne is not None:
            nom1, nom2 = tupleRetourne # On assigne nom1 et nom2 respectivement à la première et à la deuxième (et dernière) valeur du tuple retourné par la fonction askMultipleNames
            fenetreJeu = Toplevel(root)
            game.main(1, fenetreJeu, name1 = nom1, name2 = nom2)
        else:
            pass
        self.stop()
        
def startSolo():
    '''
    Plutôt que de créer une instance de SinglePlayer à la racine du programme et de la lancer directement en cliquant sur un bouton, on associe ces deux actions à une fonction.
    Cela permet de créer un nouveau Thread à chaque clic sur le bouton, (un Thread ne peut être lancé qu'une seule fois), et donc de pouvoir jouer plusieurs fois sans avoir à relancer le programme entre temps.
    '''
    solo = SingleplayerStarter()
    solo.start() #On appelle la méthode start de l'instance 'solo' de la classe 'SingleplayerStarter', héritée de la classe Thread, qui elle même appelle la méthode run (on exécute donc le code contenu dans la méthode run)
    
def startMulti():
    '''
    Idem que pour startSolo
    '''
    multi = MultiplayerStarter()
    multi.start()   
############Création du menu###############
menuFrame = Frame(root) #On crée une frame contenant les éléments du menu
bouton1 = Button(menuFrame, text = "Jouer contre l'IA", command = startSolo) #Création du bouton permettant de lancer le mode Joueur contre IA.
bouton2 = Button(menuFrame, text = "Jouer contre un autre joueur", command = startMulti) #Création du bouton permettant de lancer le mode Joueur contre Joueur.
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