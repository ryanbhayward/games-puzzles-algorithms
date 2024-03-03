# MCTS-Hex

## Contributors

Luke Schultz <br>
Kamillah Hasham <br>
Zhihong Piao <br>

## Makefile

`make runs`
executes main.py which starts the CLI

## CLI Instructions

| Command | Description | Example |
| --- | --- | --- |
| `x <column><row>` | makes x move at (column, row) | `x a4` |
| `o <column><row>` | makes o move at (column, row) | `o i12` |
| `. <column><row>` | sets board to blank at (column, row) | `. a3` |
| `show` | prints the board | |
| `size <dimension>` | sets the board size, and resets the game | `size 7` |
| `reset`| resets the game | |
| `undo` | undoes previous change to game state | |
| `mcts <player>` | runs Monte Carlo Tree Search to make move for given player | `mcts x` |
| `gameversion <version>` | selects the version of board implementation | `gameversion 2` |
| `mctsversion <version>` | selects the version of mcts implementation | `mctsversion 0` |
| `exit`, `quit`, `q` | exits the CLI | |

## Versions

There are different implementations of Hex, and MCTS given.

| Version | File | Description |
| --- | --- | --- |
| Hex0 | `hex_game0.py` | 1d list representation, DFS win checking |
| Hex1 | `hex_game1.py` | 1d numpy array representation, DFS win checking |
| Hex2 | `hex_game2.py` | 1d numpy array representation, UnionFind win checking |
| MCTS0 | `mcts0.py` | Standard MCTS implementation |
| MCTS1 | `mcts1.py` | Backs up proven wins and loses |

## TODO

1. Setup testsuit
2. Debugging / verbose output
3. Simple bridges
4. Transposition Table
