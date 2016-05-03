from games_puzzles_algorithms.game.dex.game_state import GameState as DexGameState
from games_puzzles_algorithms.game.hex.game_state import GameState as HexGameState
import pytest


class FakeGameState(object):
    def __init__(self):
        self._player_to_act = 0

    def num_legal_actions(self):
        return 2

    def legal_actions(self):
        for a in range(2):
            yield a

    def play(self, action):
        pass

    def do_after_play(self, action):
        self.play(action)
        yield self
        self.undo()

    def undo(self):
        pass

    def set_player_to_act(self, player):
        self._player_to_act = player

    def player_to_act(self):
        return self._player_to_act

    def is_terminal(self):
        return False

    def score(self):
        return None if self.is_terminal() else 0


def game_states():
    return [
        FakeGameState(),
        #DexGameState.root(),
        #HexGameState.root()
    ]


@pytest.mark.parametrize('game_state', game_states())
def test_num_legal_actions(game_state):
    game_state.num_legal_actions()
    assert len(list(game_state.legal_actions())) == game_state.num_legal_actions()


@pytest.mark.parametrize('game_state', game_states())
def test_legal_actions(game_state):
    game_state.legal_actions()


@pytest.mark.parametrize('game_state, action', [
    (g, 0) for g in game_states()] + [(g, 1) for g in game_states()
])
def test_play(game_state, action):
    game_state.play(action)


@pytest.mark.parametrize('game_state', game_states())
def test_undo(game_state):
    game_state.undo()


@pytest.mark.parametrize('game_state, player', [
    (g, 0) for g in game_states()] + [(g, 1) for g in game_states()
])
def test_player_to_act(game_state, player):
    game_state.set_player_to_act(player)
    assert game_state.player_to_act() == player


@pytest.mark.parametrize('game_state', game_states())
def test_is_terminal(game_state):
    game_state.is_terminal()


@pytest.mark.parametrize('game_state', game_states())
def test_score(game_state):
    game_state.score()

@pytest.mark.parametrize('game_state, action', [
    (g, 0) for g in game_states()] + [(g, 1) for g in game_states()
])
def test_do_after_play(game_state, action):
    game_state.do_after_play(action)
