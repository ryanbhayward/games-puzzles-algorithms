import Board


b = Board.Board()
b.print_heap()

while not b.is_it_end():
    b.user_move()

    if b.is_it_end():
        break

    b.computer_move()
