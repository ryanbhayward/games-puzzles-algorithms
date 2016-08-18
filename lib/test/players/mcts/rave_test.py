from games_puzzles_algorithms.players.mcts.rave_agent \
    import RaveAgent, RaveNode, INF
from games_puzzles_algorithms.players.mcts.mcts_agent import UctNode
from games_puzzles_algorithms.games.fake_game_state import FakeGameState
import pytest
import random


def test_backup():
    rave_moves = {0: [0]}
    root = RaveNode(1, 300)
    state = FakeGameState()
    RaveNode.enable_rave(state)
    root.expand(state)
    children = root.child_nodes()
    children[0].expand(state)
    children[0].child_nodes()[0].backup(-1, rave_moves)
    assert children[0].child_nodes()[0].avg_reward == -1
    assert children[0].child_nodes()[1].avg_reward == 0
    assert children[0].avg_reward == 1
    assert children[1].num_children() == 0
    assert children[1].avg_reward == 0
    children[0].child_nodes()[1].backup(1, rave_moves)
    assert children[0].child_nodes()[0].avg_reward == -1
    assert children[0].child_nodes()[1].avg_reward == 1
    assert children[0].avg_reward == 0
    assert children[1].num_children() == 0
    assert children[1].avg_reward == 0


def test_backup_with_value():
    rave_moves = {0: [0]}
    root = RaveNode(1, 300)
    state = FakeGameState()
    root.expand(state)
    children = root.child_nodes()
    children[0].expand(state)
    children[0].child_nodes()[0].backup(-1, rave_moves)
    assert children[0].child_nodes()[0].rave_num_visits == 1
    assert children[0].child_nodes()[1].rave_num_visits == 0
    assert children[0].value() == 1
    assert children[1].value() == INF
    assert children[0].child_nodes()[0].value() == -1
    assert children[0].child_nodes()[1].value() == INF
    children[0].child_nodes()[1].backup(1, rave_moves)
    assert children[0].child_nodes()[0].rave_num_visits == 2
    assert children[0].child_nodes()[1].rave_num_visits == 0
    assert children[0].value() == 0.8325546111576977
    assert children[0].child_nodes()[0].value() == 1.1740766891821415
    assert children[0].child_nodes()[1].value() == 1.1807433558488079


def test_roll_out():
    random.seed(0)

    state = FakeGameState()
    RaveNode.enable_rave(state)
    patient = RaveAgent(random)
    outcome = patient.roll_out(state, 0)
    assert outcome['score'] == 2
    print(outcome)
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

    state = FakeGameState()
    patient = RaveAgent(random)
    num_iterations = 10
    stats = patient.search(state, num_iterations=num_iterations)

    assert stats['num_iterations_completed'] == 10
    assert stats['time_used_s'] is not None
    assert stats['num_nodes_expanded'] == 9
