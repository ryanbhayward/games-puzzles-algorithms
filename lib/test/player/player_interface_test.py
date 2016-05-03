from games_puzzles_algorithms.player.rule_based.uniform_random_agent \
    import UniformRandomAgent
from games_puzzles_algorithms.player.rule_based.first_action_agent \
    import FirstActionAgent
from games_puzzles_algorithms.player.mcts.mcts_agent \
    import MctsAgent
import pytest


class MockGameState(object):
    def num_legal_actions(self):
        return 2

    def legal_actions(self):
        for a in [1, 2]:
            yield a


@pytest.mark.parametrize('player', [
    UniformRandomAgent(lambda: 0.54),
    FirstActionAgent(),
    # MctsAgent()
])
def test_act(player):
    player.act(MockGameState())
