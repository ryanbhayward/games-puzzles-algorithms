import pytest

from games_puzzles_algorithms.games.hex.color import IllegalAction
from games_puzzles_algorithms.games.hex.game_state import GameState


@pytest.mark.xfail
def test_hex_board_prints():
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


@pytest.mark.xfail
def test_hex_move_made_twice():
    patient = GameState.root(5)
    patient.play(patient.board.cell_index(0, 0))

    with pytest.raises(IllegalAction):
        patient.play(patient.board.cell_index(0, 0))
