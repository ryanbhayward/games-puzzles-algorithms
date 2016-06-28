




class Point:

    def __init__(self):
        self.white_c = 0
        self.red_c = 0
        self.prev = None
        self.next = None

    def printPoint(self):

        return "White : "+ str(self.white_c) +" , red : "+str(self.red_c)


# color 1 is red color 2 is white
    def isAddable(self,color):
        if color==1:
            if self.white_c >1:
                return False
            else:
                return True
        elif color==2:
            if self.red_c >1:
                return False
            else:
                return True
    def addChecker(self,color,quant):
        if color ==1:
            self.red_c = self.red_c + quant
        elif color ==2:
            self.white_c = self.white_c+quant
