from games_puzzles_algorithms.players.mcts.mcts_agent import MctsAgent
from games_puzzles_algorithms.players.mcts.mcts_agent import UctNode
from games_puzzles_algorithms.players.mcts.mcts_agent import BanditNode
from games_puzzles_algorithms.games.fake_game_state import FakeGameState
from games_puzzles_algorithms.debug import log
import random


def test_roll_out():
    random.seed(0)

    state = FakeGameState()
    patient = MctsAgent(random, UctNode(1))
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


def test_search_explore3():
    random.seed(0)

    state = FakeGameState()
    patient = MctsAgent(random, UctNode(3))
    num_iterations = 10
    stats = patient.search(state, num_iterations=num_iterations)

    assert stats['num_iterations_completed'] == 10
    assert stats['time_used_s'] is not None
    assert stats['num_nodes_expanded'] == 11


def test_search_explore2():
    random.seed(0)

    state = FakeGameState()
    patient = MctsAgent(random, UctNode(2))
    num_iterations = 10
    stats = patient.search(state, num_iterations=num_iterations)

    assert stats['num_iterations_completed'] == 10
    assert stats['time_used_s'] is not None
    assert stats['num_nodes_expanded'] == 9


def test_search_explore1():
    random.seed(0)

    state = FakeGameState()
    patient = MctsAgent(random, UctNode(1))
    num_iterations = 10
    stats = patient.search(state, num_iterations=num_iterations)

    assert stats['num_iterations_completed'] == 10
    assert stats['time_used_s'] is not None
    assert stats['num_nodes_expanded'] == 9


def test_child_nodes():
    root = BanditNode()
    assert root.child_nodes() == []


def test_expand():
    root = BanditNode()
    state = FakeGameState()
    root.expand(state)
    children = root.child_nodes()
    assert len(children) == 2
    assert children[0].action == 0
    assert children[1].action == 1
    assert children[0].parent == root
    assert children[1].parent == root


def test_is_leaf():
    root = BanditNode()
    assert root.is_leaf()
    state = FakeGameState()
    root.expand(state)
    assert not root.is_leaf()


def test_is_root():
    root = BanditNode()
    state = FakeGameState()
    root.expand(state)
    assert root.is_root()
    for child in root.child_nodes():
        assert not child.is_root()


def test_child_nodes():
    root = BanditNode()
    state = FakeGameState()
    root.expand(state)
    assert len(root.child_nodes()) == 2
    for child in root.child_nodes():
        assert len(child.child_nodes()) == 0


def test_num_nodes():
    root = BanditNode()
    state = FakeGameState()
    root.expand(state)
    assert root.num_nodes() == 3
    for child in root.child_nodes():
        assert child.num_nodes() == 1


def test_ucb_initial_explore():
    root = BanditNode()
    state = FakeGameState()
    root.expand(state)
    children = root.child_nodes()
    for child in children:
        assert BanditNode.ucb_value(child, 1) == float('inf')


def test_backup():
    root = BanditNode()
    state = FakeGameState()
    root.expand(state)
    children = root.child_nodes()

    state.play(children[0].action)
    children[0].expand(state)

    children[0].child_nodes()[0].backup(-1)
    assert children[0].child_nodes()[0].avg_reward() == -1
    assert children[0].child_nodes()[1].avg_reward() == 0
    assert children[0].avg_reward() == 1
    assert len(children[1].child_nodes()) == 0
    assert children[1].avg_reward() == 0
    children[0].child_nodes()[1].backup(1)
    assert children[0].child_nodes()[0].avg_reward() == -1
    assert children[0].child_nodes()[1].avg_reward() == 1
    assert children[0].avg_reward() == 0
    assert len(children[1].child_nodes()) == 0
    assert children[1].avg_reward() == 0


def test_backup_with_lcb():
    root = BanditNode()
    state = FakeGameState()
    root.expand(state)
    children = root.child_nodes()

    state.play(children[0].action)
    children[0].expand(state)

    children[0].child_nodes()[0].backup(-1)
    children[0].child_nodes()[1].backup(1)
    assert BanditNode.lcb_value(children[0], 1) == -0.8325546111576977
    assert BanditNode.lcb_value(children[0].child_nodes()[0], 1) == (
        -2.177410022515475)
    assert BanditNode.lcb_value(children[0].child_nodes()[1], 1) == (
        -0.17741002251547466)


