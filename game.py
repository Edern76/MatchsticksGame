
from random import randint

matches_num = 21

def AI():
    global matches_num
    end = False
    n = 0
    while not end:
        if matches_num == 4*n:
            matches_num -= 3
            print('AI took 3 matches')
            end = True
        elif matches_num == 4*n + 3:
            matches_num -= 2
            print('AI took 2 matches')
            end = True
        elif matches_num == 4*n + 2:
            matches_num -= 1
            print('AI took 1 match')
            end = True
        n += 1
        if  not end and 4*n > matches_num:
            num = randint(1, 3)
            if matches_num - num < 0:
                num = matches_num
            matches_num -= num
            print('AI took ' + str(num) + ' match(es)')
            end = True
    print('matches left: ' + str(matches_num))

def player():
    global matches_num
    while True:
        num = int(input('how many? '))
        if matches_num - num < 0 or num not in [1, 2, 3]:
            print('please choose a correct option')
        else:
            matches_num -= num
            print('Player took ' + str(num) + ' match(es)')
            break
    print('matches left: ' + str(matches_num))

def main(mode = 3):
    global matches_num
    while not mode in [0, 1]:
        mode = int(input('Against player (1) or computer (0) '))
    matches_num = 21 #int(input('how many matches? '))
    print('Starting matches number: ' + str(matches_num))
    if not mode:
        while True:
            player()
            if matches_num == 0:
                print('player loses')
                break
            AI()
            if matches_num == 0:
                print('AI loses')
                break
    else:
        while True:
            print('player1 turn')
            player()
            if matches_num == 0:
                print('player 1 loses')
                break
            print('player2 turn')
            player()
            if matches_num == 0:
                print('player 2 loses')
                break

if __name__ == "__main__":
    main()
