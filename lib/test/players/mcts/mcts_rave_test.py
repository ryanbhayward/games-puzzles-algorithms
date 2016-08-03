from games_puzzles_algorithms.players.mcts.mcts_rave_agent \
    import RaveAgent, RaveNode
from games_puzzles_algorithms.players.mcts.mcts_agent import UctNode
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


def test_initial_lcb():
    root = RaveNode()
    with pytest.raises(UctNode.RootNodeError):
        root.lcb() 


def test_backup_with_lcb():
    rave_moves = {0: [0]}
    root = RaveNode()
    state = SimpleRaveGameState()
    root.expand(state)
    children = root.child_nodes()
    children[0].expand(state)
    children[0].child_nodes()[0].backup(1, rave_moves)
    with pytest.raises(UctNode.RootNodeError):
        root.lcb()
    assert children[0].lcb() == -1
    assert children[1].lcb() == 0
    assert children[0].child_nodes()[0].lcb() == 1
    assert children[0].child_nodes()[1].lcb() == 0
    children[0].child_nodes()[1].backup(-1, rave_moves)
    assert children[0].lcb() == 0
    #assert children[0].child_nodes()[0].lcb() == 1
    assert children[0].child_nodes()[1].lcb() == -1
    
def test_backup_with_value():
    root = RaveNode()
    state = SimpleRaveGameState()
    root.expand(state)
    children = root.child_nodes()
    children[0].expand(state)
    children[0].child_nodes()[0].backup(1, state.rave_moves())
    with pytest.raises(UctNode.RootNodeError):
        root.value()
    assert children[0].value() == -1
    assert children[1].value() == 0
    assert children[0].child_nodes()[0].value() == 1
    assert children[0].child_nodes()[1].value() == 0
    children[0].child_nodes()[1].backup(-1, state.rave_moves)
    assert children[0].value() == 0
    assert children[0].child_nodes()[0].value() == 1
    assert children[0].child_nodes()[1].value() == -1
    

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