from games_puzzles_algorithms.players.rule_based.uniform_random_agent \
    import UniformRandomAgent
from games_puzzles_algorithms.players.rule_based.first_action_agent \
    import FirstActionAgent
from games_puzzles_algorithms.players.mcts.mcts_agent import MctsAgent
from games_puzzles_algorithms.games.fake_game_state import FakeGameState
import pytest


@pytest.mark.parametrize('player', [
    UniformRandomAgent(lambda: 0.54),
    FirstActionAgent(),
    MctsAgent(num_iterations=0)
])
def test_select_action(player):
    player.select_action(FakeGameState())


@pytest.mark.parametrize('player', [
    UniformRandomAgent(lambda: 0.54),
    FirstActionAgent(),
    MctsAgent()
])
def test_reset(player):
    player.reset()
