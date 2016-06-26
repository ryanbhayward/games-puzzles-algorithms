class FirstActionAgent(object):
    """docstring for FirstActionAgent"""
    def select_action(self, state, time_available=-1):
        return next(state.legal_actions())

    def reset(self):
        pass
