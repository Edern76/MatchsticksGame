import os, sys
from random import randint


matches_num = 21
 
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
                print(self.current_player.capitalize(), 'took', str(number), "matches.")
                return 'done'
        except ValueError:
            return 'fail'
        
    def checkWin(self):
        if self.current_matches <= 0:
            print(self.current_player, "wins !")
            return 'win'
        else:
            return 'continue'
    
    def player(self):
        def inputNumber():
            num = int(input('How many ?'))
            return num
        
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
                #print('AI took 3 matches')
            elif matches_num == 4*n + 3:
                removeMatch(2)
                #print('AI took 2 matches')
            elif matches_num == 4*n + 2:
                removeMatch(1)
                #print('AI took 1 match')
            else:
                num = randint(1, 3)
                if matches_num - num < 0:
                    num = matches_num
                removeMatch(num)    
                #print('AI took ' + str(num) + ' match(es)')
            n += 1
    
    def play(self, mode):
        if not mode in (0,1):
            raise ValueError("Mode number must be either 0 or 1")
        if not mode:
            self.AI = self.AIComponent(self)
        player = self.player
        AI = self.AI.takeTurn
        while not self.checkWin() == 'win':
            print(self.current_player + "'s turn.")
            print('Current matches :', self.current_matches)
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
