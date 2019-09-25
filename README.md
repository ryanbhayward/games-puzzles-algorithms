# CMPUT 355 -- Games, Puzzles, and Algorithms

CMPUT 396 software to solve puzzles and play games.

### Quick Start (Puzzles)

#### Common Steps

* (optional?) Create a new virtual environment and activate the environment
```bash
virtualenv -p python3 venv
source venv/bin/activate
```

#### Python Shell Interface

* (optional?) Navigate to the **lib** directory and install the requirements
```bash
cd lib
pip install -r requirements.txt
```

## Contents

### Puzzles

- Maze traversal
- Sliding tiles

### Games

- Tic-tac-toe
- Nim
- Hex
- Go


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
- `virtualenv` (Optional)
- `make` (Optional) 

<!-- TODO - FFI (`libffi-dev`)? -->


### Procedure

- Run `make` in the project's root directory. This will first create a Python virtual environment with `virtualenv` where the project and its Python dependencies will be installed, then install he project and its dependencies.
    - If installing without `virtualenv`, run `make install` with the `PIP` argument, specifying a different instance of `pip` that will be used to install the project and its dependencies. For example, if you have PyPy installed to `~/.pypy`, then a command like `make install PIP=~/.pypy/bin/pip` would install this project and its dependencies for use with PyPy.
    - If installing without `make`, see `Makefile` and `lib/Makefile` for more details on the commands that `make install` would run and run analogous commands manually.

<!-- TODO How does this procedure change for Windows users? -->
<!-- TODO CFFI? -->


## Development and testing

- Run tests with `make test` in the project root or `lib`.


## How to run programs

### how to run the game-text-protocol using command-line-interface

For Hex and tic-tac-toe. To see usage run:

```bash
bin/gpa-games-cli -h
```

Example usage (here, Hex with the MCTS agent):

```bash
bin/gpa-games-cli hex mcts
```

Then, type help to get a list of available commands.

### Puzzles CLI

For sliding tile puzzles. To see usage run:

```bash
bin/gpa-puzzles-cli -h
```

Example usage (solvable sliding tile with A*):

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

Help:
```bash
python3 tournament/play_tournament.py -h
```

Example usage (MCTS hex player versus random hex player):

```bash
python3 tournament/play_tournament.py "bin/gpa-games-cli hex mcts" "bin/gpa-games-cli hex random"
```
