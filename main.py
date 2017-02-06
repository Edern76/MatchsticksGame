#taking the last one = loss
from Crypto.Random.random import randint

def easy_AI():
    number = randint(1, 3)
    substraction = matchsticks_number - number
    if substraction < 0:
        number = matchsticks_number
    print('AI took ' + str(number) + ' matchstick(s)')
    matchsticks_number -= number
    print('matchsticks left: ' + str(matchsticks_number))

def smart_AI():
    global matchsticks_number
    chosen = False
    while not chosen:
        if matchsticks_number == 12 or matchsticks_number == 8:
            print('took 3 matchsticks')
            matchsticks_number -= 3
            chosen = True
        elif matchsticks_number == 11 or matchsticks_number == 7 or matchsticks_number == 3:
            print('took 2 matchsticks')
            matchsticks_number -= 2
            chosen = True
        elif matchsticks_number == 10 or matchsticks_number == 6 or matchsticks_number == 2:
            print('took 1 matchstick')
            matchsticks_number -= 1
            chosen = True
        else:
            number = randint(1, 3)
            substraction = matchsticks_number - number
            if substraction < 0:
                number = matchsticks_number
            print('AI took ' + str(number) + ' matchstick(s)')
            matchsticks_number -= number
            chosen = True
    print('matchsticks left: ' + str(matchsticks_number))

def player_turn():
    global matchsticks_number
    chosen = False
    correct_options = [1, 2, 3]
    while not chosen:
        choice = int(input('how many ? '))
        if not choice in correct_options:
            print('please choose a correct option')
        else:
            print('Player took ' + str(choice) + ' matchstick(s)')
            matchsticks_number -= choice
            chosen = True
            print('matchsticks left: ' + str(matchsticks_number))

def main():
    global matchsticks_number
    matchsticks_number = int(input('how many matchsticks overall ? '))
    while True:
        player_turn()
        if matchsticks_number <= 0:
            print('finished: Player lost')
            break
        smart_AI()
        if matchsticks_number <= 0:
            print('finished: AI lost')
            break

main()
