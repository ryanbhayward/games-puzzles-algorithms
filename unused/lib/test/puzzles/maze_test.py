from games_puzzles_algorithms.puzzles.maze_puzzle import MazePuzzle


def construct_spiral_3_by_3():
    maze = MazePuzzle(width=3, height=3)
    maze.ver = [['|   ', '|   ', '    ', '|'],
                ['|   ', '    ', '    ', '|'],
                ['|   ', '    ', '|   ', '|'],
                []]
    maze.hor = [['+---', '+---', '+---', '+'],
                ['+   ', '+   ', '+---', '+'],
                ['+---', '+   ', '+   ', '+'],
                ['+---', '+---', '+---', '+']]
    return maze


def test_maze_construction():
    maze = construct_spiral_3_by_3()
    assert maze.position == [0, 0]
    assert maze.goal == [2, 2]
    maze_as_str = "+---+---+---+\n" \
                  "|   |     $ |\n" \
                  "+   +   +---+\n" \
                  "|           |\n" \
                  "+---+   +   +\n" \
                  "| @     |   |\n" \
                  "+---+---+---+\n" \
                  "\n"
    assert str(maze) == maze_as_str


def test_maze_valid_moves():
    maze = construct_spiral_3_by_3()
    maze.position = [0, 0]
    assert MazePuzzle.str_moves(maze.valid_moves()) == ['right']
    maze.position = [1, 0]
    assert MazePuzzle.str_moves(maze.valid_moves()) == ['up', 'left']
    maze.position = [2, 0]
    assert MazePuzzle.str_moves(maze.valid_moves()) == ['up']
    maze.position = [0, 1]
    assert MazePuzzle.str_moves(maze.valid_moves()) == ['up', 'right']
    maze.position = [1, 1]
    assert MazePuzzle.str_moves(maze.valid_moves()) == ['up', 'down', 'left', 'right']
    maze.position = [2, 1]
    assert MazePuzzle.str_moves(maze.valid_moves()) == ['down', 'left']
    maze.position = [0, 2]
    assert MazePuzzle.str_moves(maze.valid_moves()) == ['down']
    maze.position = [1, 2]
    assert MazePuzzle.str_moves(maze.valid_moves()) == ['down', 'right']
    maze.position = [2, 2]
    assert MazePuzzle.str_moves(maze.valid_moves()) == ['left']


def test_maze_traversal():
    maze = construct_spiral_3_by_3()
    assert maze.position == [0, 0]
    maze.apply_move('foobar')
    assert maze.position == [0, 0]
    maze.apply_move('left')
    assert maze.position == [0, 0]
    maze.apply_move('right')
    assert maze.position == [1, 0]
    maze.apply_move('up')
    assert maze.position == [1, 1]
    maze.apply_move('up')
    assert maze.position == [1, 2]
    maze.apply_move('right')
    assert maze.position == [2, 2]


def test_maze_is_solved():
    maze = construct_spiral_3_by_3()
    assert maze.position == [0, 0]
    assert maze.goal == [2, 2]
    assert maze.is_solved() == False
    maze.apply_move('right')
    assert maze.is_solved() == False
    maze.apply_move('up')
    assert maze.is_solved() == False
    maze.apply_move('up')
    assert maze.is_solved() == False
    maze.apply_move('right')
    assert maze.is_solved() == True
