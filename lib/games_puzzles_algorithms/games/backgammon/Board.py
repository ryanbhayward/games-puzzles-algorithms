from Point import Point as Point
import random


class Board:


    def __init__(self):
        self.points = []
        a = Point()
 #       a. white_c =2
        self.points.append(a)
        for i in range(1,24):
            b = Point()
            a.next = b
            b.prev =a
#            a.red_c =i
            self.points.append(b)
            a = b
        self.points[23].white_c=2
        self.points[18].red_c =5
        self.points[16].red_c=3
        self.points[12].white_c=5
        self.points[11].red_c=5
        self.points[7].white_c=3
        self.points[5].white_c=5
        self.points[0].red_c=2
        self.redJail_c=0
        self.whiteJail_c=0


    def printBoard(self):
        i =1
        for x in self.points:
            print("Point "+str(i) +" : "+ x.printPoint())
            i+=1
    

    def rollDice(self):
        return [random.randint(1,6),random.randint(1,6)]

    def validateMove(self,point,move,color):
        point = int(point)
        move = int(move)
        if point in range(1,25):
 #           print("here1")
            if color ==1:
                p = self.points[point-1]
                if p.red_c >0:
                    for i in range(move):
                        if p==None:
                            return True
                        p = p.next
                    if p==None:
                        return True
                    elif p.white_c<2:
                        return True
            elif color ==2:
                p= self.points[point-1]
                if p.white_c>0:
                    for i in range(move):
                        if p==None:
                            return True
                        p = p.prev
                    if p==None:
                        return True
                    elif p.red_c<2:
                        return True
        return False


    def avaliableMove(self,move,color):
        for i in range (1,25):
            if self.validateMove(i,move,color):
                return True
        return False

    def checkWin(self):
        a=0
        b=0
        for x in self.points:
            a+= x.red_c
            b+= x.white_c
        a+= self.redJail_c
        b+= self.whiteJail_c

        if a==0:
            return 1
        elif b==0:
            return 2
        else:
            return 0
        
# return true if jail is empty

    def checkJail(self,color):
        if color ==1:
            return self.redJail_c ==0
        elif color ==2:
            return self.whiteJail_c==0

    def makeMove(self,point, move,color):
        point = int(point)
        move = int(move)
        p = self.points[point-1]
        t=p
        
        if color ==1:
            for i in range(move):
                if t==None:
                    p.red_c-=1
                    return None
                t = t.next
            if t==None:
                p.red_c-=1
            else:
                if t.white_c >0:
                    self.whiteJail_c+=1
                    t.white_c -=1
                t.red_c+=1
                p.red_c-=1
        elif color ==2:
            for i in range(move):
                if t==None:
                    p.white_c-=1
                    return None
                t=t.prev
            if t==None:
                p.white_c-=1
            else:
                if t.red_c >0:
                    self.redJail_c +=1
                    t.red_c-=1
                t.white_c+=1
                p.white_c-=1
                
    def release(self,point,color):
        if color ==1:
            self.redJail_c -=1
            point.red_c+=1
        elif color ==2:
            self.whiteJail_c-=1
            point.white_c+=1
    def checkEmptyPoint(self,point,color):
        point =int(point)
        if color ==1:
            p = self.points[point]
            if p.white_c<2:
                return True
        elif color ==2:
            p = self.points[24 - point]
            if p.red_c<2:
                return True


    


#  return true if it's possible to release a prisoner#
    def checkRelease(self,rolls,color):
        for x in rolls:
            if color ==1:
                if self.points[x-1].white_c<2:
                    return True
            elif color ==2:
                if self.points[24-x].red_c<2:
                    return True
        return False
        

    def userTurn(self):
        print("user's turn begin! you are red color")
        self.printBoard()
        print("rolling dice")
        roll = self.rollDice()
        print("your dice rolls are:")
        print (roll)
        print("checking if your jail is empty")
        while not self.checkJail(1) and len(roll)>0:
            print("your jail is not empty, you have "+ str(self.redJail_c) + " number of prisioner, please empty your jail first.")
            if self.checkRelease(roll,1):
                comm = input("choose your point to release your prisoner:")
                comm = int(comm)
                while self.checkEmptyPoint(comm,1) ==False or not (comm in roll):
                    comm = input("wrong input, try again")
                    comm = int(comm)
                self.points[comm-1].red_c+=1
                self.redJail_c-=1
                roll.remove(comm)
            else:
                break
        if len(roll) == 0 or not self.checkJail(1) :
            print("no more moves your turn is over")
            return 0
        while len(roll)>0:
            check = True
            for x in roll:
                if self.avaliableMove(x,1):
                    check = False
            if check:
                print("no more avaliable moves, turn end")
                return 0
                
            print ("your remaining moves are :")
            print(roll)
            print("choose your move as following: point pace. This will move one checker from the point forward that many pace. Please input valid pace from the rolls")
            comm = input()
            p,m = comm.split()
#            print(p,m)
#            print(self.validateMove(p,m,1) == False)
#            print( (int(m) in roll))
            while self.validateMove(p,m,1) == False or not int(m) in roll :
                comm = input("invalid input, try again")
                p,m = comm.split()

            p,m = int(p),int(m)
            
            self.makeMove(p,m,1)
            self.printBoard()
            roll.remove(m)
            if self.checkWin() == 1:
                print("red wins!")
                return 1

            
        print("no more move, turn end")
        return 0

    def randomPlayer(self):
        print("computer's turn")
        roll = self.rollDice()
        print("his roll:")
        print(roll)
        while not self.checkJail(2) and len(roll)>0:
            if self.checkRelease(roll,2):
                for r in roll:
                    if self.checkEmptyPoint(r,2):
                        print("release prisoner" )
                        print(r)
                        self.points[24-r].white_c+=1
                        self.whiteJail_c-=1
                        roll.remove(r)
                        break
            else:
                break
        if len(roll)==0 or not self.checkJail(2):
            return 0
        while len(roll)>0:
            check =True
            for x in roll:
                if self.avaliableMove(x,2):
                    check = False
            if check:
                print("no more avaliable moves, turn end")
                return 0
            m = roll[0]
            for i in range(24):
                if self.points[i].white_c>0 and self.validateMove(i+1,m,2):
                    self.makeMove(i+1,m,2)
                    print("move checkers:")
                    print(i+1,m)
                    roll.remove(m)
                    break
            if self.checkWin()==2:
                return 2
        return 0



                
