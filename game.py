import threading, time, os
from random import randint
from tkinter import *
from utils import curDir, assetsDir, imageDir

matches_num = 21
playing = False
chosen = 0
lock = threading.RLock()
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
        self.imageCanvas.place(width = 640, height = 400)
        
        self.buttonFrame = Frame(self.subFrame3)
        self.button1 = Button(self.buttonFrame, text = "1", width = 5, command = lambda : chooseNumder(1))
        self.button2 = Button(self.buttonFrame, text = "2", width = 5, command = lambda : chooseNumber(2))
        self.button3 = Button(self.buttonFrame, text = "3", width = 5, command = lambda : chooseNumber(3))
        self.matchButtons = [self.button1, self.button2, self.button3]
        for loop in self.matchButtons:
            loop.pack(side = LEFT, padx = 10)
            loop.config(state = DISABLED)
        self.buttonFrame.pack(side = TOP, padx = 20, pady = 70)    
        
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

class GameHandler:
    def __init__(self, starting_num = 21, starting_player = 'Player 1'): 
        self.current_matches = starting_num
        self.current_player = starting_player
        self.AI = None
        
    def takeMatches(self, number):
        try:
            if number not in range (1,4) or self.current_matches < number:
                raise ValueError("Attempting to take an invalid number of matches ({})".format(number))
            else:
                self.current_matches -= number
                writeToField(self.current_player.capitalize() + ' took '+ str(number) + " matches.")
                return 'done'
        except ValueError:
            return 'fail'
        
    def checkWin(self):
        if self.current_matches <= 0:
            writeToField(self.current_player + " wins !")
            return 'win'
        else:
            return 'continue'
    
    def player(self):
        def inputNumber():
            global playing, chosen
            valid = False
            while not valid:
                controller = gui
                if self.current_matches >= 1:
                    gui.button1.config(state = NORMAL, command = choose1)
                if self.current_matches >= 2:
                    gui.button2.config(state = NORMAL)
                if self.current_matches >= 3:
                    gui.button3.config(state = NORMAL)
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
                for i in gui.matchButtons:
                    i.config(state = DISABLED)
                
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
            status = self.takeMatches(num)
            
    
    class AIComponent:
        def __init__(self, owner):
            self.n = 0
            self.owner = owner
            
        def takeTurn(self):
            n = self.n
            mainClass = self.owner
            matches_num = mainClass.current_matches
            removeMatch = mainClass.takeMatches
            if matches_num == 4*n:
                removeMatch(3)
                #writeToField('AI took 3 matches')
            elif matches_num == 4*n + 3:
                removeMatch(2)
                #writeToField('AI took 2 matches')
            elif matches_num == 4*n + 2:
                removeMatch(1)
                #writeToField('AI took 1 match')
            else:
                num = randint(1, 3)
                if matches_num - num < 0:
                    num = matches_num
                removeMatch(num)    
                #writeToField('AI took ' + str(num) + ' match(es)')
            n += 1
    
    def play(self, mode):
        if not mode in (0,1):
            raise ValueError("Mode number must be either 0 or 1")
        if not mode:
            self.AI = self.AIComponent(self)
        player = self.player
        AI = self.AI.takeTurn
        while not self.checkWin() == 'win':
            writeToField(self.current_player + "'s turn.")
            writeToField('Current matches : ' + str(self.current_matches))
            if not mode:
                if self.current_player == 'Player 1':
                    player()
                    self.current_player = 'AI'
                else:
                    AI()
                    self.current_player = 'Player 1'
            else:
                if self.current_player == "Player 1":
                    player()
                    self.current_player = 'Player 2'
                else:
                    player()
                    self.current_player = 'Player 1'



def main(mode = 3):
    game = GameHandler()
    gui.start()
    time.sleep(2)
    global matches_num
    matches_num = game.current_matches
    if not mode in [0, 1]:
        while not mode in [0, 1]:
            print(mode)
            mode = int(input('Against player (1) or computer (0) '))
    matches_num = game.current_matches #int(input('how many matches? '))
    print('Starting matches number: ' + str(matches_num))
    game.play(mode)

if __name__ == "__main__":
    args = sys.argv
    main(int(args[1]))
