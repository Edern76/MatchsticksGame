#!/usr/bin/env python3
# -*- coding: utf8 -*-

import threading, time, os
from random import randint
from tkinter import *
from utils import curDir, assetsDir, imageDir

matches_num = 21
playing = False
chosen = 0
lock = threading.RLock()
args = sys.argv
#P1matches = 0
#P2matches = 0
"""
class Controller:
    def __init__(self):
        self.playing = False
        self.chosen = None
"""        

def chooseNumber(number):
        global playing, chosen
        with lock:
            chosen = number
            playing = False
        
        print('Chosen')

# controller = Controller()

class GUI(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.textField = None
        self.chosen = None
        self.playing = False
        self.P1Name = "Loading..."
        self.P2Name = "Loading..."
        self.P1Avatar = "loading_avatar_big.png"
        self.P2Avatar = "loading_avatar_big.png"
        #self.P1Text = "Allumettes : " + str(P1matches)
        #self.P2Text = "Allumettes : " + str(P2matches)
        self.matchesImages = []
        self._stop = threading.Event()
        
    def stop(self):
        self._stop.set()
    
    def stopped(self):
        return self._stop.isSet()
    
    def exit(self):
        self.stop()
        while not self.stopped():
            continue
        os._exit(1)

    def run(self):
##############Creation de la fenêtre principale##############       
        self.base = Tk()
        self.base.geometry('1280x720+0+0')
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
        matchX = 15 #Abscisse sur le canvas de la première allumette
        matchY = 135 #Ordonée sur le canvas des allumettes
        matchFile = PhotoImage(file = os.path.join(imageDir, 'match_smaller.png')) #Récupération de l'image correspondant à une allumette
        for loop in range(21):
            allumette = self.imageCanvas.create_image(matchX, matchY, anchor = NW, image = matchFile) #Placement de l'image sur le canvas
            self.matchesImages.append(allumette) #Ajout de l'image à la liste des allumettes (pour pouvoir ensuite influer sur les images en dehors de la classe GUI)
            matchX += 30 #Incrémentation de l'abscisse de la prochaine allumette de 30 pixels (= on place la prochaine allumette 30 pixels sur la droite de l'allumette précédente)
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
        
        args = sys.argv #Récupération des arguments passés au module par l'intermédiaire du shell

##############Création des contrôles du joueur 2##############
        if int(args[1]) == 1: #Si on a choisi le mode 2 joueurs, on crée les contrôles du joueur 2. La procédure est alors la même que pour les contrôles du joueur 1 mais dans une frame différente.
            self.P2buttonFrame = Frame(self.subFrame1)
            self.P2button1 = Button(self.P2buttonFrame, text = "1", width = 5, command = lambda : chooseNumber(1))
            self.P2button2 = Button(self.P2buttonFrame, text = "2", width = 5, command = lambda : chooseNumber(2))
            self.P2button3 = Button(self.P2buttonFrame, text = "3", width = 5, command = lambda : chooseNumber(3))
            self.P2matchButtons = [self.P2button1, self.P2button2, self.P2button3]
            for loop in self.P2matchButtons:
                loop.pack(side = LEFT, padx = 10)
                loop.config(state = DISABLED)
            self.P2buttonFrame.pack(side = BOTTOM, padx = 20, pady = 30)
            print("Player 2 config complete") #Ligne utilisée uniquement pour le débugage, afin de signifier que la création des contrôles s'est correctement executée
        
        else: #Sinon, on ne crée pas les contrôles
            self.P2buttonFrame = None
            self.P2button1 = None
            self.P2button2 = None
            self.P2button3 = None
            self.P2matchButtons = None
            print("Current mode : " + str(args[1])) #Ligne utilisée uniquement pour le débugage
#############################################################


        self.subWindow.add(self.subFrame1)
        self.subWindow.add(self.subFrame2)
        self.subWindow.add(self.subFrame3)
        self.subWindow.pack()
                
        self.rWindow = PanedWindow(self.frame3, orient = VERTICAL)
        self.rWindow.pack(side = TOP, expand = Y, fill = BOTH) # On fait en sorte que la PanedWindow remplisse l'intégralité du volet de droite
        self.rFrame1 = Frame(self.rWindow, width = 340, height = 150) #Création des volets
        self.rFrame2 = Frame(self.rWindow, width = 340, height = 500) #Création des volets
        self.rFrame3 = Frame(self.rWindow, width = 340, height = 110) #Création des volets
        
        self.P2Canvas= Canvas(self.rFrame1, width = 80, height = 80, relief = GROOVE)
        self.P2File = PhotoImage(file = os.path.join(imageDir, self.P2Avatar))
        self.P2Image = self.P2Canvas.create_image(0, 0, anchor = NW, image = self.P2File)
        self.P2Label = Label(self.rFrame1, text = self.P2Name, relief = RIDGE, justify = CENTER, fg = 'gray', bg = 'white')
        #self.P2MLabel = Label(self.rFrame1, text = self.P2Text, relief = RIDGE, justify = CENTER, bg = 'white')
        self.P2Canvas.grid(row = 0, column = 1, rowspan = 5, columnspan = 2)
        self.P2Label.grid(row = 2, column = 4, columnspan = 3)
        #self.P2MLabel.grid(row = 4, column = 4, columnspan = 3)
        
        self.P1Canvas= Canvas(self.rFrame3, width = 80, height = 80, relief = GROOVE)
        self.P1File = PhotoImage(file = os.path.join(imageDir, self.P1Avatar))
        self.P1Image = self.P1Canvas.create_image(0, 0, anchor = NW, image = self.P1File)
        self.P1Label = Label(self.rFrame3, text = self.P1Name, relief = RIDGE, justify = CENTER, fg = 'gray', bg = 'white')
        self.P1Canvas.grid(row = 0, column = 1, rowspan = 5, columnspan = 2)
        self.P1Label.grid(row = 2, column = 4, columnspan = 3)
        
        self.rWindow.add(self.rFrame1)
        self.rWindow.add(self.rFrame2)
        self.rWindow.add(self.rFrame3)
        self.rWindow.pack()
        
        
        self.base.protocol("WM_DELETE_WINDOW", self.exit)
        self.base.mainloop()

        raise SystemExit
gui = GUI()

def writeToField(message):
    convMessage = message + '\n'
    gui.textField.config(state = NORMAL)
    gui.textField.insert('end', convMessage)
    gui.textField.config(state = DISABLED)

class ImageMover(threading.Thread):
    def __init__(self, image, dx, dy, repet = 1, sleepTime = 0, deleteWhenDone = True):
        threading.Thread.__init__(self)
        self.image = image
        self.dx = dx
        self.dy = dy
        self.repet = repet
        self.sleepTime = sleepTime
        self.deleteWhenDone = deleteWhenDone
        
        
    def run(self):
        for w in range(self.repet):
            gui.imageCanvas.move(self.image, self.dx, self.dy)
            time.sleep(self.sleepTime)
        if self.deleteWhenDone:
            gui.imageCanvas.delete(self.image)

class GameHandler:
    def __init__(self, starting_num = 21, starting_player = 'Player 1'): 
        self.current_matches = starting_num
        self.current_player = starting_player
        self.AI = None
        self.curPlayName = gui.P1Name
        
    def takeMatches(self, number, playerNum = 1):
        try:
            if number not in range (1,4) or self.current_matches < number:
                raise ValueError("Attempting to take an invalid number of matches ({})".format(number))
            else:
                self.current_matches -= number
                writeToField(self.curPlayName + ' took '+ str(number) + " matches.")
                matchesToMove = []
                moveThreads = []
                for loop in range(number):
                    matchesToMove.append(gui.matchesImages[-1])
                    #gui.imageCanvas.move(gui.matchesImages[-1], 0, 1)
                    #gui.imageCanvas.delete(gui.matchesImages[-1])
                    del gui.matchesImages[-1]
                for i in matchesToMove:
                    if playerNum == int(1):
                        mover = ImageMover(i, dx = 0, dy = 1, repet = 50, sleepTime = 0.005)
                    else:
                        print('PlayNum = ' + str(playerNum))
                        mover = ImageMover(i, dx = 0, dy = -1, repet = 50, sleepTime = 0.005)
                    moveThreads.append(mover)
                for j in moveThreads:
                    j.start()
                for k in moveThreads:
                    k.join()
                return 'done'
        except ValueError:
            return 'fail'
        
    def checkWin(self):
        if self.current_matches <= 0:
            if self.current_player in ('Player 2', 'AI'):
                self.curPlayName = gui.P2Name
                gui.P1Label.config(fg = "gray")
            else:
                self.curPlayName = gui.P1Name
                gui.P2Label.config(fg = "gray")
            writeToField(self.curPlayName + " wins !")
            return 'win'
        else:
            return 'continue'
    
    def player(self, playNum = 1, turnNum = 1):
        def inputNumber():
            global playing, chosen
            valid = False
            while not valid:
                controller = gui
                if playNum == 1:
                    if self.current_matches >= 1:
                        gui.button1.config(state = NORMAL)
                    if self.current_matches >= 2:
                        gui.button2.config(state = NORMAL)
                    if self.current_matches >= 3:
                        gui.button3.config(state = NORMAL)
                    buttonList = gui.matchButtons
                    curFrame = gui.buttonFrame
                else:
                    if self.current_matches >= 1:
                        gui.P2button1.config(state = NORMAL)
                    if self.current_matches >= 2:
                        gui.P2button2.config(state = NORMAL)
                    if self.current_matches >= 3:
                        gui.P2button3.config(state = NORMAL)
                        
                    buttonList = gui.P2matchButtons
                    curFrame = gui.P2buttonFrame
                '''
                if args[1] == 1 and turnNum > 1:
                    for r in buttonList:
                        r.pack()
                '''
                #controller.playing = True
                playing = True
                while True:
                    with lock:
                        mustContinue = playing and (chosen == 0)  #(not controller.playing) or
                        if mustContinue:
                            #print('wtf')
                            continue
                        else:
                            #print(controller.playing)
                            print(playing)
                            print(mustContinue)
                            print(chosen)
                            break
                print('Loop ended')
                for i in buttonList:
                    i.config(state = DISABLED)
                    '''
                    if args[1] == int(1):
                        i.pack_remove()
                    '''
                chosenNum = int(chosen)
                print(chosen)
                print(chosenNum)
                if chosenNum != 0:
                    valid = True
                    break
            chosen = 0    
            return chosenNum
        
        status = 'fail'
        while status != 'done':
            num = inputNumber()
            status = self.takeMatches(num, playerNum = playNum)
            
    
    class AIComponent:
        def __init__(self, owner):
            self.n = 0
            self.owner = owner
            
        def takeTurn(self):
            self.n = 0
            n = self.n
            mainClass = self.owner
            matches_num = mainClass.current_matches
            removeMatch = mainClass.takeMatches
            end = False
            while not end:
                if matches_num == 4*n:
                    removeMatch(3, playerNum = 2)
                    #writeToField('AI took 3 matches')
                    end = True
                elif matches_num == 4*n + 3:
                    removeMatch(2, playerNum = 2)
                    #writeToField('AI took 2 matches')
                    end = True
                elif matches_num == 4*n + 2:
                    removeMatch(1, playerNum = 2)
                    #writeToField('AI took 1 match')
                    end = True
                n += 1
                if not end and 4*n > matches_num:
                    num = randint(1, 3)
                    if matches_num - num < 0:
                        num = matches_num
                    removeMatch(num, playerNum = 2)    
                    end = True
                    #writeToField('AI took ' + str(num) + ' match(es)')
                
    
    def play(self, mode):
        if not mode in (0,1):
            raise ValueError("Mode number must be either 0 or 1")
        if not mode:
            self.AI = self.AIComponent(self)
            AI = self.AI.takeTurn
        player = self.player
        turnNum = 0
        while not self.checkWin() == 'win':
            if self.current_player in ('Player 2', 'AI'):
                writeToField(gui.P2Name + "'s turn.")
                self.curPlayName = gui.P2Name
            else:
                writeToField(gui.P1Name +"'s turn.")
                self.curPlayName = gui.P1Name
            #writeToField('Current matches : ' + str(self.current_matches))
            if not mode:
                if self.current_player == 'Player 1':
                    player(turnNum = turnNum)
                    self.current_player = 'AI'
                else:
                    AI()
                    self.current_player = 'Player 1'
            else:
                if self.current_player == "Player 1":
                    player(turnNum = turnNum)
                    self.current_player = 'Player 2'
                else:
                    player(2, turnNum = turnNum)
                    self.current_player = 'Player 1'
            turnNum += 1



def main(mode = 3):
    game = GameHandler()
    gui.start()
    time.sleep(3)
    global matches_num
    matches_num = game.current_matches
    if not mode in [0, 1]:
        while not mode in [0, 1]:
            print(mode)
            mode = int(input('Against player (1) or computer (0) '))
    matches_num = game.current_matches #int(input('how many matches? '))
    print('Starting matches number: ' + str(matches_num))
    print(mode)
    if mode == 0:
        gui.P2Name = "R0B0T0"
        gui.P2Avatar = "AI_avatar_big.png"
        gui.P1Name = str(args[2])
    else:
        gui.P2Name = str(args[3])
        gui.P2Avatar = "P2_avatar.png"
        gui.P1Name = str(args[2])
    gui.P1Avatar = "P1_avatar.png"
    gui.P2Label.config(text = gui.P2Name, fg = "red")
    gui.P1Label.config(text = gui.P1Name, fg = "blue")
    gui.P1File.configure(file = os.path.join(imageDir, gui.P1Avatar))
    gui.P2File.configure(file = os.path.join(imageDir, gui.P2Avatar))
    game.play(mode)

if __name__ == "__main__":
    main(int(args[1]))
