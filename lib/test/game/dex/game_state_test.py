from games_puzzles_algorithms.game.dex.game_state import color_to_player
from games_puzzles_algorithms.game.dex.game_state import COLORS
from games_puzzles_algorithms.game.dex.game_state import GameState
from games_puzzles_algorithms.game.dex.game_state import IllegalAction
import pytest
import random
from games_puzzles_algorithms.choose import choose_legal_action_uniformly_randomly


def test_white_win1():
    patient = GameState.root(5)
    patient.place((1, 0), COLORS['white'])
    patient.place((1, 1), COLORS['white'])
    patient.place((1, 2), COLORS['white'])
    patient.place((1, 3), COLORS['white'])

    assert patient.to_s(color_to_player(COLORS['white'])) == (
'''
  A  B  C  D  E
1  .  .  .  .  .  O
 2  O  O  O  O  .  O
  3  .  .  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
    )

    patient.place((1, 4), COLORS['white'])

    assert patient.to_s(color_to_player(COLORS['white'])) == (
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
    patient.place((1, 0), COLORS['white'])
    patient.place((1, 1), COLORS['white'])
    patient.place((1, 2), COLORS['white'])
    patient.place((1, 3), COLORS['white'])

    assert patient.to_s(color_to_player(COLORS['white'])) == (
'''
  A  B  C  D  E
1  .  .  .  .  .  O
 2  O  O  O  O  .  O
  3  .  .  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
    )

    patient.place((0, 4), COLORS['white'])

    assert patient.to_s(color_to_player(COLORS['white'])) == (
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
    patient.place((1, 1), COLORS['white'])
    patient.place((0, 1), COLORS['black'])
    patient.place((0, 1), COLORS['white'])

    assert patient.to_s(color_to_player(COLORS['white'])) == (
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
    for cell in patient.board.every_legal_neighbor(color_to_player(COLORS['white']), 1, 1):
        patient.place(cell, COLORS['white'])
        count += 1

    assert count == num_neighbors

    assert patient.to_s(color_to_player(COLORS['white'])) == (
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
    patient.place((1, 1), COLORS['white'])

    assert patient.to_s(color_to_player(COLORS['white'])) == (
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
    for cell in patient.board.every_legal_neighbor(color_to_player(COLORS['white']), 1, 1):
        patient.place(cell, COLORS['white'])
        count += 1

    assert count == num_neighbors

    assert patient.to_s(color_to_player(COLORS['white'])) == (
'''
  A  B  C  D  E
1  .  O  O  .  .  O
 2  O  O  O  .  .  O
  3  O  O  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
    )


def test_potentially_winning_moves2():
    patient = GameState.root(5)
    patient.place((1, 0), COLORS['white'])
    patient.place((1, 1), COLORS['white'])
    patient.place((1, 4), COLORS['white'])
    patient.place((1, 3), COLORS['white'])

    assert patient.to_s(color_to_player(COLORS['white'])) == (
'''
  A  B  C  D  E
1  .  .  .  .  .  O
 2  O  O  .  O  O  O
  3  .  .  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
    )

    patient.set_turn(color_to_player(COLORS['white']))
    moves = patient.potentially_winning_moves()
    assert moves == [patient.board.cell_index(1, 2)]


def test_potentially_winning_moves1():
    patient = GameState.root(5)
    patient.place((1, 0), COLORS['white'])
    patient.place((1, 1), COLORS['white'])
    patient.place((1, 2), COLORS['white'])
    patient.place((1, 3), COLORS['white'])

    assert patient.to_s(color_to_player(COLORS['white'])) == (
'''
  A  B  C  D  E
1  .  .  .  .  .  O
 2  O  O  O  O  .  O
  3  .  .  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
    )

    patient.set_turn(color_to_player(COLORS['white']))
    moves = patient.potentially_winning_moves()
    assert moves == [patient.board.cell_index(0, 4), patient.board.cell_index(1, 4)]


def test_set_colorless():
    patient = GameState.root(5)
    patient.place((0, 0), COLORS['white'])

    with pytest.raises(IndexError):
        patient.place((0, 0), COLORS['none'])
    assert patient.to_s(color_to_player(COLORS['white'])) == (
'''
  A  B  C  D  E
1  O  .  .  .  .  O
 2  .  .  .  .  .  O
  3  .  .  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
    )


def test_with_stone_at_index():
    patient = GameState.root(5)
    assert patient.actor == color_to_player(COLORS['white'])
    for _ in patient.with_stone_at_index(0):
        assert patient.actor == color_to_player(COLORS['white'])
        assert patient.to_s(color_to_player(COLORS['white'])) == (
'''
  A  B  C  D  E
1  O  .  .  .  .  O
 2  .  .  .  .  .  O
  3  .  .  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
        )
    assert patient.actor == color_to_player(COLORS['white'])
    assert patient.to_s(color_to_player(COLORS['white'])) == (
'''
  A  B  C  D  E
1  .  .  .  .  .  O
 2  .  .  .  .  .  O
  3  .  .  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
        )


def test_with_stone_at_cell():
    patient = GameState.root(5)
    assert patient.actor == color_to_player(COLORS['white'])
    for _ in patient.with_stone_at_cell((0, 1)):
        assert patient.actor == color_to_player(COLORS['white'])
        assert patient.to_s(color_to_player(COLORS['white'])) == (
'''
  A  B  C  D  E
1  .  O  .  .  .  O
 2  .  .  .  .  .  O
  3  .  .  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
        )
    assert patient.actor == color_to_player(COLORS['white'])
    assert patient.to_s(color_to_player(COLORS['white'])) == (
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
    patient.place((0, 0), COLORS['white'])
    patient.place((1, 1), COLORS['white'])
    patient.place((0, 1), COLORS['black'])
    patient.place((0, 0), COLORS['black'])
    patient.place((1, 1), COLORS['black'])
    patient.place((1, 0), COLORS['black'])

    assert patient.winner() == COLORS['black']


def test_white_moves_are_hidden_from_black():
    patient = GameState.root(5)
    cell = (0, 0)
    patient.place(cell, COLORS['white'])
    patient.set_turn(color_to_player(COLORS['white']))
    assert patient.turn() == color_to_player(COLORS['white'])
    assert patient[cell] == COLORS['white']

    patient.set_turn(color_to_player(COLORS['black']))
    assert patient.turn() == color_to_player(COLORS['black'])
    assert patient[cell] == COLORS['none']

    assert patient.to_s(color_to_player(COLORS['white'])) == (
'''
  A  B  C  D  E
1  O  .  .  .  .  O
 2  .  .  .  .  .  O
  3  .  .  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
    )
    assert patient.to_s(color_to_player(COLORS['black'])) == (
'''
  A  B  C  D  E
1  .  .  .  .  .  O
 2  .  .  .  .  .  O
  3  .  .  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
    )


def test_white_moves_are_revealed_to_black_after_a_collision():
    patient = GameState.root(5)
    cell = (0, 0)

    patient.place(cell, COLORS['white'])

    patient.set_turn(color_to_player(COLORS['white']))
    assert patient.turn() == color_to_player(COLORS['white'])
    assert patient[cell] == COLORS['white']

    patient.set_turn(color_to_player(COLORS['black']))
    assert patient.turn() == color_to_player(COLORS['black'])
    assert patient[cell] == COLORS['none']

    patient.place(cell, COLORS['black'])
    assert patient[cell] == COLORS['white']

    assert patient.to_s(color_to_player(COLORS['white'])) == (
'''
  A  B  C  D  E
1  O  .  .  .  .  O
 2  .  .  .  .  .  O
  3  .  .  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
    )
    assert patient.to_s(color_to_player(COLORS['black'])) == (
'''
  A  B  C  D  E
1  O  .  .  .  .  O
 2  .  .  .  .  .  O
  3  .  .  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
    )


def test_black_moves_are_hidden_from_white():
    patient = GameState.root(5)
    cell = (0, 0)
    patient.place(cell, COLORS['black'])
    patient.set_turn(color_to_player(COLORS['black']))
    assert patient.turn() == color_to_player(COLORS['black'])
    assert patient[cell] == COLORS['black']

    patient.set_turn(color_to_player(COLORS['white']))
    assert patient.turn() == color_to_player(COLORS['white'])
    assert patient[cell] == COLORS['none']

    assert patient.to_s(color_to_player(COLORS['white'])) == (
'''
  A  B  C  D  E
1  .  .  .  .  .  O
 2  .  .  .  .  .  O
  3  .  .  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
    )
    assert patient.to_s(color_to_player(COLORS['black'])) == (
'''
  A  B  C  D  E
1  @  .  .  .  .  O
 2  .  .  .  .  .  O
  3  .  .  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
    )


def test_black_moves_are_revealed_to_white_after_a_collision():
    patient = GameState.root(5)
    cell = (0, 0)

    patient.place(cell, COLORS['black'])

    patient.set_turn(color_to_player(COLORS['black']))
    assert patient.turn() == color_to_player(COLORS['black'])
    assert patient[cell] == COLORS['black']

    patient.set_turn(color_to_player(COLORS['white']))
    assert patient.turn() == color_to_player(COLORS['white'])
    assert patient[cell] == COLORS['none']

    patient.place(cell, COLORS['white'])

    assert patient[cell] == COLORS['black']

    assert patient.to_s(color_to_player(COLORS['white'])) == (
'''
  A  B  C  D  E
1  @  .  .  .  .  O
 2  .  .  .  .  .  O
  3  .  .  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
    )
    assert patient.to_s(color_to_player(COLORS['black'])) == (
'''
  A  B  C  D  E
1  @  .  .  .  .  O
 2  .  .  .  .  .  O
  3  .  .  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
    )


def test_undo_after_a_collision():
    patient = GameState.root(5)
    cell = (0, 0)

    patient.place(cell, COLORS['black'])

    patient.set_turn(color_to_player(COLORS['black']))
    assert patient.turn() == color_to_player(COLORS['black'])
    assert patient[cell] == COLORS['black']

    patient.set_turn(color_to_player(COLORS['white']))
    assert patient.turn() == color_to_player(COLORS['white'])
    assert patient[cell] == COLORS['none']

    patient.place(cell, COLORS['white'])

    assert patient[cell] == COLORS['black']

    assert patient.to_s(color_to_player(COLORS['white'])) == (
'''
  A  B  C  D  E
1  @  .  .  .  .  O
 2  .  .  .  .  .  O
  3  .  .  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
    )
    assert patient.to_s(color_to_player(COLORS['black'])) == (
'''
  A  B  C  D  E
1  @  .  .  .  .  O
 2  .  .  .  .  .  O
  3  .  .  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
    )

    assert patient.turn() == color_to_player(COLORS['white'])
    patient.undo()
    assert patient.turn() == color_to_player(COLORS['white'])
    assert patient[cell] == COLORS['none']

    patient.set_turn(color_to_player(COLORS['black']))
    assert patient.turn() == color_to_player(COLORS['black'])
    assert patient[cell] == COLORS['black']

    patient.set_turn(color_to_player(COLORS['white']))
    assert patient.turn() == color_to_player(COLORS['white'])

    patient.undo()
    assert patient.turn() == color_to_player(COLORS['black'])
    assert patient[cell] == COLORS['none']


def test_terminal_black():
    patient = GameState.root(5)
    assert patient.winner() == COLORS['none']
    patient.place((0, 0), COLORS['black'])
    assert patient.winner() == COLORS['none']
    patient.place((1, 0), COLORS['black'])
    assert patient.winner() == COLORS['none']
    patient.place((2, 0), COLORS['black'])
    assert patient.winner() == COLORS['none']
    patient.place((3, 0), COLORS['black'])
    assert patient.winner() == COLORS['none']
    patient.place((4, 0), COLORS['black'])
    assert patient.winner() == COLORS['black']


def test_terminal_black():
    patient = GameState.root(5)
    assert patient.winner() == COLORS['none']
    patient.place((0, 0), COLORS['black'])
    assert patient.winner() == COLORS['none']
    patient.place((1, 0), COLORS['black'])
    assert patient.winner() == COLORS['none']
    patient.place((2, 0), COLORS['black'])
    assert patient.winner() == COLORS['none']
    patient.place((3, 0), COLORS['black'])
    assert patient.winner() == COLORS['none']
    patient.place((4, 0), COLORS['black'])
    assert patient.winner() == COLORS['black']

    patient.set_turn(color_to_player(COLORS['white']))
    patient.undo()
    assert patient.winner() == COLORS['none']


def test_terminal_white():
    patient = GameState.root(5)
    assert patient.winner() == COLORS['none']
    patient.place((0, 0), COLORS['white'])
    assert patient.winner() == COLORS['none']
    patient.place((0, 1), COLORS['white'])
    assert patient.winner() == COLORS['none']
    patient.place((0, 2), COLORS['white'])
    assert patient.winner() == COLORS['none']
    patient.place((0, 3), COLORS['white'])
    assert patient.winner() == COLORS['none']
    patient.place((0, 4), COLORS['white'])
    assert patient.winner() == COLORS['white']
