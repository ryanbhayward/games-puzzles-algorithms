import pytest

from games_puzzles_algorithms.games.ttt.game_state import GameState


def test_empty_board():
    '''Check that GameState instance is created with an empty board'''
    patient = GameState(3)
    assert(patient.score(0) is None)
    assert(patient.score(1) is None)
    assert(
        str(patient) ==
        " | | \n" +
        "-|-|-\n" +
        " | | \n" +
        "-|-|-\n" +
        " | | "
    )


def test_first_player_to_move():
    '''
    Check that the player to move is X
    '''
    patient = GameState(3)
    assert(patient.score(0) is None)
    assert(patient.score(1) is None)
    assert(patient.player_to_act() == 0)


def test_moves():
    '''
    Check that a move can be taken by specifying a row and column, and
    only empty spaces can be taken
    '''
    patient = GameState(3)
    assert(patient.score(0) is None)
    assert(patient.score(1) is None)
    assert(
        str(patient.play(patient._board._spaces.index(1, 1))) ==
        " | | \n" +
        "-|-|-\n" +
        " |X| \n" +
        "-|-|-\n" +
        " | | "
    )
    assert(patient.player_to_act() == 1)

    try: patient.play(patient._board._spaces.index(1, 1))
    except IndexError: pass
    else: raise "Should have raised IndexError"


def test_row_win():
    '''
    Check that the match is won properly on a row
    '''
    patient = GameState(3)
    assert(patient.score(0) is None)
    assert(patient.score(1) is None)
    patient.play(patient._board._spaces.index(0, 0)) \
        .play(patient._board._spaces.index(1, 0)) \
        .play(patient._board._spaces.index(0, 1)) \
        .play(patient._board._spaces.index(1, 2)) \
        .play(patient._board._spaces.index(0, 2))
    assert(patient.score(0) == 1)
    assert(patient.score(1) == -1)


def test_column_win():
    '''
    Check that the match is won properly on a column
    '''
    patient = GameState(3)
    assert(patient.score(0) is None)
    assert(patient.score(1) is None)
    patient.play(patient._board._spaces.index(0, 0)) \
        .play(patient._board._spaces.index(1, 1)) \
        .play(patient._board._spaces.index(1, 0)) \
        .play(patient._board._spaces.index(1, 2)) \
        .play(patient._board._spaces.index(2, 0))
    assert(patient.score(0) == 1)
    assert(patient.score(1) == -1)


def test_diag_1_win():
    '''
    Check that the match is won properly on first diagonal
    (bottom left to top right)
    '''
    patient = GameState(3)
    assert(patient.score(0) is None)
    assert(patient.score(1) is None)
    patient.play(patient._board._spaces.index(0, 0)) \
        .play(patient._board._spaces.index(1, 0)) \
        .play(patient._board._spaces.index(1, 1)) \
        .play(patient._board._spaces.index(1, 2)) \
        .play(patient._board._spaces.index(2, 2))
    assert(patient.score(0) == 1)
    assert(patient.score(1) == -1)


def test_draw():
    '''
    Check that the match is drawn
    '''
    patient = GameState(3)
    assert(patient.score(0) is None)
    assert(patient.score(1) is None)
    patient.play(patient._board._spaces.index(0, 0)) \
        .play(patient._board._spaces.index(1, 0)) \
        .play(patient._board._spaces.index(0, 1)) \
        .play(patient._board._spaces.index(1, 1)) \
        .play(patient._board._spaces.index(1, 2)) \
        .play(patient._board._spaces.index(0, 2)) \
        .play(patient._board._spaces.index(2, 0)) \
        .play(patient._board._spaces.index(2, 1)) \
        .play(patient._board._spaces.index(2, 2))
    assert(patient.is_terminal())
    assert(patient.score(0) == 0)


@pytest.mark.xfail
def test_empty_undo():
    '''
    Check that undoing an empty board doesn't break.
    '''
    patient = GameState(3)
    patient.undo()
    assert(patient.player_to_act() == 0)
