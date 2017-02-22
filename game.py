import threading, time, os
from random import randint
from tkinter import *
from utils import curDir, assetsDir, imageDir

matches_num = 21
playing = False
chosen = 0
lock = threading.RLock()
args = sys.argv
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
    
def choose1():
    chooseNumber(1)

def choose2():
    chooseNumber(2)
    
def choose3():
    chooseNumber(3)


# controller = Controller()

class GUI(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.textField = None
        self.chosen = None
        self.playing = False
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
        global controller
        self.base = Tk()
        self.base.geometry('1280x720+0+0')
        self.window = PanedWindow(self.base, orient = HORIZONTAL)
        self.window.pack(side = TOP, expand = Y, fill = BOTH)
        self.frame1 = Frame(self.window, width = 300, height = 720)
        self.frame2 = Frame(self.window, width = 640, height = 720)
        self.frame3 = Frame(self.window, width = 340, height = 720)
        self.frame1.grid_propagate(False)
        self.frame1.pack_propagate(False)
        self.textField = Text(self.frame1)
        self.textField.pack(expand = Y, fill = BOTH)
        self.textField.config(state = DISABLED)
        
        self.window.add(self.frame1)
        self.window.add(self.frame2)
        
        self.subWindow = PanedWindow(self.frame2, orient = VERTICAL)
        self.subWindow.pack(side = TOP, expand = Y, fill = BOTH)
        self.subFrame1 = Frame(self.subWindow, width = 640, height = 150)
        self.subFrame2 = Frame(self.subWindow, width = 640, height = 400)
        self.subFrame3 = Frame(self.subWindow, width = 640, height = 210)
        
        self.photo = PhotoImage(file = os.path.join(imageDir, 'playfield.png'))
        self.imageCanvas = Canvas(self.subFrame2, width = 640, height = 400)
        self.imageCanvas.create_image(0, 0, anchor = NW, image = self.photo)
        matchX = 15
        matchY = 135
        matchFile = PhotoImage(file = os.path.join(imageDir, 'match_smaller.png'))
        for loop in range(21):
            allumette = self.imageCanvas.create_image(matchX, matchY, anchor = NW, image = matchFile)
            self.matchesImages.append(allumette)
            matchX += 30
        self.imageCanvas.place(width = 640, height = 400)
        
        self.buttonFrame = Frame(self.subFrame3)
        self.button1 = Button(self.buttonFrame, text = "1", width = 5, command = lambda : chooseNumber(1))
        self.button2 = Button(self.buttonFrame, text = "2", width = 5, command = lambda : chooseNumber(2))
        self.button3 = Button(self.buttonFrame, text = "3", width = 5, command = lambda : chooseNumber(3))
        self.matchButtons = [self.button1, self.button2, self.button3]
        for loop in self.matchButtons:
            loop.pack(side = LEFT, padx = 10)
            loop.config(state = DISABLED)
        self.buttonFrame.pack(side = TOP, padx = 20, pady = 70)
        
        args = sys.argv
        
        if int(args[1]) == 1:
            self.P2buttonFrame = Frame(self.subFrame1)
            self.P2button1 = Button(self.P2buttonFrame, text = "1", width = 5, command = lambda : chooseNumber(1))
            self.P2button2 = Button(self.P2buttonFrame, text = "2", width = 5, command = lambda : chooseNumber(2))
            self.P2button3 = Button(self.P2buttonFrame, text = "3", width = 5, command = lambda : chooseNumber(3))
            self.P2matchButtons = [self.P2button1, self.P2button2, self.P2button3]
            for loop in self.P2matchButtons:
                loop.pack(side = LEFT, padx = 10)
                loop.config(state = DISABLED)
            self.P2buttonFrame.pack(side = BOTTOM, padx = 20, pady = 30)
            print("Player 2 config complete")
        
        else:
            self.P2buttonFrame = None
            self.P2button1 = None
            self.P2button2 = None
            self.P2button3 = None
            self.P2matchButtons = None
            print("Current mode : " + str(args[1]))
        
        self.subWindow.add(self.subFrame1)
        self.subWindow.add(self.subFrame2)
        self.subWindow.add(self.subFrame3)
        self.subWindow.pack()
                
        self.window.add(self.frame3)
        self.window.pack()
        
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
        
    def takeMatches(self, number, playerNum = 1):
        try:
            if number not in range (1,4) or self.current_matches < number:
                raise ValueError("Attempting to take an invalid number of matches ({})".format(number))
            else:
                self.current_matches -= number
                writeToField(self.current_player.capitalize() + ' took '+ str(number) + " matches.")
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
            writeToField(self.current_player + " wins !")
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
                        gui.button1.config(state = NORMAL, command = choose1)
                    if self.current_matches >= 2:
                        gui.button2.config(state = NORMAL)
                    if self.current_matches >= 3:
                        gui.button3.config(state = NORMAL)
                    buttonList = gui.matchButtons
                    curFrame = gui.buttonFrame
                else:
                    if self.current_matches >= 1:
                        gui.P2button1.config(state = NORMAL, command = choose1)
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
            writeToField(self.current_player + "'s turn.")
            writeToField('Current matches : ' + str(self.current_matches))
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
    game.play(mode)

if __name__ == "__main__":
    main(int(args[1]))
