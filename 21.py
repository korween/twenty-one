#!/usr/bin/env python2

from random import random
from time import sleep
import sys, tty, termios

class clr:
    gr = '\033[96m'
    b = '\033[94m'
    g = '\033[92m'
    y = '\033[93m'
    r = '\033[91m'
    e = '\033[0m'

def cprint(string, c=str()):
    clear = str() if len(c)==0 else clr.e
    print(c + string + clear)

def _getChar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setraw(sys.stdin.fileno())
    while 1:
        ch = sys.stdin.read(1)
        if ch is not None:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

def _gh(c_list, m):
    l = len(c_list)
    i = 0
    s = str()
    while i<m:
        i+=1
        s+=c_list[i%l]
    return s

def _get_bet(mx, b=1):
    b = mx if b > mx else b
    ok = True
    print('\rBet: $%s'%b),
    while ok: 
        c = _getChar()
        if c == "z":
            b+=1
        elif c == "s":
            b-=1
        elif c == "d":
            ok = False
        elif c == "q":
            print('\nBye!')
            sys.exit(0)
        else:
            continue
        b = 1 if b < 1 else b
        b = mx if b > mx else b
        print('\rBet: $%s'%b),
    return b


numbers = [2,3,4,5,6,7,8,9,10,11,10,10,10]

def round():
    o = 0
    tot = 0
    game = True
    outcome = None  # 0: lost, 1: draw, 2: won
    cprint("D: DRAW, *: STOP", clr.y)
    while game:
        i = _getChar()
        if str(i) != "d":
            game = False
        else:
            n=numbers[int(random()*len(numbers))]
            tot+=n
            print("\r%s (draw: %s)                      " % (str(tot), str(n))),
            if tot==21:
                game = False
            elif tot>21:
                cprint('\n[OVERDRAW]', clr.y)
                outcome = 0
                game = False
    print
    if outcome == 0:
        pass
    else:
        while o < 16: 
            n=numbers[int(random()*len(numbers))]
            o+=n
            cprint("BANK: %s (draw: %s)   " % (o, n), clr.gr)
            sleep(0.5)
        if tot > o or o > 21:
            outcome = 2
        elif tot < o:
            outcome = 0
        else:
            outcome = 1
    return outcome

def bet():
    money = 250
    rnd = 0
    last_bet = 1
    while money>0:
        rnd+=1
        cprint("Z:+ | S:- | D: OK | Q: QUIT", clr.y)
        bet_ok = True
        while bet_ok:
            print("[$%s remaining]"%money)
            bet = _get_bet(money, last_bet)
            try:
                if int(bet) > 0 and money - int(bet) >= 0:
                    money -= int(bet)
                    bet_ok = False
            except:
                pass
        bet = int(bet)
        cprint('\rYour bet: $%s\n'%bet, clr.g)
        last_bet = bet
        res = round()
        cprint(_gh("*+*", 41), clr.b)
        if res == 1:
            cprint("You get your bet of $%s back"%bet, clr.y)
        elif res ==0:
            cprint("You lose $%s"%bet, clr.r)
            bet=0
        else:
            bet*=2
            cprint("You win $%s"%bet, clr.g)
        money+=bet
        print('\n')
    cprint("GAME OVER!", clr.r)


bet()
