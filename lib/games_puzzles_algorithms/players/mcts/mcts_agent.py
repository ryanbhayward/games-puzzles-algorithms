from __future__ import division
import time
from math import sqrt, log
from games_puzzles_algorithms.choose import choose_legal_action_randomly
import games_puzzles_algorithms.debug as debug
import logging
import json
INF = float('inf')


class TimeIsUp(Exception):
    pass


class BanditNode(object):

    @staticmethod
    def greedy_value(node):
        return node.avg_reward

    @staticmethod
    def ucb_value(node, exploration):
        """Return the upper confidence bound of the given node.

        The parameter `exploration` specifies how much the value should favor
        nodes that have yet to be thoroughly explored versus nodes that
        seem to have a high win rate.
        """
        if node.num_visits == 0:
            if exploration > 0:
                return INF
            else:
                return node.avg_reward
        else:
            return (node.avg_reward
                    + exploration
                    * sqrt(2 * log(node.parent.num_visits) / node.num_visits))

    @staticmethod
    def lcb_value(node, exploration):
        """Return the lower confidence bound of the given node.

        The parameter `exploration` specifies how much the value should favor
        nodes that have yet to be thoroughly explored versus nodes that
        seem to have a high win rate. `exploration` is set to zero by default
        which means that the action with the highest winrate will have
        the greatest value.
        """
        # unless explore is set to zero, maximally favor unexplored nodes
        if node.num_visits == 0:
            if exploration > 0:
                return -INF
            else:
                return node.avg_reward
        else:
            return (node.avg_reward
                    - exploration
                    * sqrt(2 * log(node.parent.num_visits) / node.num_visits))

    def __init__(self, action=None, parent=None, acting_player=None):
        self.reset(action=action, parent=parent, acting_player=acting_player)

    def reset(self, action=None, parent=None, acting_player=None):
        self.action = action
        self.parent = self if parent is None else parent
        self.num_visits = 0  # times this position was visited
        self.avg_reward = 0  # average reward (wins-losses) from this position
        self._children = []
        self.acting_player = acting_player

    def clone(self):
        return type(self)(action=self.action,
                          parent=self.parent,
                          acting_player=self.acting_player)

    def expand(self, game_state):
        if game_state.num_legal_actions() > 0:
            assert(not game_state.is_terminal())

            self.acting_player = game_state.player_to_act()
            for action in game_state.legal_actions():
                child = self.clone()
                child.reset(action=action, parent=self)
                self._children.append(child)

    def backup(self, score=0):
        """Update the node statistics on the path from the passed node to
        root to reflect the value of the given `simulation_statistics`.
        """
        self.num_visits += 1
        self.avg_reward += (score - self.avg_reward) / self.num_visits
        if not self.is_root():
            self.parent.backup(score=-score)

    def child_nodes(self): return self._children

    def is_leaf(self): return len(self._children) < 1

    def is_root(self): return self.parent is self

    def value(self): return self.avg_reward

    def favorite_children(self, value=None):
        if value is None:
            value = type(self).value
        max_value = value(max(self.child_nodes(), key=value))
        return [n for n in self.child_nodes() if value(n) == max_value]

    def num_descendents(self):
        count = 0
        for child in self.child_nodes():
            count += child.num_descendents() + 1
        return count

    def num_children(self): return len(self._children)

    def num_nodes(self): return self.num_descendents() + 1

    def info_strings_to_dict(self):
        d = {}
        d['info'] = "| avg_reward: {} num_visits: {}".format(self.avg_reward,
                                                             self.num_visits)
        if self.action is not None:
            d['info'] = "action: {} ".format(self.action) + d['info']
        if self.acting_player is not None:
            d['info'] = "player: {} ".format(self.acting_player) + d['info']
        if not self.is_leaf():
            d['children'] = []
            for n in self.child_nodes():
                d['children'].append(n.info_strings_to_dict())
        return d

    def to_dict(self):
        d = {'avg_reward': self.avg_reward, 'num_visits': self.num_visits}
        if self.action is not None:
            d["action"] = self.action
        if self.acting_player is not None:
            d['player'] = self.acting_player
        if not self.is_leaf():
            d['children'] = []
            for n in self.child_nodes():
                d['children'].append(n.to_dict())
        return d

    def __str__(self):
        return json.dumps(self.info_strings_to_dict(),
                          sort_keys=True,
                          indent=4)


class UctNode(BanditNode):

    def __init__(self, exploration, *args, **kwargs):
        super(UctNode, self).__init__(*args, **kwargs)
        self.exploration = exploration

    def clone(self):
        return type(self)(self.exploration,
                          action=self.action,
                          parent=self.parent,
                          acting_player=self.acting_player)

    def value(self): return BanditNode.ucb_value(self, self.exploration)

    def info_strings_to_dict(self):
        d = {}
        d['info'] = "| ucb_value: {} avg_reward: {} num_visits: {}".format(
            self.value(),
            self.avg_reward,
            self.num_visits)
        if self.action is not None:
            d['info'] = "action: {} ".format(self.action) + d['info']
        if self.acting_player is not None:
            d['info'] = "player: {} ".format(self.acting_player) + d['info']
        if not self.is_leaf():
            d['children'] = []
            for n in self.child_nodes():
                d['children'].append(n.info_strings_to_dict())
        return d

    def to_dict(self):
        d = {
            'ucb_value': self.value(),
            'avg_reward': self.avg_reward,
            'num_visits': self.num_visits
        }
        if self.action is not None:
            d["action"] = self.action
        if self.acting_player is not None:
            d['player'] = self.acting_player
        if not self.is_leaf():
            d['children'] = []
            for n in self.child_nodes():
                d['children'].append(n.to_dict())
        return d


