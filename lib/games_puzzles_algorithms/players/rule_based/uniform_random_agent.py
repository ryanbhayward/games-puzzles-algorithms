from games_puzzles_algorithms.choose \
    import choose_legal_action_uniformly_randomly


class UniformRandomAgent(object):
    """docstring for UniformRandomAgent"""
    def __init__(self, random_generator):
        super(UniformRandomAgent, self).__init__()
        self.random_generator = random_generator

    def select_action(self, state, time_available=-1):
        return choose_legal_action_uniformly_randomly(
            state, self.random_generator())

    def reset(self):
        pass
