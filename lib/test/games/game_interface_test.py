from games_puzzles_algorithms.games.hex.game_state import GameState as HexGameState
from games_puzzles_algorithms.games.fake_game_state import FakeGameState
from games_puzzles_algorithms.games.ttt.game_state import GameState as TttGameState
import pytest


def game_states():
    return [
        FakeGameState(),
        HexGameState.root(),
        TttGameState()
    ]


@pytest.mark.parametrize('game_state', game_states())
def test_num_legal_actions(game_state):
    assert (len(list(game_state.legal_actions()))
            == game_state.num_legal_actions())


@pytest.mark.parametrize('game_state', game_states())
def test_legal_actions(game_state):
    game_state.legal_actions()


@pytest.mark.parametrize('game_state, action', [
    (g, 0) for g in game_states()] + [(g, 1) for g in game_states()
])
def test_play(game_state, action):
    assert game_state == game_state.play(action)


@pytest.mark.parametrize('game_state', game_states())
def test_undo(game_state):
    game_state.undo()


@pytest.mark.parametrize('game_state, player', [
    (g, 0) for g in game_states()] + [(g, 1) for g in game_states()
])
def test_player_to_act(game_state, player):
    game_state.set_player_to_act(player)
    assert game_state.player_to_act() == player


@pytest.mark.parametrize('game_state, player', [
    (g, 0) for g in game_states()] + [(g, 1) for g in game_states()
])
def test_player_who_acted_last(game_state, player):
    game_state.set_player_to_act(player)
    game_state.play(0)
    assert game_state.player_who_acted_last() == player
    game_state.play(1)
    game_state.undo()
    assert game_state.player_who_acted_last() == player


@pytest.mark.parametrize('game_state', game_states())
def test_is_terminal(game_state):
    game_state.is_terminal()


@pytest.mark.parametrize('game_state, player', [
    (g, 0) for g in game_states()] + [(g, 1) for g in game_states()
])
def test_score(game_state, player):
    game_state.score(player)


@pytest.mark.parametrize('game_state, action', [
    (g, 0) for g in game_states()] + [(g, 1) for g in game_states()
])
def test_do_after_play(game_state, action):
    with game_state.play(action):
        pass
