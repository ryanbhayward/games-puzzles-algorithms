from games_puzzles_algorithms.players.rule_based.random_agent \
    import RandomAgent
from games_puzzles_algorithms.players.rule_based.first_action_agent \
    import FirstActionAgent
from games_puzzles_algorithms.players.mcts.mcts_agent import MctsAgent
from games_puzzles_algorithms.players.minimax.minimax_agent import MinimaxAgent
from games_puzzles_algorithms.players.minimax.alpha_beta_agent \
    import AlphaBetaAgent
from games_puzzles_algorithms.games.fake_game_state import FakeGameState
import pytest
import random


@pytest.mark.parametrize('player', [
    RandomAgent(lambda: 0.54),
    FirstActionAgent(),
    MctsAgent(random),
    MinimaxAgent(),
    AlphaBetaAgent()
])
def test_select_action(player):
    player.select_action(FakeGameState(), time_allowed_s=0.001)


@pytest.mark.parametrize('player', [
    RandomAgent(lambda: 0.54),
    FirstActionAgent(),
    MctsAgent(random),
    MinimaxAgent()
])
def test_reset(player):
    player.reset()
