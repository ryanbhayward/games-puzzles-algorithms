class FakeGameState(object):
    def __init__(self):
        self._player_to_act = 0

    def num_legal_actions(self):
        return 2

    def legal_actions(self):
        for a in range(2):
            yield a

    def play(self, action):
        '''Apply the given action.

        `action` must be in the set of legal actions (see `legal_actions`).
        '''
        pass

    def do_after_play(self, action):
        '''Apply the given action, yield the new state, and undo the action
        application afterwards.'''
        self.play(action)
        yield self
        self.undo()

    def undo(self):
        '''Reverse the effect of the last action that was played'''
        pass

    def set_player_to_act(self, player):
        self._player_to_act = player

    def player_to_act(self):
        return self._player_to_act

    def is_terminal(self):
        return False

    def score(self, player):
        return None if self.is_terminal() else 0
