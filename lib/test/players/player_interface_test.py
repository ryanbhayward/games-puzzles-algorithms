from games_puzzles_algorithms.players.rule_based.uniform_random_agent \
    import UniformRandomAgent
from games_puzzles_algorithms.players.rule_based.first_action_agent \
    import FirstActionAgent
from games_puzzles_algorithms.players.mcts.mcts_agent import MctsAgent
from games_puzzles_algorithms.players.minimax.minimax_agent import MinimaxAgent
from games_puzzles_algorithms.players.mimimax.alpha_beta_agent \
    import AlphaBetaAgent
from games_puzzles_algorithms.games.fake_game_state import FakeGameState
import pytest


@pytest.mark.parametrize('player', [
    UniformRandomAgent(lambda: 0.54),
    FirstActionAgent(),
    MctsAgent(num_iterations=0),
    MinimaxAgent(),
    AlphaBetaAgent()
])
def test_select_action(player):
    player.select_action(FakeGameState(), time_available=0.001)


@pytest.mark.parametrize('player', [
    UniformRandomAgent(lambda: 0.54),
    FirstActionAgent(),
    MctsAgent()
])
def test_reset(player):
    player.reset()
