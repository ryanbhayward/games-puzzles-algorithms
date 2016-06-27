# games-puzzles-algorithms
software for CMPUT 396: ugrad course on games, puzzles, algorithms

## Puzzles

Currently, Sliding Tile and Maze puzzles are defined and working.

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

