#!/usr/bin/env python3
# -*- coding: utf8 -*-

import threading, time, os
from random import randint
from tkinter import *
from utils import curDir, assetsDir, imageDir

matches_num = 21
playing = False
exitted = False
chosen = 0
lock = threading.RLock()

def chooseNumber(number):
        global playing, chosen
        with lock:
            chosen = number
            playing = False   



class GUI(threading.Thread):
    '''
    Classe permettant de créer l'interface graphique. Elle hérite de la classe Thread, car pour que l'interface s'exécute en même temps que le code relatif au jeu, il faut placer le code relatif à l'interface dans un thread s'exécutant en parallèle et communiquant avec le jeu
    GUI est l'acronyme anglais pour Graphical User Interface, c'est à dire Interface Utilisateur Graphique. Il s'agit de l'élément au travers duquel l'utilisateur va interagir avec le programme
    '''
    def __init__(self, attachTo = None, mode = 0):
        '''
        Méthode appelée lors de la création d'une instance de la classe GUI (on crée une instance en tapant "foo = GUI()", où foo est le nom de l'instance de la classe
        @type attachTo: Toplevel
        @param attachTo: La fenêtre à laquelle l'interface va s'attacher. Si cette variable est None, on crée une fenêtre à la place.
        
        @type mode: int
        @param mode: Le mode de jeu. Si cette variable est égale à 0, l'interface ne créera pas les contrôles du joueur 2 (puisque le mode 0 correspond au mode joueur contre IA)
        '''
        threading.Thread.__init__(self) #Création d'une instance de la classe Thread
        self.textField = None
        self.chosen = None
        self.playing = False
        ##############Valeurs temporaires affichées uniquement durant le chargement##############
        self.P1Name = "Loading..."
        self.P2Name = "Loading..."
        self.P1Avatar = "loading_avatar_big.png"
        self.P2Avatar = "loading_avatar_big.png"
        self.matchText = "NaN"
        ##############################################################################
        self.matchesImages = [] #Liste contenant les images des allumettes, de sorte à ce qu'on puisse les manipuler en dehors de la classe GUI
        self._stop = threading.Event()
        self.mode = mode
        self.attachTo = attachTo
        self.base = self.attachTo
        
    def stop(self):
        global exitted
        self._stop.set()
        exitted = True #On fait en sorte que la variable globale exitted soit égale à True, afin que le code relatif au jeu se quitte lui aussi en même temps que le GUI.
    
    def stopped(self):
        return self._stop.isSet()
    
    def exit(self):
        self.stop() #On envoie une requête d'arrêt au Thread du GUI
        while not self.stopped():
            continue #On attend que le Thread s'arrêté (on ne peut utiliser la méthode join() qu'en dehors du Thread)
        self.attachTo.destroy() #On supprime la fenêtre contenant l'interface
        del self #On supprime l'instance de la classe GUI, afin de ne pas utiliser inutilement de la mémoire

    def run(self):
