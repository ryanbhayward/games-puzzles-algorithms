import json

from flask import Flask, render_template, request

from games_puzzles_algorithms.puzzles.maze_puzzle import MazePuzzle
from games_puzzles_algorithms.puzzles.solvable_sliding_tile_puzzle import SolvableSlidingTilePuzzle as SlidingTilePuzzle
from games_puzzles_algorithms.search.breadth_first_search import BreadthFirstSearch
from games_puzzles_algorithms.search.depth_first_search import DepthFirstSearch
from games_puzzles_algorithms.search.a_star import AStar

app = Flask(__name__)

SOLVERS = {
    "A*": AStar,
    "bfs": BreadthFirstSearch,
    "dfs": DepthFirstSearch
}


@app.route("/", methods=['GET'])
def index():
    """
    Route for the index page. Links to the maze and the sliding tile web implementations.
    :return: HTML template for index
    """
    return render_template('index.html')


# * * * * * * * * * * * * * * * * * * * *
# MAZE SECTION
# * * * * * * * * * * * * * * * * * * * *

# MAZE VARIABLES
maze = MazePuzzle(width=20, height=20)
maze_str_solver = "bfs"
maze_solver = SOLVERS[maze_str_solver](maze, -1)
maze_search_steps = 0
maze_steps = 0


@app.route("/maze", methods=['GET'])
def maze_index():
    """
    Route for the maze implementations.
    :return: HTML template for index
    """
    return render_template('maze.html')


@app.route("/maze/state", methods=['GET'])
def maze_state():
    """
    Return the current state of the puzzle
    :return: JSON object representing the state of the maze puzzle
    """
    json_state = {'maze': maze.array(), 'solver': maze_str_solver, 'steps': maze_steps,
                  'search_steps': maze_search_steps}
    return json.dumps(json_state)


@app.route("/maze/refresh", methods=['GET'])
def maze_refresh():
    global maze, maze_search_steps, maze_steps
    width = len(maze.hor[0]) - 1
    height = len(maze.hor) - 1
    maze = MazePuzzle(width=width, height=height)
    _instantiate_maze_solver(maze_str_solver)
    maze_search_steps = 0
    maze_steps = 0
    return maze_state()


@app.route("/maze/move", methods=['POST', 'PUT'])
def maze_move():
    global maze_steps
    raw_move = request.form['move']
    if raw_move in maze.str_moves(maze.valid_moves()):
        maze.apply_move(raw_move)
        maze_steps += 1
        _instantiate_maze_solver(maze_str_solver)
    return maze_state()


@app.route("/maze/set_search", methods=['POST'])
def maze_set_search():
    """
    Change the current search to use specified solver
    """
    _instantiate_maze_solver(request.form['search'])
    return maze_state()


@app.route("/maze/set_size", methods=['POST'])
def maze_set_size():
    """
    Change the current solver to use specified solver
    """
    global maze
    try:
        raw_width = int(request.form['width'])
        raw_height = int(request.form['height'])
        maze = MazePuzzle(width=raw_width, height=raw_height)
        _instantiate_maze_solver(maze_str_solver)
    except ValueError:
        pass
    return maze_state()


@app.route("/maze/search_step", methods=['GET'])
def maze_search_step():
    global maze_search_steps
    solved, step = maze_solver.step(verbose=False, tick=maze_search_steps)
    maze_search_steps += 1
    if solved is None:
        data = {'solved': None}
    elif not solved:
        data = {'solved': solved, 'maze': step.array()}
    else:
        data = {'solved': solved, 'solution': step}
        _instantiate_maze_solver(maze_str_solver)
    return json.dumps(data)


def _instantiate_maze_solver(raw_str_solver):
    global maze_str_solver, maze_solver
    if raw_str_solver in SOLVERS.keys():
        maze_str_solver = raw_str_solver
        if raw_str_solver == 'A*':
            maze_solver = SOLVERS[raw_str_solver](maze, -1, maze.heuristic('raw_distance'))
        else:
            maze_solver = SOLVERS[raw_str_solver](maze, -1)


