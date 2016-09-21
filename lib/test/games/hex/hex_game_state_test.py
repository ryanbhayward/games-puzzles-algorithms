import pytest
import random
from games_puzzles_algorithms.games.hex.game_state import color_to_player
from games_puzzles_algorithms.games.hex.game_state import COLOR_NONE, COLOR_BLACK, COLOR_WHITE
from games_puzzles_algorithms.games.hex.game_state import GameState
from games_puzzles_algorithms.games.hex.game_state import IllegalAction


def test_one_by_one():
    state = GameState.root(1)
    assert str(state) == (
'''
  A
1  .  O
    @''')
    state.play(0)
    assert state.is_terminal() == True


def test_white_win1():
    patient = GameState.root(5)
    patient.place(patient.board.cell_index(1, 0), COLOR_WHITE)
    patient.place(patient.board.cell_index(1, 1), COLOR_WHITE)
    patient.place(patient.board.cell_index(1, 2), COLOR_WHITE)
    patient.place(patient.board.cell_index(1, 3), COLOR_WHITE)

    assert str(patient) == (
'''
  A  B  C  D  E
1  .  .  .  .  .  O
 2  O  O  O  O  .  O
  3  .  .  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
    )

    patient.place(patient.board.cell_index(1, 4), COLOR_WHITE)

    assert str(patient) == (
'''
  A  B  C  D  E
1  .  .  .  .  .  O
 2  O  O  O  O  O  O
  3  .  .  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
    )

    assert patient.winner() == COLOR_WHITE


def test_white_win2():
    patient = GameState.root(5)
    patient.place(patient.board.cell_index(1, 0), COLOR_WHITE)
    patient.place(patient.board.cell_index(1, 1), COLOR_WHITE)
    patient.place(patient.board.cell_index(1, 2), COLOR_WHITE)
    patient.place(patient.board.cell_index(1, 3), COLOR_WHITE)

    assert str(patient) == (
'''
  A  B  C  D  E
1  .  .  .  .  .  O
 2  O  O  O  O  .  O
  3  .  .  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
    )

    patient.place(patient.board.cell_index(0, 4), COLOR_WHITE)

    assert str(patient) == (
'''
  A  B  C  D  E
1  .  .  .  .  O  O
 2  O  O  O  O  .  O
  3  .  .  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
    )

    assert patient.winner() == COLOR_WHITE


def test_legal_neighbors():
    patient = GameState.root(5)
    patient.place(patient.board.cell_index(1, 1), COLOR_WHITE)
    patient.place(patient.board.cell_index(0, 1), COLOR_BLACK)

    assert str(patient) == (
'''
  A  B  C  D  E
1  .  @  .  .  .  O
 2  .  O  .  .  .  O
  3  .  .  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
    )

    num_neighbors = 5
    count = 0
    for cell in patient.board.every_legal_neighbor(1, 1):
        patient.place(patient.board.cell_index(*cell), COLOR_WHITE)
        count += 1

    assert count == num_neighbors

    assert str(patient) == (
'''
  A  B  C  D  E
1  .  @  O  .  .  O
 2  O  O  O  .  .  O
  3  O  O  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
    )


def test_neighbors():
    patient = GameState.root(5)
    patient.place(patient.board.cell_index(1, 1), COLOR_WHITE)

    assert str(patient) == (
'''
  A  B  C  D  E
1  .  .  .  .  .  O
 2  .  O  .  .  .  O
  3  .  .  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
    )

    num_neighbors = 6
    count = 0
    for cell in patient.board.every_legal_neighbor(1, 1):
        patient.place(patient.board.cell_index(*cell), COLOR_WHITE)
        count += 1

    assert count == num_neighbors

    assert str(patient) == (
'''
  A  B  C  D  E
1  .  O  O  .  .  O
 2  O  O  O  .  .  O
  3  O  O  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
    )


def test_set_colorless1():
    patient = GameState.root(5)
    patient.place(patient.board.cell_index(0, 0), COLOR_WHITE)

    with pytest.raises(IllegalAction):
        patient.place(patient.board.cell_index(0, 0), COLOR_NONE)
    assert str(patient) == (
'''
  A  B  C  D  E
1  O  .  .  .  .  O
 2  .  .  .  .  .  O
  3  .  .  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
    )


def test_set_colorless2():
    patient = GameState.root(5)

    with pytest.raises(IndexError):
        patient.place(patient.board.cell_index(0, 0), COLOR_NONE)
    assert str(patient) == (
'''
  A  B  C  D  E
1  .  .  .  .  .  O
 2  .  .  .  .  .  O
  3  .  .  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
    )


