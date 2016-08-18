from games_puzzles_algorithms.games.ttt.game_state import GameState


def test_m_x_n_board():
    patient = GameState(2, 4)
    assert(patient.score(0) is None)
    assert(patient.score(1) is None)
    assert(
        str(patient) ==
        "\n" +
        "  A B C D\n" +
        "1  | | | \n" +
        "  -|-|-|-\n" +
        "2  | | | \n"
    )


def test_k_win():
    patient = GameState(3, num_spaces_to_win=2)
    assert(patient.score(0) is None)
    assert(patient.score(1) is None)
    assert(
        str(patient) ==
        "\n" +
        "  A B C\n" +
        "1  | | \n" +
        "  -|-|-\n" +
        "2  | | \n" +
        "  -|-|-\n" +
        "3  | | \n"
    )

    patient.play(0)
    patient.play(1)
    patient.play(3)
    assert(
        str(patient) ==
        "\n" +
        "  A B C\n" +
        "1 X|X| \n" +
        "  -|-|-\n" +
        "2 O| | \n" +
        "  -|-|-\n" +
        "3  | | \n"
    )
    assert(patient.score(0) == 1)
    assert(patient.score(1) == -1)
    assert(patient.winner() == 0)


def test_empty_board():
    '''Check that GameState instance is created with an empty board'''
    patient = GameState(3)
    assert(patient.score(0) is None)
    assert(patient.score(1) is None)
    assert(
        str(patient) ==
        "\n" +
        "  A B C\n" +
        "1  | | \n" +
        "  -|-|-\n" +
        "2  | | \n" +
        "  -|-|-\n" +
        "3  | | \n"
    )

def test_large_board_representation():
    '''Check that large boards are represented clearly.'''
    patient = GameState(10)
    print(patient)
    assert(
        str(patient) ==
        "\n" +
        "   A B C D E F G H I J\n" +
        "1   | | | | | | | | | \n" +
        "   -|-|-|-|-|-|-|-|-|-\n" +
        "2   | | | | | | | | | \n" +
        "   -|-|-|-|-|-|-|-|-|-\n" +
        "3   | | | | | | | | | \n" +
        "   -|-|-|-|-|-|-|-|-|-\n" +
        "4   | | | | | | | | | \n" +
        "   -|-|-|-|-|-|-|-|-|-\n" +
        "5   | | | | | | | | | \n" +
        "   -|-|-|-|-|-|-|-|-|-\n" +
        "6   | | | | | | | | | \n" +
        "   -|-|-|-|-|-|-|-|-|-\n" +
        "7   | | | | | | | | | \n" +
        "   -|-|-|-|-|-|-|-|-|-\n" +
        "8   | | | | | | | | | \n" +
        "   -|-|-|-|-|-|-|-|-|-\n" +
        "9   | | | | | | | | | \n" +
        "   -|-|-|-|-|-|-|-|-|-\n" +
        "10  | | | | | | | | | \n"
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
        str(patient.play(patient._spaces.index(1, 1))) ==
        "\n" +
        "  A B C\n" +
        "1  | | \n" +
        "  -|-|-\n" +
        "2  |X| \n" +
        "  -|-|-\n" +
        "3  | | \n"
    )
    assert(patient.player_to_act() == 1)

    try: patient.play(patient._spaces.index(1, 1))
    except IndexError: pass
    else: raise "Should have raised IndexError"


def test_row_win():
    '''
    Check that the match is won properly on a row
    '''
    patient = GameState(3)
    assert(patient.score(0) is None)
    assert(patient.score(1) is None)
    patient.play(patient._spaces.index(0, 0)) \
        .play(patient._spaces.index(1, 0)) \
        .play(patient._spaces.index(0, 1)) \
        .play(patient._spaces.index(1, 2)) \
        .play(patient._spaces.index(0, 2))
    assert(patient.score(0) == 1)
    assert(patient.score(1) == -1)
    assert(patient.is_terminal())
    assert(patient.num_legal_actions() == 0)


def test_column_win():
    '''
    Check that the match is won properly on a column
    '''
    patient = GameState(3)
    assert(patient.score(0) is None)
    assert(patient.score(1) is None)
    patient.play(patient._spaces.index(0, 0)) \
        .play(patient._spaces.index(1, 1)) \
        .play(patient._spaces.index(1, 0)) \
        .play(patient._spaces.index(1, 2)) \
        .play(patient._spaces.index(2, 0))
    assert(patient.score(0) == 1)
    assert(patient.score(1) == -1)
    assert(patient.is_terminal())
    assert(patient.num_legal_actions() == 0)


def test_diag_1_win():
    '''
    Check that the match is won properly on first diagonal
    (bottom left to top right)
    '''
    patient = GameState(3)
    assert(patient.score(0) is None)
    assert(patient.score(1) is None)
    patient.play(patient._spaces.index(0, 0)) \
        .play(patient._spaces.index(1, 0)) \
        .play(patient._spaces.index(1, 1)) \
        .play(patient._spaces.index(1, 2)) \
        .play(patient._spaces.index(2, 2))
    assert(patient.score(0) == 1)
    assert(patient.score(1) == -1)
    assert(patient.is_terminal())
    assert(patient.num_legal_actions() == 0)


def test_draw():
    '''
    Check that the match is drawn
    '''
    patient = GameState(3)
    assert(patient.score(0) is None)
    assert(patient.score(1) is None)
    patient.play(patient._spaces.index(0, 0)) \
        .play(patient._spaces.index(1, 0)) \
        .play(patient._spaces.index(0, 1)) \
        .play(patient._spaces.index(1, 1)) \
        .play(patient._spaces.index(1, 2)) \
        .play(patient._spaces.index(0, 2)) \
        .play(patient._spaces.index(2, 0)) \
        .play(patient._spaces.index(2, 1)) \
        .play(patient._spaces.index(2, 2))
    assert(patient.is_terminal())
    assert(patient.score(0) == 0)
    assert(patient.is_terminal())
    assert(patient.num_legal_actions() == 0)


def test_empty_undo():
    '''
    Check that undoing an empty board doesn't break.
    '''
    patient = GameState(3)
    patient.undo()
    assert(patient.player_to_act() == 0)


def test_winner_after_undo():
    '''
    Check that undoing a move after a win no longer results in a win.
    '''
    patient = GameState(3)
    assert(patient.score(0) is None)
    assert(patient.score(1) is None)
    patient.play(patient._spaces.index(0, 0)) \
        .play(patient._spaces.index(1, 0)) \
        .play(patient._spaces.index(1, 1)) \
        .play(patient._spaces.index(1, 2)) \
        .play(patient._spaces.index(2, 2))
    assert(patient.score(0) == 1)
    assert(patient.score(1) == -1)
    assert(patient.is_terminal())
    assert(patient.num_legal_actions() == 0)
    patient.undo()
    assert(patient.score(0) is None)
    assert(patient.score(1) is None)
    assert(not patient.is_terminal())
    assert(patient.num_legal_actions() == 5)