def test_backup_with_ucb():
    root = BanditNode()
    state = FakeGameState()
    root.expand(state)
    children = root.child_nodes()

    state.play(children[0].action)
    children[0].expand(state)

    children[0].child_nodes()[0].backup(-1)
    children[0].child_nodes()[1].backup(1)
    assert BanditNode.ucb_value(children[0], 1) == 0.8325546111576977
    assert BanditNode.ucb_value(children[0].child_nodes()[0], 1) == (
        0.17741002251547466)
    assert BanditNode.ucb_value(children[0].child_nodes()[1], 1) == (
        2.177410022515475)


def test_backup_with_value():
    root = BanditNode()
    state = FakeGameState()
    root.expand(state)
    children = root.child_nodes()

    state.play(children[0].action)
    children[0].expand(state)

    children[0].child_nodes()[0].backup(1)
    assert children[0].value() == -1
    assert children[1].value() == 0
    assert children[0].child_nodes()[0].value() == 1
    assert children[0].child_nodes()[1].value() == 0
    children[0].child_nodes()[1].backup(-1)
    assert children[0].value() == 0
    assert children[0].child_nodes()[0].value() == 1
    assert children[0].child_nodes()[1].value() == -1


def test_backup_with_ucb_explore():
    root = UctNode(1)
    state = FakeGameState()
    root.expand(state)
    children = root.child_nodes()

    state.play(children[0].action)
    children[0].expand(state)

    children[0].child_nodes()[0].backup(1)
    assert children[0].value() == -1
    assert children[1].value() == float("inf")
    assert children[0].child_nodes()[0].value() == 1
    assert children[0].child_nodes()[1].value() == float("inf")
    children[0].child_nodes()[1].backup(-1)
    assert children[0].value() > 0
    assert children[0].child_nodes()[0].value() > 1
    assert children[0].child_nodes()[1].value() > -1


def test_favorite_child():
    root = UctNode(1)
    state = FakeGameState()
    root.expand(state)
    children = root.child_nodes()
    children[0].backup(1)
    children[1].backup(-1)
    value_of_favorite = root.favorite_children()[0].value()
    for child in children:
        assert child.value() <= value_of_favorite


def test_info_strings_to_json():
    root = BanditNode()
    state = FakeGameState()
    root.expand(state)
    children = root.child_nodes()
    children[0].backup(1)
    children[1].backup(-1)
    info = root.info_strings_to_dict()
    assert info["info"] == "avg_reward: 0.0 num_visits: 2"
    assert info["children"][0][
        "info"] == "player: 0 action: 0 | avg_reward: 1.0 num_visits: 1"
    assert info["children"][1][
        "info"] == "player: 0 action: 1 | avg_reward: -1.0 num_visits: 1"


def test_info_strings_to_json_ucb():
    root = UctNode(1)
    state = FakeGameState()
    root.expand(state)
    children = root.child_nodes()
    children[0].backup(1)
    children[1].backup(-1)
    info = root.info_strings_to_dict()
    assert info[
        "info"] == "avg_reward: 0.0 num_visits: 2 ucb_value: 0.8325546111576977"
    assert info["children"][0][
        "info"] == "player: 0 action: 0 | avg_reward: 1.0 num_visits: 1 ucb_value: 2.177410022515475"
    assert info["children"][1][
        "info"] == "player: 0 action: 1 | avg_reward: -1.0 num_visits: 1 ucb_value: 0.17741002251547466"


def test_str():
    root = BanditNode()
    state = FakeGameState()
    assert str(root) == '{\n    "info": "avg_reward: 0 num_visits: 0"\n}'


def test_verbose_search():
    import json
    import logging
    logging.basicConfig(level=logging.DEBUG)

    random.seed(0)

    state = FakeGameState()
    patient = MctsAgent(random, UctNode(1))
    num_iterations = 2
    stats = patient.search(state, num_iterations=num_iterations)

    assert stats['num_iterations_completed'] == num_iterations
    assert stats['time_used_s'] is not None
    assert stats['num_nodes_expanded'] == 3

    print(json.dumps({'statistics': stats, 'tree': patient.to_dict()},
                     sort_keys=True,
                     indent=4))
