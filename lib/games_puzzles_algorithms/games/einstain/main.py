#print ("helloworld")
import itertools
import random

size = 5
numStone = 6
board = [[0 for x in range(size)] for y in range(size)]
player1 =[[0 for x in range(2)] for y in range(numStone)]
player2 =[[0 for x in range(2)] for y in range(numStone)]
player1_l =[1 for x in range(numStone)]
player2_l =[1 for x in range(numStone)]

position1 =[[0,0],[0,1],[1,0],[0,2],[2,0],[1,1]]
position2 =[[4,4],[4,3],[3,4],[4,2],[2,4],[3,3]]


def getPositions(playerPosition):
    a=[x for x in itertools.permutations(playerPosition)]
    b = random.randint(0,len(a)-1)
    return a[b]




#####################################################
'''initializing'''
#####################################################
def setBoard():
    i =1
    #print(player1)
    for j in player1:
        #print (j)
        #print (i)
        board[j[1]][j[0]] =i
        i+=1
    i =1
    for j in player2:
        board[j[1]][j[0]] =-i
        i+=1
    
def initialBoard():
    global player1,player2
   
    player1=getPositions(position1)
    player2=getPositions(position2)
    
    #print(player1)
    #print(player2)
    setBoard()

def printBoard():
    result = ""
    for i in board:
        for j in i: 
            result+=(" "+str(j)) if j>=0 else (str(j))
            result+=" "
        result+="\n"
    print(result)

#####################################################
    '''player move'''
#####################################################
def rollDice():
    return random.randint(1,numStone)

def findStone(player_l,dice):
    result = []
    
    if (player_l[dice-1] > 0):
        result.append(dice-1)
    else:
        i = dice-2
        j = dice
        while (i>=0):
            if(player_l[i]>0):
                result.append(i)
                break
            i+= -1
        while (j<size):
            if(player_l[j]>0):
                result.append(j)
                break
            j+= 1
    return result
    
def genMoveRandom(player,valid_l,mod):
    stone = valid_l[random.randint(0,len(valid_l)-1)]
    moves = []
    x,y = player[stone]
    if(not (x+ mod*1) in range(0,size)):
        moves.append(mod*1)
    elif (not (y+mod*1) in range(0,size)):
        moves.append(mod*3)
    else:
        moves.append(mod*1)
        moves.append(mod*2)
        moves.append(mod*3)
    return (stone,moves[random.randint(0,len(moves)-1)])


def makeMove(player,stone,move):
    x,y = player[stone]
    ss = board[y][x]
    if(move == -1):
        s= board[y-1][x]
        if s >0 :
            player1_l[s-1]=0
        elif s<0:
            player2_l[(-1*s)-1]=0
        board[y][x]=0
        board[y-1][x]=ss
        player[stone][0] = x
        player[stone][1] = y-1
    elif(move == -2):
        s= board[y-1][x-1]
        if s >0 :
            player1_l[s-1]=0
        elif s<0:
            player2_l[(-1*s)-1]=0
        board[y][x]=0
        board[y-1][x-1]=ss
        player[stone][0] = x-1
        player[stone][1] = y-1
    elif(move == -3):
        s= board[y][x-1]
        if s >0 :
            player1_l[s-1]=0
        elif s<0:
            player2_l[(-1*s)-1]=0
        board[y][x]=0
        board[y][x-1]=ss
        player[stone][0] = x-1
        player[stone][1] = y
    elif(move == 1):
        s= board[y+1][x]
        if s >0 :
            player1_l[s-1]=0
        elif s<0:
            player2_l[(-1*s)-1]=0
        board[y][x]=0
        board[y+1][x]=ss
        print(player)
        print(player[stone])
        print(player[stone][0])
        player[stone][0] = x
        player[stone][1] = y+1
    elif(move == 2):
        s= board[y+1][x+1]
        if s >0 :
            player1_l[s-1]=0
        elif s<0:
            player2_l[(-1*s)-1]=0
        board[y][x]=0
        board[y+1][x+1]=ss
        player[stone][0] = x+1
        player[stone][1] = y+1
    elif(move == 3):
        s= board[y][x+1]
        if s >0 :
            player1_l[s-1]=0
        elif s<0:
            player2_l[(-1*s)-1]=0
        board[y][x]=0
        board[y][x+1]=ss
        player[stone][0] = x+1
        player[stone][1] = y
 #           player1[s-1] =(0,0)
        
    

def checkWin():
    result =0
    if board[0][0] <0 :
        result =-1
    elif board[size-1][size-1]>0:
        result =1
    return result

#####################################################
    '''main'''
#####################################################
def main():
    initialBoard()
    printBoard()
    print("greetings the game has begun, type quit to quit")
    line = input()
    while(not line == "quit"):
        a = rollDice()
        b = findStone(player1_l,a)
        for ii in range(0,len(b)):
            b[ii] = b[ii]+1
        print("you rolled "+ str(a) + " and your available stones to choose is "+ str(b))
        print("input your chosen stone and your move, 1 for virtical, 2 for diagnal and 3 for horizontal moves. For exg,  4 3 : stone 4 move horizontally to the right")
        line = input()

        stone,move = line.split()
        makeMove(player1,int(stone)-1,int(move))
        r=checkWin()
        printBoard()
        
        print(r)

        print("now opponent turn")
        line = input()
        c = rollDice()
        d = findStone(player2_l,c)
        e,f = genMoveRandom(player2,d,-1)
        print("his roll is "+ str(c)+" stone and move:" + str(e+1)+" " +str(f))
        line = input()
        makeMove(player2,e,f)
        printBoard()
        r = checkWin()
        print(r)
        line=input()
main()
