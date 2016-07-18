from __future__ import division
import time
from games_puzzles_algorithms import debug
from games_puzzles_algorithms.players.minimax.minimax_agent import MinimaxAgent
import logging

INF = float('inf')


class AlphaBetaAgent(MinimaxAgent):
    """
    Alpha-Beta heuristic search class.
    Currently only solves zero-sum games where turns alternate.
    """

    def __init__(self):
        self.pruned_nodes = 0

    def value(self, game_state, alpha=-INF, beta=INF, time_allowed_s=-1,
              time_used=0, max_depth=-1, tree=None):
        """
        Return the game theoretic value of game state, `game_state`.

        If the remaining time, `time_allowed_s` - `time_used` is insufficient,
        then return the best value encountered so far.
        A non-positive `time_allowed_s` implies no time limit.

        If max_depth is non-negative, the search will only go up to max_depth
        below the current node before applying a heuristic.
        """

        if tree is None:
            self._tree = {}
            tree = self._tree
        tree['value'] = -INF

        if game_state.is_terminal():
            tree['value'] = -game_state.score(
                game_state.player_who_acted_last())
        elif max_depth == 0:
            tree['value'] = -game_state.heuristic(
                game_state.player_who_acted_last())
        elif time_allowed_s > 0 and not(time_used < time_allowed_s):
            raise self.TimeIsUp
        else:
            tree['children'] = []
            start_time = time.clock() if time_allowed_s > 0 else 0
            actions_considered = 0
            num_actions = game_state.num_legal_actions()
            for action in game_state.legal_actions():
                actions_considered += 1
                tree['children'].append({'action': action})
                with game_state.play(action):
                    action_value = -self.value(
                        game_state,
                        -beta,
                        -alpha,
                        time_allowed_s,
                        (time_used + time.clock() - start_time),
                        max_depth - 1,
                        tree['children'][-1])
                    if action_value > tree['value']:
                        tree['value'] = action_value
                    if tree['value'] >= beta:
                        self.pruned_nodes += num_actions - actions_considered
                        return tree['value']
                    alpha = max(alpha, tree['value'])

        return tree['value']

    def select_action(self, game_state, time_allowed_s=-1, max_depth=-1):
        """
        Select an action in game state, `game_state`.

        Return an optimal action in game state, `game_state`, if the time
        allowed, `time_allowed_s` is sufficient. Otherwise, return the best
        action found after `time_allowed_s` seconds. A non-positive
        `time_allowed_s` implies no time limit.

        If max_depth is positive the search only goes to max_depth below the
        rootnode before applying a heuristic.
        """
        self.pruned_nodes = 0
        start_time = time.clock() if time_allowed_s > 0 else 0
        best_action = None
        action_value = -INF

        debug.log({'Time available in seconds': time_allowed_s},
                  level=logging.INFO)
        debug.log(str(game_state), level=logging.INFO, raw=True)

        self._tree = {'children': [], 'value': action_value}

        for action in game_state.legal_actions():
            self._tree['children'].append({'action': action})
            with game_state.play(action):
                try:
                    action_value = -self.value(
                        game_state,
                        -INF,
                        INF,
                        time_allowed_s,
                        time.clock() - start_time,
                        max_depth - 1,
                        self._tree['children'][-1])
                except self.TimeIsUp:
                    if best_action is None:
                        best_action = action
                        self._tree['value'] = action_value
                    debug.log({'Time is up': True,
                               'Best action so far:': best_action,
                               'Value': self._tree['value']},
                               level=logging.INFO)
                    break
                else:
                    log_time = time_allowed_s - (time.clock() - start_time)
                    debug.log({'Time remaining in seconds': log_time,
                               'Best action so far:': best_action,
                               'New value': action_value,
                               'Value': self._tree['value'],
                               'Tree': self.to_dict()},
                               level=logging.INFO)
                    if action_value > self._tree['value']:
                        best_action = action
                        self._tree['value'] = action_value

                        debug.log({'Time remaining in seconds': log_time,
                                   'Best action so far:': best_action,
                                   'Value': self._tree['value']},
                                   level=logging.INFO)

        log_time = time_allowed_s - (time.clock() - start_time)
        debug.log({'Time remaining in seconds': log_time,
                   'Best action so far:': best_action,
                   'Value': self._tree['value'],
                   'Tree': self.to_dict(),
                   'Pruned nodes': self.pruned_nodes}, level=logging.INFO)
        return best_action
