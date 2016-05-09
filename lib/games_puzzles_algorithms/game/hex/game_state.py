from .win_detector import WinDetector
from .color import IllegalAction, COLORS, ORIENTATION, COLOR_SYMBOLS, \
    NUM_PLAYERS, color_to_player, next_player, player_to_color, cell_str, \
    cell_str_to_cell
from array import array
from games_puzzles_algorithms.debug import log


def prod(*l):
    s = 1
    for e in l:
        s *= e
    return s


class Board(object):

    def __init__(self, *dimensions):
        self.dimensions = list(dimensions)
        if len(self.dimensions) < 1:
            self.dimensions.append(10)
        if len(self.dimensions) < 2:
            self.dimensions.append(self.dimensions[0])
        self._cells = array('I', [COLORS['none']] * len(self))

    def __len__(self):
        return prod(*self.dimensions)

    def __getitem__(self, i):
        return self._cells[i]

    def __setitem__(self, i, color):
        self._cells[i] = color

    def size(self):
        return self.dimensions

    def num_rows(self):
        return self.dimensions[0]

    def num_columns(self):
        return self.dimensions[1]

    def cell_index(self, x, y):
        return x * self.num_rows() + y

    def column(self, index):
        return index // self.num_rows()

    def row(self, index):
        return index % self.num_rows()

    def empty_cells(self):
        for y in range(self.num_columns()):
            for x in range(self.num_rows()):
                if self._cells[self.cell_index(x,y)] == COLORS["none"]:
                    yield y, x

    def cells(self):
        for y in range(self.num_columns()):
            for x in range(self.num_rows()):
                yield y, x


class GameState(object):
    """
    Stores information representing the current state of a game of hex, namely
    the board and the current turn. Also provides functions for playing the game
    and returning information about it.
    """
    neighbor_patterns = ((-1,0), (0,-1), (-1,1), (0,1), (1,0), (1,-1))

    @classmethod
    def root(self, *dimensions):
        return self(dimensions[0] if len(dimensions) > 0 else 10)

    def __init__(self, *dimensions):
        """
        Initialize the game board and give Black the first turn.
        Also create our union find structures for win checking.
        """
        self.acting_player = COLORS["black"]
        self.board = Board(*dimensions)
        self.win_detector = WinDetector.root(NUM_PLAYERS)

    def undo(self):
        pass

    def do_after_play_at_index(self, cell):
        self.play_at_index(cell)
        yield
        self.undo()

    def play(self, cell):
        """
        Play a stone of the current turns color in the passed cell.
        """
        acting_player_color = player_to_color(self.acting_player)
        if(acting_player_color == COLORS["white"]):
            self.place_white(cell)
            self.acting_player = color_to_player(COLORS["black"])
        elif(acting_player_color == COLORS["black"]):
            self.place_black(cell)
            self.acting_player = color_to_player(COLORS["white"])

    def play_at_index(self, cell):
        self.play((self.column(cell), self.row(cell)))

    def place(self, cell, player):
        """
        Place a stone of the given color regardless of whose turn it is
        """
        color = player_to_color(player)
        if(color == COLORS["white"]):
            self.place_white(cell)
        elif(color == COLORS["black"]):
            self.place_black(cell)
        else:
            raise IllegalAction("Unrecognized color")


    def place_white(self, cell):
        """
        Place a white stone regardless of whose turn it is.
        """
        my_cell_index = self.board.cell_index(*cell)
        if(self.board[my_cell_index] == COLORS["none"]):
            self.board[my_cell_index] = COLORS["white"]
        else:
            raise IllegalAction("Cell occupied")
        #if the placed cell touches a white edge connect it appropriately
        if(cell[0] == 0):
            self.white_groups.join(self.EDGE1, cell)
        if(cell[0] == len(self.board) -1):
            self.white_groups.join(self.EDGE2, cell)
        #join any groups connected by the new white stone
        for n in self.neighbors(cell):
            if(self.board[self.board.cell_index(*n)] == COLORS["white"]):
                self.white_groups.join(n, cell)

    def place_black(self, cell):
        """
        Place a black stone regardless of whose turn it is.
        """
        my_cell_index = self.board.cell_index(*cell)
        if(self.board[my_cell_index] == COLORS["none"]):
            self.board[my_cell_index] = COLORS["black"]
        else:
            raise IllegalAction("Cell occupied")
        #if the placed cell touches a black edge connect it appropriately
        if(cell[1] == 0):
            self.black_groups.join(self.EDGE1, cell)
        if(cell[1] == len(self.board) -1):
            self.black_groups.join(self.EDGE2, cell)
        #join any groups connected by the new black stone
        for n in self.neighbors(cell):
            if(self.board[self.board.cell_index(*n)] == COLORS["black"]):
                self.black_groups.join(n, cell)

    def turn(self):
        """
        Return the player with the next move.
        """
        return self.acting_player

    def set_turn(self, player):
        """
        Set the player to take the next move.
        """
        players_color = player_to_color(player)
        if(players_color in COLORS.values() and players_color !=COLORS["none"]):
            self.acting_player = player
        else:
            raise ValueError('Invalid turn: ' + str(player))

    def winner(self):
        """
        Return a number corresponding to the winning player,
        or none if the game is not over.
        """
        if(self.white_groups.connected(self.EDGE1, self.EDGE2)):
            return COLORS["white"]
        elif(self.black_groups.connected(self.EDGE1, self.EDGE2)):
            return COLORS["black"]
        else:
            return COLORS["none"]

    def neighbors(self, cell):
        """
        Return list of neighbors of the passed cell.
        """
        x = cell[0]
        y=cell[1]
        return [(n[0]+x , n[1]+y) for n in self.neighbor_patterns\
            if (0<=n[0]+x and n[0]+x<len(self.board) and 0<=n[1]+y and n[1]+y<len(self.board))]

    def __getitem__(self, cell):
        return self.board[self.board.cell_index(*cell)]

    def cell_color(self, cell):
        return self[cell]

    def color(self, player, row, column):
        return self.board[self.board.cell_index(column, row)]

    def legal_actions(self):
        for row, column in self.board.empty_cells():
            yield self.board.cell_index(column, row)

    def moves(self):
        """
        Get a list of all moves possible on the current board.
        """
        for a in self.legal_actions():
            yield (self.board.row(a), self.board.column(a))

    def num_legal_actions(self):
        return len(list(self.legal_actions()))

    def __str__(self):
        """
        Print an ascii representation of the game board.
        """
        white = 'O'
        black = '@'
        empty = '.'
        ret = '\n'
        coord_size = len(str(len(self.board)))
        offset = 1
        ret+=' '*(offset+1)
        for x in range(len(self.board)):
            ret+=chr(ord('A')+x)+' '*offset*2
        ret+='\n'
        for y in range(len(self.board)):
            ret+=str(y+1)+' '*(offset*2+coord_size-len(str(y+1)))
            for x in range(len(self.board)):
                my_cell_index = self.board.cell_index(x, y)
                if(self.board[my_cell_index] == COLORS["white"]):
                    ret+=white
                elif(self.board[my_cell_index] == COLORS["black"]):
                    ret+=black
                else:
                    ret+=empty
                ret+=' '*offset*2
            ret+=white+"\n"+' '*offset*(y+1)
        ret+=' '*(offset*2+1)+(black+' '*offset*2)*len(self.board)

        return ret
