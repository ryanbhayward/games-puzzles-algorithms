class FirstActionAgent(object):
    """docstring for FirstActionAgent"""
    def __init__(self):
        super(FirstActionAgent, self).__init__()

    def select_action(self, state):
        return next(state.legal_actions())

    def reset(self):
        pass
