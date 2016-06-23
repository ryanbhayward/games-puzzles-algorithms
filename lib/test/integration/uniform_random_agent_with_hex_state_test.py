from games_puzzles_algorithms.players.rule_based.uniform_random_agent \
    import UniformRandomAgent
from games_puzzles_algorithms.games.hex.game_state import GameState
from games_puzzles_algorithms.games.hex.color import \
    COLORS, color_to_player, cell_str, cell_str_to_cell
import random


def test_on_empty():
    random_generator = random.Random(290134)
    state = GameState.root(5)
    patient = UniformRandomAgent(lambda: random_generator.uniform(0, 1))

    action = patient.select_action(state)
    cell = (state.board.row(action), state.board.column(action))
    assert cell == (1, 4)
    assert cell_str(cell) == 'e2'
    assert cell == cell_str_to_cell('e2')
    state.play(action)

    assert str(state) == (
'''
  A  B  C  D  E
1  .  .  .  .  .  O
 2  .  .  .  .  O  O
  3  .  .  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
    )
