from games_puzzles_algorithms.players.minimax.minimax_agent import MinimaxAgent
from games_puzzles_algorithms.players.minimax.alpha_beta_agent \
    import AlphaBetaAgent
from games_puzzles_algorithms.games.hex.game_state import GameState
import pytest


@pytest.mark.parametrize('player', [
    MinimaxAgent(),
    AlphaBetaAgent()
])
def test_one_by_one(player):
    state = GameState.root(1)
    assert str(state) == (
'''
  A
1  .  O
    @''')

    assert player.value(state) == 1


@pytest.mark.parametrize('player', [
    MinimaxAgent(),
    AlphaBetaAgent()
])
def test_one_by_one_action(player):
    state = GameState.root(1)
    assert str(state) == (
'''
  A
1  .  O
    @''')

    assert player.select_action(state) == 0


@pytest.mark.parametrize('player', [
    MinimaxAgent(),
    AlphaBetaAgent()
])
def test_two_by_two(player):
    state = GameState.root(2)
    assert str(state) == (
'''
  A  B
1  .  .  O
 2  .  .  O
     @  @''')

    assert player.value(state) == 1

    state.play(0)
    assert str(state) == (
'''
  A  B
1  O  .  O
 2  .  .  O
     @  @''')

    assert player.value(state) == 1

    state.undo()
    state.play(1)
    assert str(state) == (
'''
  A  B
1  .  .  O
 2  O  .  O
     @  @''')

    assert player.value(state) == -1


@pytest.mark.parametrize('player', [
    MinimaxAgent(),
    AlphaBetaAgent()
])
def test_two_by_two_action(player):
    state = GameState.root(2)
    assert str(state) == (
'''
  A  B
1  .  .  O
 2  .  .  O
     @  @''')

    assert player.select_action(state) == 1

    state.play(0)
    assert str(state) == (
'''
  A  B
1  O  .  O
 2  .  .  O
     @  @''')

    assert player.select_action(state) == 2

    state.undo()
    state.play(1)
    assert str(state) == (
'''
  A  B
1  .  .  O
 2  O  .  O
     @  @''')

    assert player.select_action(state) == 0
