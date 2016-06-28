import Bid
import random

class Game:


    NDICE = 6

    
    

    def __init__(self):
        self.rolls1 = [0 for x in range(self.NDICE)]
        self.rolls2 = [0 for x in range(self.NDICE)]
        self.currentBid = Bid.Bid(2*self.NDICE,0)
        print("loading")
        print("The real excitment is in playing the game.   ----Donald Trump")
        print("the game has begun! ")
    

    def roll(self):
        self.rolls1 = [random.randint(1,6) for x in range(self.NDICE)]
        self.rolls2 = [random.randint(1,6) for x in range(self.NDICE)]

    def showRolls(self):
        print ("Here are the rolls for both players:")
        print (self.rolls1)
        print (self.rolls2)

    def validateBid(self,newBid):
        return newBid.isBigger(self.currentBid) and newBid.isValid(2*self.NDICE)

# return True if continue to next round, false if games ended
    def turn(self):
        print("your rolls are following:")
        print(self.rolls2)
        print("it's your turn now, why don't you raise a bid, type the quantity and the facevalue of your bid separate by space:")
        q, v = input().split()    
        q, v = int(q),int(v)
        newBid = Bid.Bid(q,v)
        while (not self.validateBid(newBid)):
            q, v = input("well looks like your bid is not valid, you must raise the bid higher and within possible range").split()    
            q, v = int(q),int(v)
            newBid = Bid.Bid(q,v)
        self.currentBid = newBid
        print("now it's the computer's turn")

#############################################
        answer = self.strategy1()
# you can replace this random strategy with your own
#############################################
        if(answer == "challenge" ):
            print("looks like the computer thinks you are bluffing, so he challenged you!")
            if self.challenge():
                print("the challenge was successful, game's over! you lost.")
                return False
                
            else:
                print("the challenge failed! game's over! you win!")
                return False
                
        else:
            q,v = answer.split()

            print("the computer decides to raise, and the raise is (quantity,facevalue):")
            print("("+q + " , " + v +")")
            q,v = int(q),int(v)
            self.currentBid = Bid.Bid(q,v)
            c = input("now, would you like to challenge? y for challenge, anything else for not challenge")
            if c == "y":
                if self.challenge():
                    print("the challenge was successful, game's over! you win!")
                    return False
                    
                else:
                    print("the challenge failed! game's over! you lost")
                    return False
            print("OK..")
            return True
    
    def strategy1(self):
        for x in range(10):
            q,v=random.randint(1,2*self.NDICE) , random.randint(1,6)
            newBid = Bid.Bid(q,v)
            if self.validateBid(newBid):
                return str(q) + " "+str(v)
            return "challenge"
    
# challenge return true if the challenge was successful. i.e. the current bidder lied.
    def challenge(self):
        print("a challenge has been called:")
        self.showRolls()
        v = self.currentBid.faceValue
        q = 0
        for x in self.rolls1:
            if x == v or x ==1:
                q+=1
        for x in self.rolls2:
            if x == v or x ==1:
                q+=1
        
        if self.currentBid.quantity> q:
            return True
        else:
            return False
        
        
