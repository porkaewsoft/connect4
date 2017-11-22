import random
import copy
import time

random.seed(time.time() % 3000)
#k = row
#l = col
def showBoard(board):
    for k in board:
        for l in k:
            print l,
        print ""

def play(board,player,position):
    c = position
    mx = -1
    for i in range(len(board)):
        if board[i][c] == 0:
            mx = i
    if mx != -1:
        board[mx][c] = player
        return True
    return False
    
def checkWin(board,player):
    #horizontal
    win = False
    count = 0
    for k in range(len(board)):
        for offset in range(0,len(board[k])-4+1):
            count = 0
            for i in range(0,4):
                if board[k][offset+i] == player:
                    count += 1
            if count == 4:
                return True
    #vertical
    for k in range(len(board[0])):
        for offset in range(0,len(board)-4+1):
            count = 0
            for i in range(0,4):
                if board[offset+i][k] == player:
                    count += 1
            if count == 4:
                return True
    #diag L-R
    for k in range(len(board[0])-4+1):
        for offset in range(0,len(board)-4+1):
            count = 0
            for i in range(0,4):
                if board[offset+i][k+i] == player:
                    count += 1
            if count == 4:
                return True
    #diag R-L
    for k in range(3,len(board[0])):
        for offset in range(0,len(board)-4+1):
            count = 0
            for i in range(0,4):
                if board[offset+i][k-i] == player:
                    count += 1
            if count == 4:
                return True
     
    return False

def switchPlay(cplayer):
    if cplayer == 1:
        return 2
    else:
        return 1
    
def MCPlay(BOARD,player,greedy=False):
    countWin  = [0 for i in range(8)]
    countLose = [0 for i in range(8)]
    py = player
    for i in range(8):
        #print "THINK",i
        for sample in range(0,100):
            SIM_BOARD = copy.deepcopy(BOARD)
            play(SIM_BOARD,player,i)
            py = player
            for deep in range(0,20):
                py = switchPlay(py)
                pos = random.randint(0,7)
                while not play(SIM_BOARD, py, pos):
                    pos = random.randint(0,7)
                    #print pos
            win = checkWin(SIM_BOARD,player)
            py = switchPlay(player)
            lose = checkWin(SIM_BOARD,py)          
            if win:
                countWin[i] += 1
            if lose:
                countLose[i] += 1
    
    #Now, in this version only countWin is determined.
    if greedy:
        pos = countWin.index(max(countWin))
        return pos,countWin[pos]/100.0
    else:
        #Monte Carlo Sampling
        scope = sum(countWin)
        sampling = random.randint(0,scope)
        count = 0
        pos = -1
        while count < sampling:
            pos += 1
            count += countWin[pos]
        return pos,countWin[pos]/100.0

#Initialize 2-dim array with zeros     
BOARD = [ [0 for i in range(8)] for j in range(8) ]

currentPlayer = 1
winFlag = False
while winFlag == False:
    showBoard(BOARD)
    if currentPlayer == 1:
        pos = int(raw_input("P%d Play : "%currentPlayer))
    else:
        #Check if opponent will win.
        opponent_pos,conf = MCPlay(BOARD,switchPlay(currentPlayer),greedy=True)
        if conf == 1.0: 
            #Check if AI can win in next turm
            my_pos,conf = MCPlay(BOARD,currentPlayer,greedy=True)
            if conf == 1.0: #AI surely win
                pos = my_pos    
            else: #Defend at that position
                pos = opponent_pos 
        else: #Otherwise, use monte carlo strategy
            pos,conf = MCPlay(BOARD,currentPlayer,greedy=False)
        
    play(BOARD,currentPlayer,pos)

    if checkWin(BOARD,currentPlayer):
        winFlag = True
        
        print "Player %d wins !"%currentPlayer
        
    currentPlayer = switchPlay(currentPlayer)

    print "----"

showBoard(BOARD)