class MctsAgent(object):

    @staticmethod
    def final_selection_rule(node): return node.num_visits

    @classmethod
    def with_same_parameters(self, other):
        return self(root=other._root.clone())

    def __init__(self, random_generator, root=None):
        self._random = random_generator
        self._root = UctNode(1) if root is None else root
        self.reset()

    def reset(self): self._root.reset()

    def select_action(self,
                      game_state,
                      time_allowed_s=-1,
                      num_iterations=-1):
        """Return a good action to play in `game_state`.

        Parameters:
        `game_state`: The state of the game for which an action is
        requested. Must adhere to the generic game state interface
        described by `games_puzzles_algorithms.games.fake_game_state`.
        `time_allowed_s`: The time allotted to search for a good action.
        Negative values imply that there is no time limit.
        Setting this to zero will ensure that an action is selected
        uniformly at random.
        `num_iterations`: The number of search iterations (rollouts) to
        complete. Negative values imply that there is not iteration
        limit. Setting this to zero will ensure that an action is selected
        uniformly at random.

        `time_allowed_s` and `num_iterations` cannot both be negative.
        """
        self.reset()
        self.search(game_state,
                    time_allowed_s=time_allowed_s,
                    num_iterations=num_iterations)
        return self._random.choice(
            self._root.favorite_children(
                type(self).final_selection_rule)).action

    def search(self, root_state, time_allowed_s=-1, num_iterations=-1):
        """Execute MCTS from `root_state`.

        Parameters:
        `root_state`: The state of the game from which to search.
        Must adhere to the generic game state interface
        described by `games_puzzles_algorithms.games.fake_game_state`.
        `time_allowed_s`: The time allotted to search for a good action.
        Negative values imply that there is no time limit.
        Setting this to zero will ensure that no search is done.
        `num_iterations`: The number of search iterations (rollouts) to
        complete. Negative values imply that there is not iteration
        limit. Setting this to zero will ensure that no search is done.

        If `time_allowed_s` and `num_iterations` are both negative,
        `num_iterations` will be set to 1.
        """
        if time_allowed_s < 0 and num_iterations < 0:
            num_iterations = 1
        if root_state.is_terminal():
            return None

        start_time = time.clock()

        self._root.expand(root_state)

        debug.log(
            {
                'Initial search tree': self._root.info_strings_to_dict(),
                'Time available in seconds': time_allowed_s,
                '# iterations': num_iterations
            },
            level=logging.INFO)
        debug.log(str(root_state), level=logging.INFO, raw=True)

        num_iterations_completed = 0
        player_of_interest = root_state.player_to_act()
        time_used_s = 0

        def time_is_available():
            nonlocal time_used_s
            time_used_s = time.clock() - start_time
            return (time_allowed_s < 0 or time_used_s < time_allowed_s)

        while (num_iterations < 1
               or num_iterations_completed < num_iterations):
            try:
                node, game_state, num_actions = self.select_node(
                    self._root,
                    root_state,
                    time_is_available=time_is_available)
            except TimeIsUp:
                break

            debug.log("Executing roll-out from (player {} is acting):"
                      .format(game_state.player_to_act()),
                      level=logging.INFO)
            debug.log(str(game_state), level=logging.INFO, raw=True)

            rollout_results = self.roll_out(game_state, player_of_interest)
            debug.log({'Roll-out results': rollout_results})
            node.backup(**rollout_results)

            debug.log(
                {
                    'Updated search tree': self._root.info_strings_to_dict(),
                    'Seconds used': time_used_s,
                    '# iterations completed': num_iterations_completed + 1
                },
                level=logging.INFO)

            for _ in range(num_actions):
                game_state.undo()
            num_iterations_completed += 1
        return {'num_iterations_completed': num_iterations_completed,
                'time_used_s': time_used_s,
                'num_nodes_expanded': self._root.num_nodes()}

    def select_node(self, node, game_state, time_is_available=lambda: True):
        assert(not game_state.is_terminal())

        num_actions = 0
        my_child_nodes = node.child_nodes()
        while len(my_child_nodes) > 0:
            if not time_is_available():
                raise TimeIsUp()

            node = self._random.choice(node.favorite_children())
            game_state.play(node.action)
            num_actions += 1

            # If some child node has not been explored select it
            # before expanding other children
            if node.num_visits == 0:
                return (node, game_state, num_actions)
            else:
                my_child_nodes = node.child_nodes()

        # If we reach a leaf node generate its children and
        # return one of them
        node.expand(game_state)
        my_child_nodes = node.child_nodes()
        if len(my_child_nodes) > 0:
            assert(not game_state.is_terminal())
            node = self._random.choice(node.child_nodes())
            game_state.play(node.action)
            num_actions += 1
        return (node, game_state, num_actions)

    def roll_out_policy(self, state):
        '''Random roll-out policy.'''
        return choose_legal_action_randomly(state, self._random.random())

    def evaluation(self, state, player_of_interest):
        return {'score': state.score(player_of_interest)}

    def roll_out(self, state, player_of_interest):
        """
        Simulate a play-out from the passed game state, `state`.

        Return roll out statistics from the perspective of
        `player_of_interest`.
        """
        if state.is_terminal():
            return self.evaluation(state, player_of_interest)
        else:
            outcome = None
            action = self.roll_out_policy(state)
            with state.play(action):
                outcome = self.roll_out(state, player_of_interest)
            return outcome

    def num_nodes_in_tree(self): return self._root.num_nodes()

    def info_strings_to_dict(self):
        return self._root.info_strings_to_dict()

    def to_dict(self):
        return self._root.to_dict()
