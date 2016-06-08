from __future__ import division
import time
import random
from math import sqrt, log
from copy import deepcopy
INF = float('inf')


class MinimaxAgent(object):
    '''Currently only solves zero-sum games where turns alternate'''
    class TimeIsUp(Exception): pass

    def value(self, game_state, time_available=-1, time_used=0):
        if game_state.is_terminal():
            return -game_state.score(game_state.player_who_acted_last())
        elif time_available > 0 and not(time_used < time_available):
            raise self.TimeIsUp
        else:
            start_time = time.clock() if time_available > 0 else 0
            best_value = -INF
            for action in game_state.legal_actions():
                with game_state.play(action):
                    action_value = -self.value(
                        game_state,
                        time_available=time_available,
                        time_used=(time_used + time.clock()) - start_time)
                    if action_value > best_value:
                        best_value = action_value
            return best_value

    def select_action(self, game_state, time_available=-1):
        start_time = time.clock() if time_available > 0 else 0
        best_action = None
        best_value = -INF
        for action in game_state.legal_actions():
            with game_state.play(action):
                try:
                    action_value = -self.value(
                        game_state,
                        time_available=time_available,
                        time_used=time.clock() - start_time)
                except self.TimeIsUp:
                    return action if best_action is None else best_action
                else:
                    if action_value > best_value:
                        best_action = action
                        best_value = action_value
        return best_value

    def reset(self): pass
