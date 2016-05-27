from games_puzzles_algorithms.players.mcts.mcts_agent import MctsAgent
from games_puzzles_algorithms.games.fake_game_state import FakeGameState
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

        `action` must be in the set of legal actions (see `legal_actions`).
        '''
        self._actions.append(action)

    def do_after_play(self, action):
        '''Apply the given action, yield the new state, and undo the action
        application afterwards.'''
        self.play(action)
        yield self
        self.undo()

    def undo(self):
        '''Reverse the effect of the last action that was played'''
        self._actions.pop()

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
    patient = MctsAgent.Mcts(exploration=1)
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
    patient = MctsAgent.Mcts(exploration=1)
    num_iterations = 10
    stats = patient.search(state, num_iterations=num_iterations)

    assert stats['num_iterations_completed'] == 10
    assert stats['time_used_s'] is not None
    assert stats['num_nodes_expanded'] == 11
