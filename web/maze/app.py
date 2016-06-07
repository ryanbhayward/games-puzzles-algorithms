import json

from flask import Flask, render_template, request

from games_puzzles_algorithms.puzzles.maze_puzzle import MazePuzzle
from games_puzzles_algorithms.search.breadth_first_search import BreadthFirstSearch
from games_puzzles_algorithms.search.depth_first_search import DepthFirstSearch
from games_puzzles_algorithms.search.a_star import AStar

app = Flask(__name__)

SOLVERS = {
    "A*": AStar,
    "bfs": BreadthFirstSearch,
    "dfs": DepthFirstSearch
}

# MAZE VARIABLES
maze = MazePuzzle()
str_solver = "bfs"
solver = SOLVERS[str_solver](maze, -1)
search_steps = 0
steps = 0


@app.route("/", methods=['GET'])
def index():
    """
    Route for the index page. Links to the maze and the sliding tile web implementations.
    :return: HTML template for index
    """
    return render_template('index.html')


@app.route("/state", methods=['GET'])
def state():
    """
    Return the current state of the puzzle
    :return: JSON object representing the state of the maze puzzle
    """
    json_state = {'maze': maze.array(), 'solver': str_solver, 'steps': steps, 'search_steps': search_steps}
    return json.dumps(json_state)


@app.route("/refresh", methods=['GET'])
def refresh():
    global maze, search_steps, steps
    width = len(maze.hor[0]) - 1
    height = len(maze.hor) - 1
    print(width, height)
    maze = MazePuzzle(width=width, height=height)
    _instantiate_solver(str_solver)
    search_steps = 0
    steps = 0
    return state()


@app.route("/move", methods=['POST', 'PUT'])
def move():
    global steps
    raw_move = request.form['move']
    if raw_move in maze.str_moves(maze.valid_moves()):
        maze.apply_move(raw_move)
        steps += 1
        _instantiate_solver(str_solver)
    return state()


@app.route("/set_search", methods=['POST'])
def set_search():
    """
    Change the current search to use specified solver
    """
    _instantiate_solver(request.form['search'])
    return state()


@app.route("/set_size", methods=['POST'])
def set_size():
    """
    Change the current solver to use specified solver
    """
    global maze
    try:
        raw_width = int(request.form['width'])
        raw_height = int(request.form['height'])
        maze = MazePuzzle(width=raw_width, height=raw_height)
        _instantiate_solver(str_solver)
    except ValueError:
        pass
    return state()


@app.route("/search_step", methods=['GET'])
def search_step():
    global search_steps
    solved, step = solver.step(verbose=False, tick=search_steps)
    search_steps += 1
    if solved is None:
        data = {'solved': None}
    elif not solved:
        data = {'solved': solved, 'maze': step.array()}
    else:
        data = {'solved': solved, 'solution': step}
        _instantiate_solver(str_solver)
    return json.dumps(data)


def _instantiate_solver(raw_str_solver):
    global str_solver, solver
    if raw_str_solver in SOLVERS.keys():
        str_solver = raw_str_solver
        if raw_str_solver == 'A*':
            solver = SOLVERS[raw_str_solver](maze, -1, maze.heuristic('raw_distance'))
        else:
            solver = SOLVERS[raw_str_solver](maze, -1)

if __name__ == "__main__":
    app.run()
