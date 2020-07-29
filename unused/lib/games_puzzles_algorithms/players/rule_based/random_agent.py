from games_puzzles_algorithms.choose \
    import choose_legal_action_randomly


class RandomAgent(object):
    """docstring for RandomAgent"""
    def __init__(self, random_generator):
        self.random_generator = random_generator

    def select_action(self, state, **_):
        return choose_legal_action_randomly(
            state, self.random_generator())

    def reset(self):
        pass
