import Board

b = Board.Board()
b.printHeap()
while (not b.isItEnd()):
    b.userMove()
    if(b.isItEnd()):
        break
    b.computerMove()