##############Creation de la fenêtre principale##############
        if self.attachTo is None:
            self.base = Tk() #Si aucune fenêtre principale n'a été crée, on en crée une
            #En soi, cette ligne n'est actuellement jamais utilisée, car si le programme est lancé directement à partir de game.py, il affiche un message d'erreur, car on souhaite que l'utilisateur passe par le menu principal, afin qu'on lui demande son nom et qu'il puisse choisir son mode de jeu.
            #Il s'agit donc d'un artefact de développement (car les versions antérieures étaient lancées en appellant la fonction os.system(), qui simulait une commande shell, il fallait donc que game.py soit exécutable indépendamment. Cela permettait également de tester rapidement le programme sans avoir à repasser par le menu principal à chaque fois.
            #Néanmoins, il est très facile de restaurer cette fonctionnalité, en remplacant le bloc de code contenu sous if __name__ == '__main__' par un appel de la fonction main(), avec les arguments adéquats.
        else:
            self.base = self.attachTo #Sinon, on execute la création de l'interface dans la fenêtre TopLevel spécifiée en argument lors de la création de l'instance de la classe (on ne peut avoir qu'une seule fenêtre Tk() par application)
        screenWidth = self.base.winfo_screenwidth()
        screenHeight = self.base.winfo_screenheight()
        startX = screenWidth // 2 - (1280 // 2)
        startY = ((screenHeight // 2) - (720 // 2)) - 40
        self.base.geometry('1280x720+{}+{}'.format(startX, startY))
        self.base.title("Loading...")
#############################################################

##############Division de la fenêtre en trois parties verticales##############
        self.window = PanedWindow(self.base, orient = HORIZONTAL) #Creation d'une 'fenêtre à volets' (ou PanedWindow) verticaux
        self.window.pack(side = TOP, expand = Y, fill = BOTH) #On fait en sorte que la PanedWindow remplisse toute la fenêtre principale
        self.frame1 = Frame(self.window, width = 300, height = 720) #Création des volets
        self.frame2 = Frame(self.window, width = 640, height = 720) #Création des volets
        self.frame3 = Frame(self.window, width = 340, height = 720) #Création des volets
        self.frame1.grid_propagate(False) #On fait en sorte que le premier volet ne change pas de taille
        self.frame1.pack_propagate(False) #Idem que ci-dessus
        self.textField = Text(self.frame1) #Création d'un champ de texte dans le volet 1
        self.textField.pack(expand = Y, fill = BOTH) #On fait en sorte que le champ remplisse l'intégralité du volet 1
        self.textField.config(state = DISABLED) #On désactive le champ de texte de sorte que le texte à l'intérieur soit en lecture seule
        
        self.window.add(self.frame1) #Ajout des volets à la PanedWindow
        self.window.add(self.frame2) #Ajout des volets à la PanedWindow
        self.window.add(self.frame3) #Ajout des volets à la PanedWindow
        self.window.pack() #Placement de la PanedWindow dans la fenêtre principale
###############################################################################        

##############Division du volet central en trois parties horizontales##############        
        self.subWindow = PanedWindow(self.frame2, orient = VERTICAL) #Création d'une nouvelle PanedWindow dans le volet central (notez que l'orientation indiquée est l'inverse du résultat obtenu)
        self.subWindow.pack(side = TOP, expand = Y, fill = BOTH) # On fait en sorte que la PanedWindow remplisse l'intégralité du volet central
        self.subFrame1 = Frame(self.subWindow, width = 640, height = 150) #Création des volets
        self.subFrame2 = Frame(self.subWindow, width = 640, height = 400) #Création des volets
        self.subFrame3 = Frame(self.subWindow, width = 640, height = 210) #Création des volets
###################################################################################

##############Création de l'aire de jeu##############        
        self.photo = PhotoImage(file = os.path.join(imageDir, 'playfield.png')) #Récupération de l'image correspondant à l'aire de jeu
        self.imageCanvas = Canvas(self.subFrame2, width = 640, height = 400) #Création d'un canvas dans le volet horizontal central du volet vertical central
        self.imageCanvas.create_image(0, 0, anchor = NW, image = self.photo) #Placement de l'image dans le canvas
#####################################################

##############Placement des allumettes##############
        self.matchX = 15 #Abscisse sur le canvas de la première allumette
        self.matchY = 135 #Ordonée sur le canvas des allumettes
        self.matchFile = PhotoImage(file = os.path.join(imageDir, 'match_smaller.png')) #Récupération de l'image correspondant à une allumette
        for loop in range(21):
            allumette = self.imageCanvas.create_image(self.matchX, self.matchY, anchor = NW, image = self.matchFile) #Placement de l'image sur le canvas
            self.matchesImages.append(allumette) #Ajout de l'image à la liste des allumettes (pour pouvoir ensuite influer sur les images en dehors de la classe GUI)
            self.matchX += 30 #Incrémentation de l'abscisse de la prochaine allumette de 30 pixels (= on place la prochaine allumette 30 pixels sur la droite de l'allumette précédente)
#####################################################

        self.imageCanvas.place(width = 640, height = 400) #Placement du canvas dans le volet
        
##############Création des contrôles du joueur 1##############
        self.buttonFrame = Frame(self.subFrame3) # Création d'une frame dans le volet inférieur horizontal du volet central vertical (= en dessous de l'aire du jeu, en bas au centre de la fenêtre principale)
        self.button1 = Button(self.buttonFrame, text = "1", width = 5, command = lambda : chooseNumber(1)) #Création des boutons. Normalement, l'attribut command est un nom de fonction SANS parenthèses (si l'on en met, la fonction s'exécute une seule fois à la création du bouton, puis plus du tout même si l'on clique dessus), on ne peut donc normalement pas lui donner d'argument. Pour pallier à cela, on utilise l'instruction lambda avant d'écrire la fonction avec les parenthèses et les arguments, afin qu'elle ne s'exécute pas à la création du bouton mais seulement lorsque l'on clique dessus.
        self.button2 = Button(self.buttonFrame, text = "2", width = 5, command = lambda : chooseNumber(2)) #Création des boutons. Voir ci-dessus pour les explications quant à 'lambda'
        self.button3 = Button(self.buttonFrame, text = "3", width = 5, command = lambda : chooseNumber(3)) #Création des boutons. Idem que ci-dessus
        self.matchButtons = [self.button1, self.button2, self.button3] #Création d'une liste contenant les boutons, afin de pouvoir modifier les trois à la fois à l'aide d'une boucle
        for loop in self.matchButtons:
            loop.pack(side = LEFT, padx = 10) #Placement des boutons
            loop.config(state = DISABLED) #Par défaut, on fait en sorte que les boutons ne soient pas cliquables
        self.buttonFrame.pack(side = TOP, padx = 20, pady = 70) #Placement de la frame contenant les boutons
###############################################################
        

##############Création des contrôles du joueur 2##############
        if self.mode == 1: #Si on a choisi le mode 2 joueurs, on crée les contrôles du joueur 2. La procédure est alors la même que pour les contrôles du joueur 1 mais dans une frame différente.
            self.P2buttonFrame = Frame(self.subFrame1)
            self.P2button1 = Button(self.P2buttonFrame, text = "1", width = 5, command = lambda : chooseNumber(1))
            self.P2button2 = Button(self.P2buttonFrame, text = "2", width = 5, command = lambda : chooseNumber(2))
            self.P2button3 = Button(self.P2buttonFrame, text = "3", width = 5, command = lambda : chooseNumber(3))
            self.P2matchButtons = [self.P2button1, self.P2button2, self.P2button3]
            for loop in self.P2matchButtons:
                loop.pack(side = LEFT, padx = 10)
                loop.config(state = DISABLED)
            self.P2buttonFrame.pack(side = BOTTOM, padx = 20, pady = 30)
        
        else: #Sinon, on ne crée pas les contrôles
            self.P2buttonFrame = None
            self.P2button1 = None
            self.P2button2 = None
            self.P2button3 = None
            self.P2matchButtons = None
#############################################################

##############Ajout des volets horizontaux au volet central##############
        self.subWindow.add(self.subFrame1)
        self.subWindow.add(self.subFrame2)
        self.subWindow.add(self.subFrame3)
        self.subWindow.pack()
#########################################################################

##############Division du volet de droite en volets verticaux##############                
        self.rWindow = PanedWindow(self.frame3, orient = VERTICAL)
        self.rWindow.pack(side = TOP, expand = Y, fill = BOTH) # On fait en sorte que la PanedWindow remplisse l'intégralité du volet de droite
        self.rFrame1 = Frame(self.rWindow, width = 340, height = 150) #Création des volets
        self.rFrame2 = Frame(self.rWindow, width = 340, height = 500) #Création des volets
        self.rFrame2.pack_propagate(0) #On fait en sorte que le volet 2 ne rétrécisse pas pour s'adapter à la taille des éléments qu'il contient
        self.rFrame3 = Frame(self.rWindow, width = 340, height = 110) #Création des volets
###########################################################################

##############Placement des noms et avatars des joueurs##############        
        self.P2Canvas= Canvas(self.rFrame1, width = 80, height = 80, relief = GROOVE)
        self.P2File = PhotoImage(file = os.path.join(imageDir, self.P2Avatar))
        self.P2Image = self.P2Canvas.create_image(0, 0, anchor = NW, image = self.P2File)
        self.P2Label = Label(self.rFrame1, text = self.P2Name, relief = RIDGE, justify = CENTER, fg = 'gray', bg = 'white')
        self.P2Canvas.grid(row = 0, column = 1, rowspan = 5, columnspan = 2)
        self.P2Label.grid(row = 2, column = 4, columnspan = 3, pady = 0, ipady = 0)
        
        self.P1Canvas= Canvas(self.rFrame3, width = 80, height = 80, relief = GROOVE)
        self.P1File = PhotoImage(file = os.path.join(imageDir, self.P1Avatar))
        self.P1Image = self.P1Canvas.create_image(0, 0, anchor = NW, image = self.P1File)
        self.P1Label = Label(self.rFrame3, text = self.P1Name, relief = RIDGE, justify = CENTER, fg = 'gray', bg = 'white')
        self.P1Canvas.grid(row = 0, column = 1, rowspan = 5, columnspan = 2)
        self.P1Label.grid(row = 2, column = 4, columnspan = 3)
######################################################################

##############Remplissage du volet central du volet de droite##############
        self.matchLabel = Label(self.rFrame2, text = 'Allumettes : ' + str(self.matchText), bg = "white", relief = RIDGE) #Texte affichant combien d'allumettes il reste
        self.matchLabel.place(anchor = CENTER, relx = 0.50, rely = 0.47)
        self.quitButton = Button(self.rFrame2, text = 'Quitter', command = self.exit) #Bouton permettant de quitter le programme. A surtout une valeur décorative, puisque cliquer sur la croix rouge a exactement le même effet (voir ci-dessous)
        self.quitButton.place(anchor = CENTER, relx = 0.50, rely = 0.53)
###########################################################################

##############Ajout des volets au volet de droite##############
        self.rWindow.add(self.rFrame1)
        self.rWindow.add(self.rFrame2)
        self.rWindow.add(self.rFrame3)
        self.rWindow.pack()
###############################################################
        
        self.base.protocol("WM_DELETE_WINDOW", self.exit) #On remplace la commande exécutée lorsque l'on clique sur la croix par notre propre commande d'arrêt, afin d'éviter que les Threads ne poursuivent leur exécution en arrière plan après la fermeture de la fenêtre
        if self.attachTo is None:
            self.base.mainloop() #Si on a du créer une fenêtre Tk(), alors on appelle sa méthode mainloop().
            

gui = GUI() #On crée une instance de la classe GUI. Elle ne reçoit aucun argument, et ne sert à rien (car on la recrée plus tard), sauf à faire en sorte que Python ne renvoie pas d'erreur en lisant les fonctions ci-dessous (qui font référence à l'instance gui de la classe GUI)

def writeToField(message):
    '''
    Permet d'écrire un message dans la zone de texte à gauche de l'interface
    '''
    convMessage = message + '\n' #On ajoute la commande de saut de ligne à la fin du message
    gui.textField.config(state = NORMAL) #On active la zone de texte afin de pouvoir écrire dedans
    gui.textField.insert('end', convMessage) #On ajoute le message après ceux déjà existants
    gui.textField.config(state = DISABLED) #On désactive la zone de texte afin de la repasser en lecture seule

class ImageMover(threading.Thread):
    '''
    Permet d'animer le déplacement d'une image. Ce déplacement est réalisé dans un Thread, afin de pouvoir déplacer plusieurs images simultanément
    '''
    def __init__(self, image, dx, dy, repet = 1, sleepTime = 0, deleteWhenDone = True):
        '''
        @type dx: int
        @param dx: Valeur du déplacement en abscisse à chaque étape de l'animation
        
        @type dy : int
        @param dy : Valeur du déplacement en ordonnée à chaque étape de l'animation
        
        @type repet : int
        @param repet : Nombre d'étapes de l'animation
        
        @type sleepTime: float
        @param sleepTime : Temps en secondes entre chaque étape. Si ce temps est égal à 0, l'animation est quasi instantanée, et donc quasi invisible
        
        @type deleteWhenDone : bool
        @param deleteWhenDone : Si cette variable est égale à True, on efface l'image à la fin de l'animation. Sinon, on ne l'efface pas
        '''
        threading.Thread.__init__(self)
        self.image = image
        self.dx = dx
        self.dy = dy
        self.repet = repet
        self.sleepTime = sleepTime
        self.deleteWhenDone = deleteWhenDone
        
        
    def run(self):
        for w in range(self.repet):
            gui.imageCanvas.move(self.image, self.dx, self.dy) #A chaque étape, on déplace l'image selon les coordonnées spécifiées
            time.sleep(self.sleepTime) #Puis on attend le temps indiqué avant de poursuivre l'animation
        if self.deleteWhenDone:
            gui.imageCanvas.delete(self.image) #Si la variable correspondante est égale à True, alors on efface l'image après l'animation.

class GameHandler:
    '''
    Classe contenant les fonctions nécessaires au déroulement du jeu.
    '''
    def __init__(self, starting_num = 21, starting_player = 'Player 1'): 
        self.current_matches = starting_num
        self.current_player = starting_player #L'identifiant du joueur dont c'est le tour. "Player 1" si c'est le joueur 1, "Player 2" ou "AI" si c'est l'IA ou le joueur 2. Notez que cela est différent du nom réel des joueurs
        self.AI = None #Par défaut, on n'a pas d'IA
        self.curPlayName = gui.P1Name #Le nom du joueur duquel c'est le tour
                
    def takeMatches(self, number, playerNum = 1):
        try:
            if number not in range (1,4) or self.current_matches < number:
                raise ValueError("Attempting to take an invalid number of matches ({})".format(number)) #On provoque une erreur si on essaye de prendre un nombre d'allumettes invalide (cela est cependant théoriquement impossible)
            else:
                self.current_matches -= number #On soustrait le nombre d'allumettes prises au nombre d'allumette restantes
                if number > 1:
                    writeToField(self.curPlayName + ' a pris '+ str(number) + " allumettes.") #On écrit dans le champ de texte le nom du joueur ayant pris les allumettes et le nombre d'allumettes qu'il a pris
                else:
                    writeToField(self.curPlayName + ' a pris '+ str(number) + " allumette.")
                matchesToMove = [] #Liste des allumettes dont il faut animer la prise
                moveThreads = [] #Liste des threads chargés de l'animation des allumettes
                for loop in range(number): #On répète le bloc ci-dessous autant de fois que l'on a pris d'allumette
                    matchesToMove.append(gui.matchesImages[-1]) #On ajoute à la liste des allumettes à animer la dernière allumette de la liste des images d'allumettes du GUI
                    del gui.matchesImages[-1] #On retire cette image de la liste, afin de ne pas prendre deux fois la même
                for i in matchesToMove:
                    if playerNum == int(1):
                        mover = ImageMover(i, dx = 0, dy = 1, repet = 50, sleepTime = 0.005) #Si il s'agit du joueur 1 qui a pris les allumettes, on crée un Thread qui va animer les allumettes vers le bas
                    else:
                        mover = ImageMover(i, dx = 0, dy = -1, repet = 50, sleepTime = 0.005) #Sinon, on crée un thread qui va animer les allumettes vers le haut
                    moveThreads.append(mover) #On ajoute le thread crée à la liste des threads chargés de l'animation
                for j in moveThreads:
                    j.start() #On démarre chacun des threads, quasi simultanément. Si la machine sur lequel le programme tourne a des problèmes de performance, les animations ne seront tout de fois pas correctement synchronisées
                for k in moveThreads:
                    k.join() #Une fois que les trois threads ont été lancés, on attend qu'ils se terminent avant de continuer l'exécution du programme
                return 'done'
        except ValueError:
            return 'fail'
        
    def checkWin(self):
        if exitted:
            return #Si on a quitté l'interface, on quitte également cette fonction
        gui.matchText = str(self.current_matches) #On met à jour le texte correspondant au nombre d'allumette
        gui.matchLabel.configure(text = "Allumettes : " + str(gui.matchText)) # On met à jour l'affichage de ce nombre d'allumettes, en lui indiquant d'utiliser la nouvelle valeur de gui.matchText
        if self.current_matches <= 0: #Si il ne reste plus aucune allumette, alors on regarde qui a joué en dernier
            if self.current_player in ('Player 2', 'AI'):
                self.curPlayName = gui.P2Name #On met à jour le nom du joueur en cours
                gui.P1Label.config(fg = "gray") #On grise le nom du perdant
            else:
                self.curPlayName = gui.P1Name #On met à jour le nom du joueur en cours
                gui.P2Label.config(fg = "gray") #On grise le nom du perdant
            writeToField(self.curPlayName + " remporte la partie !") #On affiche le nom du vainqueur
            return 'win' #On retourne 'win', afin d'indiquer qu'il faut arrêter le jeu
        else:
            return 'continue' #On retourne 'continue', pour indiquer qu'il faut continuer le jeu
    
    def player(self, playNum = 1, turnNum = 1):
        '''
        Fonction permettant d'effectuer le tour d'un joueur
        '''
        def inputNumber():
            '''
            Fonction permettant d'attendre que le joueur clique sur un bouton, et de retourner la valeur choisie
            '''
            global playing, chosen
            valid = False
            while not valid:       
                if playNum == 1: #Si le joueur en cours est le joueur 1
                    if self.current_matches >= 1:
                        gui.button1.config(state = NORMAL) #Si il reste plus d'une allumette, on rend le bouton 1 du joueur 1 cliquable
                    if self.current_matches >= 2:
                        gui.button2.config(state = NORMAL) #Si il reste plus de deux allumettes, on rend le bouton 2 du joueur 1 cliquable
                    if self.current_matches >= 3:
                        gui.button3.config(state = NORMAL) #Si il reste plus de trois allumettes, on rend le bouton 3 du joueur 1 cliquable
                    buttonList = gui.matchButtons #La liste des boutons que l'on devra désactiver à la fin du tour est la liste des boutons du joueur 1
                else: #Si le joueur en cours est le joueur 2
                    if self.current_matches >= 1:
                        gui.P2button1.config(state = NORMAL) #Si il reste plus d'une allumette, on rend le bouton 1 du joueur 2 cliquable
                    if self.current_matches >= 2:
                        gui.P2button2.config(state = NORMAL) #Si il reste plus de deux allumettes, on rend le bouton 2 du joueur 2 cliquable
                    if self.current_matches >= 3:
                        gui.P2button3.config(state = NORMAL) #Si il reste plus de deux allumettes, on rend le bouton 3 du joueur 2 cliquable
                        
                    buttonList = gui.P2matchButtons #La liste des boutons que l'on devra désactiver à la fin du tour est la liste des boutons du joueur 2

                playing = True
                
                while True: #Boucle infinie tant que l'on ne rencontre pas return ou break (puisque par 'while True' on sous entend 'while True = True', ce qui est toujours vrai, on aurait aussi pû écrire quelque chose comme 'while 1 + 1 == 2')
                    if exitted:
                        return #Si on a quitté l'interface, on quitte aussi cette fonction
                    with lock: #Cette ligne indique que l'on verrouille les variables auquelles l'on accède dans ce bloc afin qu'un autre thread n'y accède pas en même temps
                        mustContinue = playing and (chosen == 0)  #Si playing est True et que chosen est égal à 0 (= si l'on n'a pas encore choisi de nombre d'allumettes à retirer), mustContinue est True
                        if mustContinue:
                            continue #Si l'on a pas encore fait de choix de nombre d'allumette, on continue la boucle (pendant ce temps, l'exécution du jeu ne se poursuit pas (contrairement à l'interface), ce qui permet d'attendre que l'on clique sur un des trois boutons
                        else:
                            break #Sinon, on sort de la boucle
                if not exitted:
                    for i in buttonList:
                        i.config(state = DISABLED) #On redésactive tous les boutons que l'on a activé précédemment (afin que l'on ne puisse pas les cliquer pendant le tour de l'autre joueur)
                else:
                    return
                chosenNum = int(chosen) #chosenNum prend la valeur de la variable chosen, qui a été modifiée grâce à la fonction chooseNumber() appelée lors du clic sur un bouton. On utilise int() afin de s'assurer que chosenNum soit bien une copie de la valeur de la variable chosen (çad qu'on peut modifier l'une indépendamment de l'autre), et nom un 'raccourci' vers la variable chosen (çad que les modifications de l'une se répercutent sur l'autre)
                if chosenNum != 0:
                    valid = True 
                    break #On quitte la boucle principale
            chosen = 0 #On réinitialise la variable 'chosen'
            return chosenNum #On retourne la valeur de chosenNum, qui correspond à la valeur du bouton que l'on a cliqué
        
        status = 'fail'
        while status != 'done':
            if exitted:
                return #On quitte cette fonction si l'on a quitté l'interface
            else:
                num = inputNumber() #On utilise la fonction inputNumber() (définie quelques lignes plus haut) pour récupérer la valeur du bouton cliqué par le joueur.
                status = self.takeMatches(num, playerNum = playNum) #On retire autant d'allumette que le joueur l'a indiqué
            
    
    class AIComponent:
        def __init__(self, owner):
            self.n = 0
            self.owner = owner #Owner sert à renvoyer à l'instance de la classe gameHandler dont l'instance active de la classe AIComponent dépend
            
        def takeTurn(self):
            self.n = 0
            n = self.n #Raccourci vers la variable self.n, afin d'éviter de devoir retaper self.n à chaque fois
            mainClass = self.owner #Raccourci vers la variable self.owner
            matches_num = mainClass.current_matches #Raccourci vers la variable current_class de l'instance actuellement active de la classe gameHandler
            removeMatch = mainClass.takeMatches #Raccourci vers la méthode takeMatches de l'instance actuellement active de la classe gameHandler
            end = False
            while not end: #Tant que l'on a pas trouvé combien d'allumettes retirer, on continue à chercher, en incrémentant n à chaque fois
                if exitted:
                    return #On quitte cette fonction si l'on a quitté l'interface
                #La stratégie gagnante consiste à - si l'autre joueur commence (comme c'est le cas ici) - toujours laisser à chaque tour (un multiple de 4) + 1 allumettes. L'autre joueur n'a alors strictement aucune chance de gagner, il sera toujours obligé de prendre la dernière allumette
                if matches_num == 4*n: #Si le nombre d'allumettes est égal à un multiple de 4
                    removeMatch(3, playerNum = 2) #On enlève 3 allumettes
                    end = True #On a trouvé combien d'allumettes retirer, on indique donc qu'il faut quitter la boucle
                elif matches_num == 4*n + 3: #Si le nombre d'allumettes est égal à (un multiple de 4) + 3
                    removeMatch(2, playerNum = 2) #On enlève 2 allumettes
                    end = True
                elif matches_num == 4*n + 2: #Si le nombre d'allumettes est égal à (un multiple de 4) + 2
                    removeMatch(1, playerNum = 2) #On retire une allumette
                    end = True
                n += 1 #On incrémente la variable n
                if not end and 4*n > matches_num: #Si l'on a pas trouvé combien d'allumettes retirer et que 4*n est plus élevé que le nombre d'allumettes restantes
                    num = randint(1, 3) #On sélectionne un nombre aléatoire entre 1 et 3
                    if matches_num - num < 0: #Si retirer ce nombre d'allumettes aboutirait à un nombre d'allumettes négatif
                        num = matches_num #On choisit de retirer autant d'allumettes qu'il en reste
                    removeMatch(num, playerNum = 2) #On retire le nombre choisi    
                    end = True

                
    
    def play(self, mode):
        if not mode in (0,1):
            raise ValueError("Mode number must be either 0 or 1")
        gui.base.title("Ryuga no Allumette") #On met à jour le titre de la fenêtre
        if not mode: #Equivalent à if mode == 0
            self.AI = self.AIComponent(self) #On crée une instance de la classe AIComponent, et on l'assinge à la variable AI de l'instance active de la classe gameHandler
            AI = self.AI.takeTurn # On raccourcit la méthode takeTurn de l'instance de la classe AI crée plus tôt en AI
        player = self.player #On raccourcit self.player en player
        turnNum = 0
        while not self.checkWin() == 'win' and not exitted: #Tant que un joueur n'a pas gagné ou que l'on n'a pas quitté l'interface, on exécute le bloc en dessous
            if self.current_player in ('Player 2', 'AI'):
                writeToField("Tour de " + gui.P2Name)
                self.curPlayName = gui.P2Name #On met à jour le nom réel du joueur dont c'est le tour
            else:
                writeToField("Tour de " + gui.P1Name)
                self.curPlayName = gui.P1Name #On met à jour le nom réel du joueur dont c'est le tour
            if not mode: #Si on est en mode joueur contre IA
                if self.current_player == 'Player 1':
                    player(turnNum = turnNum) #On appelle la fonction permettant d'effectuer le tour du joueur 1
                    self.current_player = 'AI' #On indique que c'est le tour de l'IA
                else:
                    AI() #On effectue le tour de l'IA
                    self.current_player = 'Player 1' #On indique que c'est au tour du joueur 1
            else:
                if self.current_player == "Player 1": 
                    player(turnNum = turnNum) #On effectue le tour du joueur 1
                    self.current_player = 'Player 2' #On indique que c'est au tour du joueur 2
                else:
                    player(2, turnNum = turnNum) #On effectue le tour du joueur 2
                    self.current_player = 'Player 1' #On indique que c'est au tour du joueur 1
            turnNum += 1



def main(mode = 3, attachTo = None, name1 = None, name2 = None):
    global gui, exitted
    exitted = False
    game = GameHandler() #On crée une instance de gameHandler nommée game, qui va gérer la logique du jeu
    gui = GUI(attachTo, mode) #On remplace l'instance temporaire de GUI par une autre instance, prenant cette fois en compte les arguments que l'on a passé à la fonction main (la fenêtre à laquelle s'attacher si il y en a une et le mode de jeu)
    gui.start() #On démarre le thread de l'interface
    time.sleep(4) #On attend quatre secondes avant de poursuivre l'exécution. En effet, si le programme se poursuit alors que l'interface n'a pas fini de charger, cela va provoquer énormément d'erreurs
    global matches_num
    matches_num = game.current_matches #On fait en sorte que la variable globale matches_num soit un raccourci vers la variable current_matches de game
    if mode == 0: #Si on est en mode joueur contre IA
        gui.P2Name = "R0B0T0" #Le nom du "Joueur" 2 devient "R0B0T0" (au lieu de "Loading..."), qui est le nom de notre IA
        gui.P2Avatar = "AI_avatar_big.png" #L'avatar du "Joueur" 2 devient l'avatar de l'IA
    else: #Si l'on est en mode joueur contre joueur
        gui.P2Name = str(name2) #Le nom du joueur 2 devient le nom que l'on a spécifié préalablement
        gui.P2Avatar = "P2_avatar.png" #On assigne au joueur 2 son avatar
        
    gui.P1Name = str(name1) #Le nom du joueur 1 devient le nom que l'on a spécifié préalablement
    gui.P1Avatar = "P1_avatar.png" #On assigne au joueur 1 son avatar
    gui.P2Label.config(text = gui.P2Name, fg = "red") #On indique à l'interface de charger la nouvelle valeur du nom du "joueur" 2 (qu'il soit humain ou IA, la distinction s'effectue plus haut) et de l'afficher en rouge dans le label correspondant
    gui.P1Label.config(text = gui.P1Name, fg = "blue") #On indique à l'interface de charger la nouvelle valeur du nom du joueur 1 et de l'afficher en bleu dans le label correspondant.
    #NB : Les méthodes config et configure ont exactement le même fonctionnement
    gui.P1File.configure(file = os.path.join(imageDir, gui.P1Avatar)) #On indique à l'interface de charger le nouvel avatar du joueur 1
    gui.P2File.configure(file = os.path.join(imageDir, gui.P2Avatar)) #On indique à l'interface de charger le nouvel avatar du "joueur" 2
    game.play(mode) #Enfin, on démarre le jeu

if __name__ == "__main__": #Si l'on exécute directement game.py
    from tkinter.messagebox import *
    showerror('Erreur', 'Veuillez lancer main.pyw pour démarrer le programme') #On affiche un message d'erreur.
