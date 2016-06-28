from Board import Board


a = Board()
game =0
while game == 0:
    game =a.userTurn()
    if game ==1:
        break
    game = a.randomPlayer()

print("player"+ str(game) +"has won")
