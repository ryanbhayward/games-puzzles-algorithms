import random




class Board:


    heapNum = 5
    heap = [1,2,3,4,5]


    def __init__(self):
        print("board initialized")

    def resetBoard(self,heapNum,heap):
        self.heapNum=heapNum
        self.heap = heap


    def printHeap(self):
        print("Num of heaps left:" + str(self.heapNum))
        print("items in heaps :")
        i = 1
        for a in self.heap:
            print ("heap " + str(i) +" : "+str(a))
            i+=1
    
    def makeMove(self,row,num):
        a = self.heap[row]
        if a == num:
            self.heap.pop(row)
            self.heapNum-=1
        else:
            a = a- num
            self.heap[row] = a
        print("you removed "+str(num) +" items from heap "+str(row+1)+", now the board looks like this:")

        self.printHeap()


    def nimSum(self):
        result = 0
        for a in self.heap:
            result =result ^ a
        return result

    def winningHeap(self):
        num = self.nimSum()
        




        
    def userMove(self):
            row, num = input("Enter row and num of items you want to take separated with space ex.(1 2):  ").split()	
            row, num = int(row)-1,int(num)

            try:
                    if row <= -1: raise
                    if num>0 and num<=self.heap[row]:	
                            self.makeMove(row,num)
                    else:
                            print ("WRONG NUMBER TRY AGAIN") 
                            self.userMove()
            except:
                    print ("WRONG ROW TRY AGAIN")
                    self.userMove()
            if self.isItEnd(): print ("YOU WIN")
              

    def computerMove(self):
            print ("Now it's my turn")
            
            if self.nimSum()==0:
                row = random.randint(0,self.heapNum-1)
                num = random.randint(1,self.heap[row])
                self.makeMove(row,num)
            else:
                s = self.nimSum()
                i = 0
                for row in self.heap:
                    x = s ^ row
                    if x < row :
                        x = row ^ s
                        self.makeMove(i, row - x)
                        break
                    i +=1
                
            if self.isItEnd(): print ("YOU LOST")
            

    def isItEnd(self):
            return all(z == 0 for z in self.heap)





                
