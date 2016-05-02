class IllegalAction(Exception):
    pass


COLORS = {"none": 2, "white": 1, "black": 0}
ORIENTATION = ['row', 'column']
COLOR_SYMBOLS = ['@', 'O', '.']
NUM_PLAYERS = len(ORIENTATION)


def color_to_player(color):
    return color


def next_player(player):
    return int(not(player))


def player_to_color(player):
    return player


def cell_str(cell):
    return chr(ord('a') + cell[1]) + str(cell[0] + 1)


def cell_str_to_cell(string):
    column = ord(string[0].lower()) - ord('a')
    row = int(string[1:]) - 1
    return (row, column)