def test_with_action_applied():
    patient = GameState.root(5)
    assert patient.player_to_act() == color_to_player(COLOR_WHITE)
    for _ in patient.with_action_applied(0):
        assert patient.player_to_act() == color_to_player(COLOR_WHITE)
        assert str(patient) == (
'''
  A  B  C  D  E
1  O  .  .  .  .  O
 2  .  .  .  .  .  O
  3  .  .  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
        )
    assert patient.player_to_act() == color_to_player(COLOR_WHITE)
    assert str(patient) == (
'''
  A  B  C  D  E
1  .  .  .  .  .  O
 2  .  .  .  .  .  O
  3  .  .  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
        )


def test_two_by_two_bug():
    patient = GameState.root(2)
    patient.place(patient.board.cell_index(0, 0), COLOR_WHITE)
    patient.place(patient.board.cell_index(1, 1), COLOR_WHITE)
    patient.place(patient.board.cell_index(0, 1), COLOR_BLACK)
    patient.place(patient.board.cell_index(1, 0), COLOR_BLACK)

    assert patient.winner() == COLOR_BLACK


def test_white_moves_are_not_hidden_from_black():
    patient = GameState.root(5)
    cell = (0, 0)
    patient.place(patient.board.cell_index(*cell), COLOR_WHITE)
    patient.set_player_to_act(color_to_player(COLOR_WHITE))
    assert patient.player_to_act() == color_to_player(COLOR_WHITE)
    assert patient[cell] == COLOR_WHITE

    patient.set_player_to_act(color_to_player(COLOR_BLACK))
    assert patient.player_to_act() == color_to_player(COLOR_BLACK)
    assert patient[cell] == COLOR_WHITE

    assert str(patient) == (
'''
  A  B  C  D  E
1  O  .  .  .  .  O
 2  .  .  .  .  .  O
  3  .  .  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
    )


def test_black_moves_are_not_hidden_from_white():
    patient = GameState.root(5)
    cell = (0, 0)
    patient.place(patient.board.cell_index(*cell), COLOR_BLACK)
    patient.set_player_to_act(color_to_player(COLOR_BLACK))
    assert patient.player_to_act() == color_to_player(COLOR_BLACK)
    assert patient[cell] == COLOR_BLACK

    patient.set_player_to_act(color_to_player(COLOR_WHITE))
    assert patient.player_to_act() == color_to_player(COLOR_WHITE)
    assert patient[cell] == COLOR_BLACK

    assert str(patient) == (
'''
  A  B  C  D  E
1  @  .  .  .  .  O
 2  .  .  .  .  .  O
  3  .  .  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
    )


def test_terminal_black():
    patient = GameState.root(5)
    assert patient.winner() == COLOR_NONE
    patient.place(patient.board.cell_index(0, 0), COLOR_BLACK)
    assert patient.winner() == COLOR_NONE
    patient.place(patient.board.cell_index(1, 0), COLOR_BLACK)
    assert patient.winner() == COLOR_NONE
    patient.place(patient.board.cell_index(2, 0), COLOR_BLACK)
    assert patient.winner() == COLOR_NONE
    patient.place(patient.board.cell_index(3, 0), COLOR_BLACK)
    assert patient.winner() == COLOR_NONE
    patient.place(patient.board.cell_index(4, 0), COLOR_BLACK)
    assert patient.winner() == COLOR_BLACK


def test_terminal_black():
    patient = GameState.root(5)
    assert patient.winner() == COLOR_NONE
    patient.place(patient.board.cell_index(0, 0), COLOR_BLACK)
    assert patient.winner() == COLOR_NONE
    patient.place(patient.board.cell_index(1, 0), COLOR_BLACK)
    assert patient.winner() == COLOR_NONE
    patient.place(patient.board.cell_index(2, 0), COLOR_BLACK)
    assert patient.winner() == COLOR_NONE
    patient.place(patient.board.cell_index(3, 0), COLOR_BLACK)
    assert patient.winner() == COLOR_NONE
    patient.place(patient.board.cell_index(4, 0), COLOR_BLACK)
    assert patient.winner() == COLOR_BLACK

    patient.set_player_to_act(color_to_player(COLOR_WHITE))
    patient.undo()
    assert patient.winner() == COLOR_NONE


