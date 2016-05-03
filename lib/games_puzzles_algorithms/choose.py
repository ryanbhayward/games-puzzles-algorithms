from collections import defaultdict


def _items_from_list(l):
    for i in range(len(l)):
        yield i, l[i]


def _items_from_dict(l):
    return l.items()


def choose_from_distribution(distribution, random_number):
    s = 0
    last_key = None
    items = (
        _items_from_dict if hasattr(distribution, 'items')
        else _items_from_list
    )
    for i, weight in items(distribution):
        s += weight
        if s > random_number:
            return i
        else:
            last_key = i
    return last_key


def choose_legal_action_uniformly_randomly(state, random_number):
    s = 0
    uniform_weight = 1.0 / state.num_legal_actions()
    for action in state.legal_actions():
        s += uniform_weight
        if s > random_number:
            return action
    return action


def probability_distribution_over_legal_actions(
    state,
    distribution,
    sum_over_distribution,
    new_distribution=lambda: defaultdict(lambda: 0.0)
):
    p = new_distribution()
    if sum_over_distribution > 0.0:
        for action in state.legal_actions():
            p[action] = distribution[action] / sum_over_distribution
    else:
        uniform_weight = 1.0 / state.num_legal_actions()
        for action in state.legal_actions():
            p[action] = uniform_weight
    return p
