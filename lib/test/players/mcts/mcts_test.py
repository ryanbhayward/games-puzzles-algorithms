from games_puzzles_algorithms.players.mcts.mcts_agent import MctsAgent
from games_puzzles_algorithms.games.fake_game_state import FakeGameState
from games_puzzles_algorithms.debug import log
import pytest
import random


def test_roll_out():
    random.seed(0)

    state = FakeGameState()
    patient = MctsAgent(random, exploration=1)
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

    state = FakeGameState()
    patient = MctsAgent(random, exploration=1)
    num_iterations = 10
    stats = patient.search(state, num_iterations=num_iterations)

    assert stats['num_iterations_completed'] == 10
    assert stats['time_used_s'] is not None
    assert stats['num_nodes_expanded'] == 7


def test_verbose_search():
    import json
    import logging
    logging.basicConfig(level=logging.DEBUG)

    random.seed(0)

    state = FakeGameState()
    patient = MctsAgent(random, exploration=1)
    num_iterations = 2
    stats = patient.search(state, num_iterations=num_iterations)

    assert stats['num_iterations_completed'] == 2
    assert stats['time_used_s'] is not None
    assert stats['num_nodes_expanded'] == 3

    print(json.dumps({'statistics': stats, 'tree': patient.to_dict()},
                     sort_keys=True,
                     indent=4))
