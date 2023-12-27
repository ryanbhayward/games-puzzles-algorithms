from collections import deque
#import hexio
#from hexio import Cell

class Cell: #############  cells #########################
  e,b,w,ch = 0,1,2, '.*@'       # empty, black, white

  def get_ptm(ch):
    return ord(ch) >> 5 # divide by the floor of 32 get player 1 or 2 based on char * or @

  def opponent(c):
    return 3-c

class WinCheck:
    def __init__(self,board):
        self.board = board

    def update(self, move):
        pass

    def check(self):
        pass


class BFSWinCheck(WinCheck):
    def __init__(self, board):
        super().__init__(board)

    def get_node_id(self,row,col):
        r1 = row - 1
        return col + (r1*self.board.c)

    def get_neighbours(self,row,col):
        pos_x = 1
        pos_y = 1
        r = []
        #if left
        if not (row-pos_x < 1): #not out of board left
            r.append([row-pos_x,col])
            #if left down
            if not (col+pos_y > self.board.c): #not out of board down
                r.append([row-pos_x,col+pos_y])

        #if right
        if not (row+pos_x > self.board.r ): #not out of board right
            r.append([row+pos_x,col])
            #if right up
            if not (col - pos_y < 1): #not out of board up
                r.append([row + pos_x, col - pos_y])

        #if up (left)
        if not (col - pos_y < 1):
            r.append([row, col - pos_y])

        #if down (right)
        if not (col + pos_y > self.board.c ):
            r.append([row , col + pos_y])

        return r

    def bfs(self,player,root):
        graph = self.board.brd
        brd_data = self.board
        visited = set()
        x_queue = deque(maxlen=brd_data.c*brd_data.r)
        y_queue = deque(maxlen=brd_data.c*brd_data.r)
        x_queue.append(root[0])
        y_queue.append(root[1])

        score = 0
        end_found = False
        if player != hexio.cell_to_char(graph[root[0]][root[1]]): # Not connected to a side
            return False
        while True:
            #while queue is not empty
            try:
                c_node = [x_queue.popleft(),
                          y_queue.popleft()]
            except IndexError:
                break

            c_id = self.get_node_id(c_node[0], c_node[1])
            visited.add(c_id)
            score += 1
            if hexio.char_to_cell(player) == Cell.b:
                if c_node[0] >= self.board.r: # token is in last row of board (right side)
                    end_found = True
                if score >= self.board.r and end_found:
                    return True
            elif hexio.char_to_cell(player) == Cell.w:
                if c_node[1] >= self.board.c: # token is in last column of board (right side)
                    end_found = True
                if score >= self.board.c and end_found:
                    return True

            for node in self.get_neighbours(c_node[0],c_node[1]):
                if player == hexio.cell_to_char(graph[node[0]][node[1]]):
                    n_id = self.get_node_id(node[0],node[1])
                    if not (n_id in visited):
                        x_queue.append(node[0])
                        y_queue.append(node[1])
        return False

    def check(self,player):
        # BFS
        if hexio.char_to_cell(player) == Cell.b:
            for i in range(1,self.board.c+1):#if top side connects to bottom side
                if self.bfs(player,[1,i]):
                    return True
        elif hexio.char_to_cell(player) == Cell.w:#if left side connects to ride side
            for i in range(1,self.board.r+1):
                if self.bfs(player,[i,1]):
                    return True
        return False


class UFWinCheck(WinCheck):
    def __init__(self, board):
        super().__init__(board)

    def update(self, move):
        # union
        pass

    def check(self):
        # find
        pass
