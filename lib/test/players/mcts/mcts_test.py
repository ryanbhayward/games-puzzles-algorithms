from games_puzzles_algorithms.players.mcts.mcts_agent import MctsAgent, UctNode
from games_puzzles_algorithms.games.fake_game_state import FakeGameState
from games_puzzles_algorithms.debug import log
import logging
import pytest
import random


class SimpleGameState(FakeGameState):
    def __init__(self):
        self._player_to_act = 0
        self._actions = []

    def num_legal_actions(self):
        return 2

    def legal_actions(self):
        for a in range(2):
            yield a

    def play(self, action):
        '''Apply the given action.

        `action` must be in the set of legal actions
        (see `legal_actions`).
        Return `self`.
        '''
        self._actions.append(action)
        self.set_player_to_act(int(not self._player_to_act))
        return self

    def __enter__(self):
        '''Allows the following type of code:

        ```
        with state.play(action):
            # Do something with `state` after `action`
            # has been applied to `state`.
        # `action` has automatically be undone.
        '''
        pass

    def __exit__(self,
                 exception_type,
                 exception_val,
                 exception_traceback):
        '''Allows the following type of code:

        ```
        with state.play(action):
            # Do something with `state` after `action`
            # has been applied to `state`.
        # `action` has automatically be undone.
        '''
        self.undo()

    def undo(self):
        '''Reverse the effect of the last action that was played'''
        self._actions.pop()
        self.set_player_to_act(int(not self._player_to_act))

    def set_player_to_act(self, player):
        self._player_to_act = player

    def player_to_act(self):
        return self._player_to_act

    def is_terminal(self):
        return len(self._actions) == 3

    def score(self, player):
        if not self.is_terminal():
            return None
        if self._actions[0] == 0:
            if self._actions[1] == 0:
                return [2, -2][player]
            else:
                return [-3, 3][player]
        else:
            if self._actions[1] == 0:
                return [-3, 3][player]
            else:
                return [2, -2][player]


def test_roll_out():
    random.seed(0)

    state = SimpleGameState()
    patient = MctsAgent(exploration=1)
    outcome = patient.roll_out(state, 0)
    assert outcome['score'] == 2
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

    state = SimpleGameState()
    patient = MctsAgent(exploration=1)
    num_iterations = 10
    stats = patient.search(state, num_iterations=num_iterations)

    assert stats['num_iterations_completed'] == 10
    assert stats['time_used_s'] is not None
    assert stats['num_nodes_expanded'] == 11


def test_child_nodes():
    root = UctNode()
    assert root.child_nodes() == []
    
def test_expand():
    root = UctNode()
    state = SimpleGameState()
    root.expand(state)
    children = root.child_nodes()
    assert len(children) == 2
    assert children[0].action == 0
    assert children[1].action == 1
    assert children[0].parent == root
    assert children[1].parent == root
    
def test_is_leaf():
    root = UctNode()
    assert root.is_leaf()
    state = SimpleGameState()
    root.expand(state)
    assert not root.is_leaf()
    
def test_is_root():
    root = UctNode()
    state = SimpleGameState()
    root.expand(state)
    assert root.is_root()
    for child in root.child_nodes():
        assert not child.is_root()
        

def test_num_children():
    root = UctNode()
    state = SimpleGameState()
    root.expand(state)
    assert root.num_children() == 2
    for child in root.child_nodes():
        assert child.num_children() == 0

     
def test_num_nodes():
    root = UctNode()
    state = SimpleGameState()
    root.expand(state)
    assert root.num_nodes() == 3
    for child in root.child_nodes():
        assert child.num_nodes() == 1
        
        
def test_initial_lcb():
    root = UctNode()
    with pytest.raises(UctNode.RootNodeError):
        root.lcb() 
    
    
def test_initial_ucb():
    root = UctNode()
    with pytest.raises(UctNode.RootNodeError):
        root.ucb()

    
def test_ucb_initial_explore():
    root = UctNode()
    state = SimpleGameState()
    root.expand(state)
    children = root.child_nodes()
    for child in children:
        assert child.ucb(1) == float('inf')
        
    with pytest.raises(UctNode.RootNodeError):
        root.ucb(1)
    
