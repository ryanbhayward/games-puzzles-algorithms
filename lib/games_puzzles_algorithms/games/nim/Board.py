import random


class Board:
    def __init__(self, heap=None, num_heaps=5):
        if heap is None:
            self.num_heaps = num_heaps
            self.heap = [i + 1 for i in range(num_heaps)]
        else:
            self.num_heaps = len(heap)
            self.heap = heap

        print("Board Initialized")

    def print_heap(self):
        print("Number of heaps left: {}".format(self.num_heaps))
        print("Items in heaps :")
        for i, a in enumerate(self.heap):
            print("heap {} : {}".format(i + 1, a))

    def make_move(self, row, num):
        a = self.heap[row]

        if a == num:
            self.heap.pop(row)
            self.num_heaps -= 1
        else:
            a = a - num
            self.heap[row] = a

        print("Removed {} items from heap {}, now the board looks like "
              "this:".format(num, row + 1))
        self.print_heap()

    def nim_sum(self):
        result = 0

        for a in self.heap:
            result = result ^ a

        return result

    def user_move(self):
        row, num = input("Enter row and number of items you want to take "
                         "separated with a space ex.(1 2):  ").split()

        row, num = int(row) - 1, int(num)

        # handles input here
        try:
            if row <= -1:
                raise
            if num > 0 and num <= self.heap[row]:
                self.make_move(row, num)
            else:
                print("WRONG NUMBER TRY AGAIN")
                self.user_move()
        except:
            print("WRONG ROW TRY AGAIN")
            self.user_move()

        if self.is_game_over():
            print("YOU WIN")

    def computer_move(self):
        print("Now it's my turn")

        # no winning move, make a random move
        if self.nim_sum() == 0:
            row = random.randint(0, self.num_heaps - 1)
            num = random.randint(1, self.heap[row])
            self.make_move(row, num)

        # make the winning move
        else:
            s = self.nim_sum()
            for i, row in enumerate(self.heap):
                x = s ^ row

                if x < row:
                    x = row ^ s
                    self.make_move(i, row - x)
                    break

        if self.is_game_over():
            print("YOU LOST")

    def is_game_over(self):
        return all(z == 0 for z in self.heap)

    def who_has_win(self):
        if self.nim_sum() == 0:
            return "Next player to play has a winning move"
        else:
            return "Current player has a winning move"

    def board_reset(self, heap):
        self.heap = heap
        self.num_heaps = len(heap)
