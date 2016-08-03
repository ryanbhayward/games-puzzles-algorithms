from games_puzzles_algorithms.players.mcts.mcts_rave_agent import RaveAgent, RaveNode
from mcts_test import SimpleGameState
import pytest
import random

class SimpleRaveGameState(SimpleGameState):
    
    def rave_moves(self):
        if self._player_to_act == 0:
            return {0: [self._actions[1]],
                    1: [self.actions[0], self.actions[2]]}
        else:
            return {0: [self._actions[0], self._actions[2]],
                    1: [self._actions[1]]}


def test_roll_out():
    random.seed(0)

    state = SimpleRaveGameState()
    patient = RaveAgent(exploration=1)
    outcome = patient.roll_out(state, 0)
    assert outcome['score'] == 2
    assert len(outcome['rave_moves'][0]) == 2
    outcome = patient.roll_out(state, 0)
    assert outcome['score'] == -3
    outcome = patient.roll_out(state, 0)
    assert outcome['score'] == -3
    outcome = patient.roll_out(state, 1)
    assert outcome['score'] == -2
    outcome = patient.roll_out(state, 1)
    assert outcome['score'] == 3
    outcome = patient.roll_out(state, 1)
    assert outcome['score'] == 3
    outcome = patient.roll_out(state, 1)
    assert outcome['score'] == -2    

def test_search():
    random.seed(0)
    
    state = SimpleRaveGameState()
    patient = RaveAgent(exploration=1)
    num_iterations = 10
    stats = patient.search(state, num_iterations=num_iterations)

    assert stats['num_iterations_completed'] == 10
    assert stats['time_used_s'] is not None
    assert stats['num_nodes_expanded'] == 11    