def test_backup_with_lcb():
    root = UctNode()
    state = SimpleGameState()
    root.expand(state)
    children = root.child_nodes()
    children[0].expand(state)
    children[0].child_nodes()[0].backup(1)
    with pytest.raises(UctNode.RootNodeError):
        root.lcb()
    assert children[0].lcb() == -1
    assert children[1].lcb() == 0
    assert children[0].child_nodes()[0].lcb() == 1
    assert children[0].child_nodes()[1].lcb() == 0
    children[0].child_nodes()[1].backup(-1)
    assert children[0].lcb() == 0
    assert children[0].child_nodes()[0].lcb() == 1
    assert children[0].child_nodes()[1].lcb() == -1    
    
def test_backup_with_ucb():
    root = UctNode()
    state = SimpleGameState()
    root.expand(state)
    children = root.child_nodes()
    children[0].expand(state)
    children[0].child_nodes()[0].backup(1)
    with pytest.raises(UctNode.RootNodeError):
        root.ucb()
    assert children[0].ucb() == -1
    assert children[1].ucb() == 0
    assert children[0].child_nodes()[0].ucb() == 1
    assert children[0].child_nodes()[1].ucb() == 0
    children[0].child_nodes()[1].backup(-1)
    assert children[0].ucb() == 0
    assert children[0].child_nodes()[0].ucb() == 1
    assert children[0].child_nodes()[1].ucb() == -1       
    
def test_backup_with_value():
    root = UctNode()
    state = SimpleGameState()
    root.expand(state)
    children = root.child_nodes()
    children[0].expand(state)
    children[0].child_nodes()[0].backup(1)
    with pytest.raises(UctNode.RootNodeError):
        root.value()
    assert children[0].value() == -1
    assert children[1].value() == 0
    assert children[0].child_nodes()[0].value() == 1
    assert children[0].child_nodes()[1].value() == 0
    children[0].child_nodes()[1].backup(-1)
    assert children[0].value() == 0
    assert children[0].child_nodes()[0].value() == 1
    assert children[0].child_nodes()[1].value() == -1       
    
def test_backup_with_ucb_explore():
    root = UctNode()
    state = SimpleGameState()
    root.expand(state)
    children = root.child_nodes()
    children[0].expand(state)
    children[0].child_nodes()[0].backup(1)
    with pytest.raises(UctNode.RootNodeError):
        root.ucb()
    assert children[0].ucb(1) == -1
    assert children[1].ucb(1) == float("inf")
    assert children[0].child_nodes()[0].ucb(1) == 1
    assert children[0].child_nodes()[1].ucb(1) == float("inf")
    children[0].child_nodes()[1].backup(-1)
    assert children[0].ucb(1) > 0
    assert children[0].child_nodes()[0].ucb(1) > 1
    assert children[0].child_nodes()[1].ucb(1) > -1    
    
def test_favorite_child():
    root = UctNode()
    state = SimpleGameState()
    root.expand(state)
    children = root.child_nodes()
    children[0].backup(1)
    children[1].backup(-1)
    favorite = root.favorite_child()
    for child in children:
        assert child.value() <= favorite.value()
        
def test_info_strings_to_json():
    root = UctNode()
    state = SimpleGameState()
    root.expand(state)
    children = root.child_nodes()
    children[0].backup(1)
    children[1].backup(-1)
    info = root.info_strings_to_json()
    assert info["info"] == "P: 0 | Q: 0 N: 2"
    assert info["children"][0]["info"] == "A: 0 | Q: 1 N: 1"
    assert info["children"][1]["info"] == "A: 1 | Q: -1 N: 1"
    
def test_str():
    root = UctNode()
    state = SimpleGameState()
    assert str(root) == '{\n    "info": "| Q: 0 N: 0"\n}'

# def test_verbose_search():
#     logging.basicConfig(level=logging.DEBUG)
#
#     random.seed(0)
#
#     state = SimpleGameState()
#     patient = MctsAgent.Mcts(exploration=1)
#     num_iterations = 10
#     stats = patient.search(state, num_iterations=num_iterations)
#
#     assert stats['num_iterations_completed'] == 10
#     assert stats['time_used_s'] is not None
#     assert stats['num_nodes_expanded'] == 11
