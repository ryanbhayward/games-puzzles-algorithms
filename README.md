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
