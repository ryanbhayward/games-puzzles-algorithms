'''
This is a program to check the correctness of a given sequence
in a given stile search from beginning to end.

For our marking scheme we had 6 different cases:
    - Everything is right                       4/4
    - If the blank has been moved
      instead of tiles                          3/4
    - If the order is reversed                  3/4
    - If the blank has been moved
      in reverse order                          2/4
    - If the sequence is right, but longer
      than the minimum necessary moves          1/4
    - If the sequence is wrong                  0/4

The main class here is -Verify()-. It takes the sequence and the version
of the input-output tiles as the initial input. 

TO USE: Just pick the version you want to run for(or manually add a new
one using the pick_vs method in Verify) and change the version number to
the desired one. Change the sequence to check using to_check variable.
And run.
'''
import sys

def blank_move(seq):
    # move the blank instead
    new_seq = ""
    rev_dict = {'R': 'L', 'L': 'R', 'U': 'D', 'D': 'U'}
    for i in seq:
        try:
            new_seq += rev_dict[i]
        except Exception:
            print('Error on the input, found:', i)
            print('You are only allowed {R, L, D, U}')
            sys.exit()
    return new_seq

class Verify:
    def __init__(self, to_check, version = 1):
        self.init_pos, self.end_pos = self.pick_vs(version)
        self.cur_pos = self.find_cur_space(self.init_pos)
        self.to_check = to_check

    def slide(self):
        for move in self.to_check:
            if move == 'D': # Up
                # check if legal
                # make the move
                if self.cur_pos[0] - 1 >= 0: # legal
                    temp = self.init_pos[self.cur_pos[0]][self.cur_pos[1]]
                    self.init_pos[self.cur_pos[0]][self.cur_pos[1]] = self.init_pos[self.cur_pos[0] - 1][self.cur_pos[1]]
                    self.init_pos[self.cur_pos[0] - 1][self.cur_pos[1]] = temp
                    self.cur_pos[0]-=1
                else:
                    break
                
            elif move == 'U': # Down
                if self.cur_pos[0] + 1 <= len(self.init_pos)-1: # legal
                    temp = self.init_pos[self.cur_pos[0]][self.cur_pos[1]]
                    self.init_pos[self.cur_pos[0]][self.cur_pos[1]] = self.init_pos[self.cur_pos[0] + 1][self.cur_pos[1]]
                    self.init_pos[self.cur_pos[0] + 1][self.cur_pos[1]] = temp
                    self.cur_pos[0] += 1
                else:
                    break
                
            elif move == 'R': # Left
                if self.cur_pos[1] - 1 >= 0: # legal
                    temp = self.init_pos[self.cur_pos[0]][self.cur_pos[1]]
                    self.init_pos[self.cur_pos[0]][self.cur_pos[1]] = self.init_pos[self.cur_pos[0]][self.cur_pos[1] - 1]
                    self.init_pos[self.cur_pos[0]][self.cur_pos[1] - 1] = temp
                    self.cur_pos[1] -= 1
                else:
                    break
                
            elif move == 'L': # Right
                if self.cur_pos[1] + 1 < len(self.init_pos[0]): # legal
                    temp = self.init_pos[self.cur_pos[0]][self.cur_pos[1]]
                    self.init_pos[self.cur_pos[0]][self.cur_pos[1]] = self.init_pos[self.cur_pos[0]][self.cur_pos[1] + 1]
                    self.init_pos[self.cur_pos[0]][self.cur_pos[1] + 1] = temp
                    self.cur_pos[1] += 1
                else:
                    break
            # self.print_tile(self.init_pos)

    def check(self):
        if self.end_pos == self.init_pos:
            return True
        else:
            return False

    def pick_vs(self, vs):
        # ss0
        if vs == 0:
            return [[5, 1, 7, 3], [2, 6, 4, 0]],[[1, 2, 3, 4], [5, 6, 7, 0]]    
        # ss1
        elif vs == 1:
            return [[6, 2, 4, 7], [1, 5, 3, 0]],[[1, 2, 3, 4], [5, 6, 7, 0]]
        # ss2
        elif vs == 2:
            return [[2, 5, 7, 3], [1, 6, 4, 0]],[[1, 2, 3, 4], [5, 6, 7, 0]]
        # ss3
        elif vs == 3:
            return [[5, 2, 4, 7], [6, 1, 3, 0]],[[1, 2, 3, 4],[5, 6, 7, 0]]
        # ss4
        elif vs == 4:
            return [[6, 2, 7, 3], [1, 5, 4, 0]],[[1, 2, 3, 4], [5, 6, 7, 0]]
        # ss5
        elif vs == 5:
            return [[5, 1, 4, 7], [2, 6, 3, 0]], [[1, 2, 3, 4], [5, 6, 7, 0]]

    def print_tile(self, tile):
        for i in tile:
            print(i)
        print('')

    def find_cur_space(self, tile):
        for i, x in enumerate(tile):
            for j, y in enumerate(x):
                if y == 0:
                    return [i, j]

def main(to_check, version):
    # 4 different versions to check
    reversed_check = to_check[::-1]
    moving_blank = blank_move(to_check)
    rev_moving_blank = moving_blank[::-1]

    print('-'*(len(to_check)+8))
    print('Case 1:',to_check)
    print('Case 2:',reversed_check)
    print('Case 3:',moving_blank)
    print('Case 4:',rev_moving_blank)
    print('-'*(len(to_check)+8))

    score = 0

    # Checking if normal works
    ver_norm = Verify(to_check, version=version)
    ver_norm.slide()
    if ver_norm.check():
        score = 4

    # Checking if reversed vs works
    if not score:
        ver_rev = Verify(reversed_check, version=version)
        ver_rev.slide()
        if ver_rev.check():
            score = 3

    # Checking if blank vs works
    if not score:
        ver_blank = Verify(moving_blank, version=version)
        ver_blank.slide()
        if ver_blank.check():
            score = 3
    
    # Checking if reversed blank vs works
    if not score:
        ver_rev_blank = Verify(rev_moving_blank, version=version)
        ver_rev_blank.slide()
        if ver_rev_blank.check():
            score = 2
    
    # Checking if the sequence has worked for any
    # and longer than the minimum moves needed
    if len(to_check) > 10 and score != 0:
        print("Longer sequence")
        score = 1
    print('Sequence Score:', str(score) + '/4')
    print('-'*(len(to_check)+8))

if __name__ == "__main__":
    # The sequence to check
    to_check = "RRLDLULLDRUL"
    
    # The version of i-o tile pairs to use
    version = 5

    main(to_check, version)