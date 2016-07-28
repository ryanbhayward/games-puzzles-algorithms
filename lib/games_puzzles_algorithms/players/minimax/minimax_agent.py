from __future__ import division
import time
import random
from math import sqrt, log
from copy import deepcopy
INF = float('inf')


class MinimaxAgent(object):
    '''Currently only solves zero-sum games where turns alternate'''
    class TimeIsUp(Exception): pass

    def value(self, game_state, time_allowed_s=-1, time_used=0):
        if game_state.is_terminal():
            return -game_state.score(game_state.player_who_acted_last())
        elif time_allowed_s > 0 and not(time_used < time_allowed_s):
            raise self.TimeIsUp
        else:
            start_time = time.clock() if time_allowed_s > 0 else 0
            best_value = -INF
            for action in game_state.legal_actions():
                with game_state.play(action):
                    action_value = -self.value(
                        game_state,
                        time_allowed_s=time_allowed_s,
                        time_used=(time_used + time.clock()) - start_time)
                    if action_value > best_value:
                        best_value = action_value
            return best_value

    def select_action(self, game_state, time_allowed_s=-1, **_):
        start_time = time.clock() if time_allowed_s > 0 else 0
        best_action = None
        best_value = -INF
        for action in game_state.legal_actions():
            with game_state.play(action):
                try:
                    action_value = -self.value(
                        game_state,
                        time_allowed_s=time_allowed_s,
                        time_used=time.clock() - start_time)
                except self.TimeIsUp:
                    return action if best_action is None else best_action
                else:
                    if action_value > best_value:
                        best_action = action
                        best_value = action_value
        return best_action

    def reset(self): pass
