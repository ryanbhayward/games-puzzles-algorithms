# CMPUT 396 -- Games, Puzzles, and Algorithms

Software for CMPUT 396 to allow students to explore fundamental algorithms
that are used to play games and solve puzzles.


### Quick Start (Puzzles)

#### Common Steps

* Create a new virtual environment and activate the environment
```bash
virtualenv -p python3 venv
source venv/bin/activate
```

#### Python Shell Interface

* Navigate to the **lib** directory and install the requirements
```bash
cd lib
pip install -r requirements.txt
```

## Contents

### Games


- Hex
- Go
- Tic-tac-toe
- Nim


### Puzzles

- Sliding tiles
- Maze


### Algorithms

- Uniform random game player
- Minimax game tree search
- Monte-Carlo tree search
- Breadth-first search
- Depth-first search
- A* search


## Installation

### Prerequisites

- A Python3 interpreter (both *CPython* and *PyPy* are supported)
<!-- TODO - FFI (`libffi-dev`)? -->
- `virtualenv` (Optional)
- `make` (Optional)


### Procedure

- Run `make` in the project's root directory. This will first create a Python virtual environment with `virtualenv` where the project and its Python dependencies will be installed, then install he project and its dependencies.
    - If installing without `virtualenv`, run `make install` with the `PIP` argument, specifying a different instance of `pip` that will be used to install the project and its dependencies. For example, if you have PyPy installed to `~/.pypy`, then a command like `make install PIP=~/.pypy/bin/pip` would install this project and its dependencies for use with PyPy.
    - If installing without `make`, see `Makefile` and `lib/Makefile` for more details on the commands that `make install` would run and run analogous commands manually.

<!-- TODO How does this procedure change for Windows users? -->
<!-- TODO CFFI? -->


## Development and testing

- Run tests with `make test` in the project root or `lib`.


## Running

### Go text protocol games CLI

For Hex and tic-tac-toe. To see usage run:

```bash
bin/gpa-games-cli -h
```

For example, to run Hex with the MCTS agent:

```bash
bin/gpa-games-cli hex mcts
```

Then, type help to get a list of available commands.

### Puzzles CLI

For sliding tile puzzles. To see usage run:

```bash
bin/gpa-puzzles-cli -h
```

Example usage:

```bash
bin/gpa-puzzles-cli solvable_sliding_tile "A*"
```

Then, type help to get a list of available commands.

### Web GUI

For hex:
```bash
python3 web/hex/application.py
```

For puzzles:
```bash
python3 web/puzzles/application.py
```

Then, visit http://127.0.0.1:5000/ in your browser to access the GUI.

### Tournament

To see usage run:
```bash
python3 tournament/play_tournament.py -h
```

For example, to play the MCTS hex player against the random hex player:

```bash
python3 tournament/play_tournament.py "bin/gpa-games-cli hex mcts" "bin/gpa-games-cli hex random"
```

<!-- TODO Rework this with information on how to run all executables -->
<!-- * Run the `main.py` within the **ui** directory
```bash
python3 games_puzzles_algorithms/ui/main.py
# full version
python3 games_puzzles_algorithms/ui/main.py --puzzle maze --search A*
# alternatively
python3 games_puzzles_algorithms/ui/main.py --puzzle sliding_tile --search A*
```


#### Flask Web Application

* Navigate to the **web** directory and install the requirements
```bash
cd web
pip install -r requirements.txt
# alternatively, ensure the games-puzzles-algorithms is installed
# and only install flask
```

* Run the `app.py` within the **web/puzzles** directory
    * Within your web browser, navigate to [localhost:5000](http://localhost:5000).

```bash
python3 puzzles/app.py
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 ```

``` -->