# * * * * * * * * * * * * * * * * * * * *
# SLIDING TILE SECTION
# * * * * * * * * * * * * * * * * * * * *

# SLIDING TILE VARIABLES
sliding_tile = SlidingTilePuzzle(size1=3, size2=3)
sliding_tile_str_solver = "bfs"
sliding_tile_solver = SOLVERS[sliding_tile_str_solver](maze, -1)
sliding_tile_search_steps = 0
sliding_tile_steps = 0


@app.route("/sliding_tile", methods=['GET'])
def sliding_tile_index():
    """
    Route for the maze implementations.
    :return: HTML template for index
    """
    sliding_tile_refresh()  # issue with the 2D array code, fixed by reinstating the sliding tile puzzle
    return render_template('sliding_tile.html')


@app.route("/sliding_tile/state", methods=['GET'])
def sliding_tile_state():
    """
    Return the current state of the puzzle
    :return: JSON object representing the state of the maze puzzle
    """
    json_state = {'sliding_tile': sliding_tile.array(), 'solver': sliding_tile_str_solver, 'steps': sliding_tile_steps,
                  'search_steps': sliding_tile_search_steps, 'size1': sliding_tile.size1, 'size2': sliding_tile.size2}
    return json.dumps(json_state)


@app.route("/sliding_tile/refresh", methods=['GET'])
def sliding_tile_refresh():
    global sliding_tile, sliding_tile_search_steps, sliding_tile_steps
    sliding_tile = SlidingTilePuzzle(size1=sliding_tile.size1, size2=sliding_tile.size2)
    _instantiate_sliding_tile_solver(sliding_tile_str_solver)
    sliding_tile_search_steps = 0
    sliding_tile_steps = 0
    return sliding_tile_state()


@app.route("/sliding_tile/move", methods=['POST', 'PUT'])
def sliding_tile_move():
    global sliding_tile_steps
    raw_move = request.form['move']
    if raw_move in sliding_tile.str_moves(sliding_tile.valid_moves()):
        sliding_tile.apply_move(raw_move)
        sliding_tile_steps += 1
        _instantiate_sliding_tile_solver(sliding_tile_str_solver)
    return sliding_tile_state()


@app.route("/sliding_tile/set_search", methods=['POST'])
def sliding_tile_set_search():
    """
    Change the current search to use specified solver
    """
    _instantiate_sliding_tile_solver(request.form['search'])
    return sliding_tile_state()


@app.route("/sliding_tile/set_size", methods=['POST'])
def sliding_tile_set_size():
    """
    Change the current solver to use specified solver
    """
    global sliding_tile
    try:
        raw_size_1 = int(request.form['size1'])
        raw_size_2 = int(request.form['size2'])
        sliding_tile = SlidingTilePuzzle(size1=raw_size_1, size2=raw_size_2)
        _instantiate_sliding_tile_solver(sliding_tile_str_solver)
    except ValueError:
        pass
    return sliding_tile_state()


@app.route("/sliding_tile/search_step", methods=['GET'])
def sliding_tile_search_step():
    global sliding_tile_search_steps
    solved, step = sliding_tile_solver.step(verbose=False, tick=sliding_tile_search_steps)
    sliding_tile_search_steps += 1
    if solved is None:
        data = {'solved': None}
    elif not solved:
        data = {'solved': solved, 'sliding_tile': step.array()}
    else:
        data = {'solved': solved, 'solution': sliding_tile.str_moves(step)}
        _instantiate_sliding_tile_solver(sliding_tile_str_solver)
    return json.dumps(data)


def _instantiate_sliding_tile_solver(raw_str_solver):
    global sliding_tile_str_solver, sliding_tile_solver
    if raw_str_solver in SOLVERS.keys():
        sliding_tile_str_solver = raw_str_solver
        if raw_str_solver == 'A*':
            sliding_tile_solver = SOLVERS[raw_str_solver](sliding_tile, -1,
                                                          sliding_tile.heuristic('manhattan distance'))
        else:
            sliding_tile_solver = SOLVERS[raw_str_solver](sliding_tile, -1)


if __name__ == "__main__":
    app.run()
