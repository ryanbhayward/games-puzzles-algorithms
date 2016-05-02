from games_puzzles_algorithms.choose import choose_legal_action_uniformly_randomly


class FirstActionAgent(object):
    """docstring for FirstActionAgent"""
    def __init__(self):
        super(FirstActionAgent, self).__init__()

    def act(self, state):
        return next(state.legal_actions())

    def reset(self):
        pass
