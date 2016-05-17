# games-puzzles-algorithms
software for CMPUT 396: ugrad course on games, puzzles, algorithms

## Puzzles

Currently, Sliding Tile and Maze puzzles are defined and working.

### Quick Start

* Create a new virtual environment and activate the environment
```bash
virtualenv -p python3 venv
source venv/bin/activate
```
* Navigate to the **lib** directory and install the requirements
```bash
cd lib
pip install -r requirements.txt
```

* If using the sliding tile puzzle, also install numpy
```bash
pip install numpy
```

* Run the `main.py` within the **ui** directory
```bash
python3 games_puzzles_algorithms/ui/main.py
# full version
python3 games_puzzles_algorithms/ui/main.py --puzzle maze --search A*
# alternatively
python3 games_puzzles_algorithms/ui/main.py --puzzle sliding_tile --search A*
```
