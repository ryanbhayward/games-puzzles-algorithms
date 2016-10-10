from __future__ import division
import time
import random
import games_puzzles_algorithms.debug as debug
import logging
INF = float('inf')


class MinimaxAgent(object):
    '''Solves zero-sum alternating move games.'''

    class TimeIsUp(Exception):
        pass

    def value(self, game_state, time_allowed_s=-1, time_used=0, tree=None):
        '''Return the game theoretic value of game state, `game_state`.

        If the remaining time, `time_allowed_s` - `time_used` is insufficient,
        then return the best value encountered so far.

        A non-positive `time_allowed_s` implies no time limit.
        '''

        # Negamax implementation of the minimax algorithm

        if tree is None:
            self._tree = {}
            tree = self._tree
        tree['value'] = -INF

        if game_state.is_terminal():
            tree['value'] = -game_state.score(
                game_state.player_who_acted_last())
        elif time_allowed_s > 0 and not(time_used < time_allowed_s):
            raise self.TimeIsUp
        else:
            tree['children'] = []
            start_time = time.clock() if time_allowed_s > 0 else 0
            for action in game_state.legal_actions():
                tree['children'].append({'action': action})
                with game_state.play(action):
                    action_value = -self.value(
                        game_state,
                        time_allowed_s=time_allowed_s,
                        time_used=time.clock() - start_time + time_used,
                        tree=tree['children'][-1])
                    if action_value > tree['value']:
                        tree['value'] = action_value
        return tree['value']

    def to_dict(self):
        return self._tree

    def __str__(self):
        return json.dumps(self.to_dict(), sort_keys=True, indent=4)

    def select_action(self, game_state, time_allowed_s=-1, **_):
        '''Select an action in game state, `game_state`.

        Return an optimal action in game state, `game_state`, if the time
        allowed, `time_allowed_s` is sufficient. Otherwise, return the best
        action found after `time_allowed_s` seconds.

        A non-positive `time_allowed_s` implies no time limit.
        '''
        start_time = time.clock() if time_allowed_s > 0 else 0
        best_action = None
        action_value = -INF

        debug.log(lambda:{'Time available in seconds': time_allowed_s},
                  level=logging.INFO)
        debug.log(lambda:str(game_state), level=logging.INFO, raw=True)

        self._tree = {'children': [], 'value': action_value}

        for action in game_state.legal_actions():
            self._tree['children'].append({'action': action})
            with game_state.play(action):
                try:
                    action_value = -self.value(
                        game_state,
                        time_allowed_s=time_allowed_s,
                        time_used=time.clock() - start_time,
                        tree=self._tree['children'][-1])
                except self.TimeIsUp:
                    if best_action is None:
                        best_action = action
                        self._tree['value'] = action_value
                    debug.log(lambda:{'Time is up': True,
                               'Best action so far:': best_action,
                               'Value': self._tree['value']},
                              level=logging.INFO)
                    break
                else:
                    debug.log(lambda:{'Time remaining in seconds': (
                        time_allowed_s
                        - (time.clock() - start_time)),
                        'Best action so far:': best_action,
                        'New value': action_value,
                        'Value': self._tree['value'],
                        'Tree': self.to_dict()},
                        level=logging.INFO)
                    if action_value > self._tree['value']:
                        best_action = action
                        self._tree['value'] = action_value

                        debug.log(lambda:{'Time remaining in seconds': (
                            time_allowed_s
                            - (time.clock() - start_time)),
                            'Best action so far:': best_action,
                            'Value': self._tree['value']},
                            level=logging.INFO)
        debug.log(lambda:{'Time remaining in seconds': (
            time_allowed_s
            - (time.clock() - start_time)),
            'Best action so far:': best_action,
            'Value': self._tree['value'],
            'Tree': self.to_dict()}, level=logging.INFO)
        debug.log_t(lambda:{'Time remaining in seconds': (
            time_allowed_s
            - (time.clock() - start_time)),
            'Best action so far:': best_action,
            'Value': self._tree['value']}, level=logging.INFO)
        return best_action

    def reset(self): self._tree = {}
