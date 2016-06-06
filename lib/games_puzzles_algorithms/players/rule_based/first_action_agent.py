class FirstActionAgent(object):
    """docstring for FirstActionAgent"""
    def __init__(self):
        super(FirstActionAgent, self).__init__()

    def select_action(self, state, time_available=-1):
        return next(state.legal_actions())

    def reset(self):
        pass
