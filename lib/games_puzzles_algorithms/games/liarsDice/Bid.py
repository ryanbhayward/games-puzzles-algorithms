
class Bid:

    
    def __init__(self,q,v):
        self.quantity = q
        self.faceValue = v

        
    ''' return true if self is bigger than the new bid'''


    def isBigger(self,newBid):
        re = False
        if self.faceValue > newBid.faceValue:
            re = True
        elif self.faceValue > newBid.faceValue:
            if self.quantity > newBid.quantity:
                re = True
        return re
    ''' checks if it's a valid bid '''        
    def isValid(self,NDICE):

        return (self.quantity-1 in range(NDICE)) and (self.faceValue-1 in range(6))