def test_terminal_white():
    patient = GameState.root(5)
    assert patient.winner() == COLOR_NONE
    patient.place(patient.board.cell_index(0, 0), COLOR_WHITE)
    assert patient.winner() == COLOR_NONE
    patient.place(patient.board.cell_index(0, 1), COLOR_WHITE)
    assert patient.winner() == COLOR_NONE
    patient.place(patient.board.cell_index(0, 2), COLOR_WHITE)
    assert patient.winner() == COLOR_NONE
    patient.place(patient.board.cell_index(0, 3), COLOR_WHITE)
    assert patient.winner() == COLOR_NONE
    patient.place(patient.board.cell_index(0, 4), COLOR_WHITE)
    assert patient.winner() == COLOR_WHITE


def test_board_prints():
    patient = GameState.root(5)

    assert str(patient) == (
'''
  A  B  C  D  E
1  .  .  .  .  .  O
 2  .  .  .  .  .  O
  3  .  .  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
    )


def test_move_made_twice():
    patient = GameState.root(5)
    patient.play(patient.board.cell_index(0, 0))

    with pytest.raises(IllegalAction) as excinfo:
        patient.play(patient.board.cell_index(0, 0))
    assert 'stone already on cell' in str(excinfo.value)


def test_play_move():
    patient = GameState.root(6, 5)
    patient.play(patient.board.cell_index(1, 2))
    assert str(patient) == (
'''
  A  B  C  D  E
1  .  .  .  .  .  O
 2  .  .  O  .  .  O
  3  .  .  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
     6  .  .  .  .  .  O
         @  @  @  @  @'''
    )


def test_undo():
    patient = GameState.root(5)
    patient.play(patient.board.cell_index(0, 0))
    patient.undo()
    assert str(patient) == (
'''
  A  B  C  D  E
1  .  .  .  .  .  O
 2  .  .  .  .  .  O
  3  .  .  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
    )

def test_border_cells():
    patient = GameState.root(5)
    border_cells = patient.board.border_cells(0, -1)
    expected_cells = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]
    assert border_cells == expected_cells
    border_cells = patient.board.border_cells(0, -2)
    expected_cells = [(4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]
    assert border_cells == expected_cells
    border_cells = patient.board.border_cells(1, -1)
    expected_cells = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
    assert border_cells == expected_cells
    border_cells = patient.board.border_cells(1, -2)
    expected_cells = [(0, 4), (1, 4), (2, 4), (3, 4), (4, 4)]
    assert border_cells == expected_cells

def test_connected_neighbors_with_edge():
    patient = GameState.root(5)
    neighbors = []
    for neighbor in patient.board.connected_neighbors(-1, 1):
        neighbors.append(neighbor)

    neighbors.sort()
    expected = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
    assert expected == neighbors

def test_connected_neighbors_with_border_cell():
    patient = GameState.root(5)
    neighbors = []
    for neighbor in patient.board.connected_neighbors((0, 0), 0):
        neighbors.append(neighbor)

    assert -1 in neighbors
    neighbors.remove(-1)
    neighbors.sort()
    expected = [(0, 1), (1, 0)]
    assert expected == neighbors

def test_connected_neighbors_with_played_cell():
    patient = GameState.root(5)
    patient.play(patient.board.cell_index(4, 4))
    patient.play(patient.board.cell_index(1, 1))
    neighbors = []
    for neighbor in patient.board.connected_neighbors((0, 1), 0):
        neighbors.append(neighbor)

    assert -1 in neighbors
    neighbors.remove(-1)
    neighbors.sort()
    expected = [(1, 0), (0, 0), (0, 2), (2, 0), (1, 2), (2, 1)]
    expected.sort()
    assert expected == neighbors

def test_dijkstra_distance():
    patient = GameState.root(5)
    distance = patient.board.dijkstra_distance(0, -1, -2)
    assert distance == 6

def test_dijkstra_distance_with_played_cell():
    patient = GameState.root(5)
    patient.play(patient.board.cell_index(2, 0))
    distance = patient.board.dijkstra_distance(1, -1, -2)
    assert distance == 5

def test_heuristic():
    patient = GameState.root(5)
    assert patient.heuristic(0) == 0

def test_heuristic_with_played_cell():
    patient = GameState.root(5)
    patient.play(patient.board.cell_index(2, 0))
    assert patient.heuristic(1) == 1 / 5
