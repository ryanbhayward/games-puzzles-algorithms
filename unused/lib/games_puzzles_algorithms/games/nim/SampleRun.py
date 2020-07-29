import Board


b = Board.Board()
b.print_heap()

while not b.is_game_over():
    b.user_move()

    if b.is_game_over():
        break

    b.computer_move()
