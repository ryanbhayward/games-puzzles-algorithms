from games_puzzles_algorithms.players.mcts.mcts_agent import MctsAgent, UctNode
from games_puzzles_algorithms.games.hex.game_state import GameState
import random


def test_select_action():
    random.seed(0)
    state = GameState.root()
    patient = MctsAgent(random, UctNode(1))
    action = patient.select_action(state, num_iterations=10)
    state.play(action)
    assert patient.select_action(state, num_iterations=10) != action
