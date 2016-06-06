import pytest
import random
from games_puzzles_algorithms.games.hex.game_state import color_to_player
from games_puzzles_algorithms.games.hex.game_state import COLORS
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
    patient.place(patient.board.cell_index(1, 0), COLORS['white'])
    patient.place(patient.board.cell_index(1, 1), COLORS['white'])
    patient.place(patient.board.cell_index(1, 2), COLORS['white'])
    patient.place(patient.board.cell_index(1, 3), COLORS['white'])

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

    patient.place(patient.board.cell_index(1, 4), COLORS['white'])

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

    assert patient.winner() == COLORS['white']


def test_white_win2():
    patient = GameState.root(5)
    patient.place(patient.board.cell_index(1, 0), COLORS['white'])
    patient.place(patient.board.cell_index(1, 1), COLORS['white'])
    patient.place(patient.board.cell_index(1, 2), COLORS['white'])
    patient.place(patient.board.cell_index(1, 3), COLORS['white'])

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

    patient.place(patient.board.cell_index(0, 4), COLORS['white'])

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

    assert patient.winner() == COLORS['white']


def test_legal_neighbors():
    patient = GameState.root(5)
    patient.place(patient.board.cell_index(1, 1), COLORS['white'])
    patient.place(patient.board.cell_index(0, 1), COLORS['black'])

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
        patient.place(patient.board.cell_index(*cell), COLORS['white'])
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
    patient.place(patient.board.cell_index(1, 1), COLORS['white'])

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
        patient.place(patient.board.cell_index(*cell), COLORS['white'])
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
    patient.place(patient.board.cell_index(0, 0), COLORS['white'])

    with pytest.raises(IllegalAction):
        patient.place(patient.board.cell_index(0, 0), COLORS['none'])
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
        patient.place(patient.board.cell_index(0, 0), COLORS['none'])
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
    assert patient.player_to_act() == color_to_player(COLORS['white'])
    for _ in patient.with_action_applied(0):
        assert patient.player_to_act() == color_to_player(COLORS['white'])
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
    assert patient.player_to_act() == color_to_player(COLORS['white'])
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
    patient.place(patient.board.cell_index(0, 0), COLORS['white'])
    patient.place(patient.board.cell_index(1, 1), COLORS['white'])
    patient.place(patient.board.cell_index(0, 1), COLORS['black'])
    patient.place(patient.board.cell_index(1, 0), COLORS['black'])

    assert patient.winner() == COLORS['black']


def test_white_moves_are_not_hidden_from_black():
    patient = GameState.root(5)
    cell = (0, 0)
    patient.place(patient.board.cell_index(*cell), COLORS['white'])
    patient.set_player_to_act(color_to_player(COLORS['white']))
    assert patient.player_to_act() == color_to_player(COLORS['white'])
    assert patient[cell] == COLORS['white']

    patient.set_player_to_act(color_to_player(COLORS['black']))
    assert patient.player_to_act() == color_to_player(COLORS['black'])
    assert patient[cell] == COLORS['white']

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
    patient.place(patient.board.cell_index(*cell), COLORS['black'])
    patient.set_player_to_act(color_to_player(COLORS['black']))
    assert patient.player_to_act() == color_to_player(COLORS['black'])
    assert patient[cell] == COLORS['black']

    patient.set_player_to_act(color_to_player(COLORS['white']))
    assert patient.player_to_act() == color_to_player(COLORS['white'])
    assert patient[cell] == COLORS['black']

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
    assert patient.winner() == COLORS['none']
    patient.place(patient.board.cell_index(0, 0), COLORS['black'])
    assert patient.winner() == COLORS['none']
    patient.place(patient.board.cell_index(1, 0), COLORS['black'])
    assert patient.winner() == COLORS['none']
    patient.place(patient.board.cell_index(2, 0), COLORS['black'])
    assert patient.winner() == COLORS['none']
    patient.place(patient.board.cell_index(3, 0), COLORS['black'])
    assert patient.winner() == COLORS['none']
    patient.place(patient.board.cell_index(4, 0), COLORS['black'])
    assert patient.winner() == COLORS['black']


def test_terminal_black():
    patient = GameState.root(5)
    assert patient.winner() == COLORS['none']
    patient.place(patient.board.cell_index(0, 0), COLORS['black'])
    assert patient.winner() == COLORS['none']
    patient.place(patient.board.cell_index(1, 0), COLORS['black'])
    assert patient.winner() == COLORS['none']
    patient.place(patient.board.cell_index(2, 0), COLORS['black'])
    assert patient.winner() == COLORS['none']
    patient.place(patient.board.cell_index(3, 0), COLORS['black'])
    assert patient.winner() == COLORS['none']
    patient.place(patient.board.cell_index(4, 0), COLORS['black'])
    assert patient.winner() == COLORS['black']

    patient.set_player_to_act(color_to_player(COLORS['white']))
    patient.undo()
    assert patient.winner() == COLORS['none']


def test_terminal_white():
    patient = GameState.root(5)
    assert patient.winner() == COLORS['none']
    patient.place(patient.board.cell_index(0, 0), COLORS['white'])
    assert patient.winner() == COLORS['none']
    patient.place(patient.board.cell_index(0, 1), COLORS['white'])
    assert patient.winner() == COLORS['none']
    patient.place(patient.board.cell_index(0, 2), COLORS['white'])
    assert patient.winner() == COLORS['none']
    patient.place(patient.board.cell_index(0, 3), COLORS['white'])
    assert patient.winner() == COLORS['none']
    patient.place(patient.board.cell_index(0, 4), COLORS['white'])
    assert patient.winner() == COLORS['white']


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
