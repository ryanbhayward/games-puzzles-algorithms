class FirstActionAgent(object):
    """docstring for FirstActionAgent"""
    def select_action(self, state, **_):
        return next(state.legal_actions())

    def reset(self):
        pass
