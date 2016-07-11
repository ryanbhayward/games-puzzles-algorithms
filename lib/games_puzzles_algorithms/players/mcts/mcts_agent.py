from __future__ import division
import time
from math import sqrt, log
from games_puzzles_algorithms.choose import choose_legal_action_randomly
import games_puzzles_algorithms.debug as debug
import logging
import json
INF = float('inf')


def random_roll_out_policy(state, r):
    return choose_legal_action_randomly(state, r)


class UctNode(object):

    def __init__(self, action=None, parent=None, acting_player=None):
        self.action = action
        self.parent = parent
        self.num_visits = 0  # times this position was visited
        self.avg_reward = 0  # average reward (wins-losses) from this position
        self._children = []
        self.acting_player = acting_player

    def expand(self, game_state):
        if game_state.num_legal_actions() > 0:
            assert(not game_state.is_terminal())

            self.acting_player = game_state.player_to_act()
            for action in game_state.legal_actions():
                self._children.append(UctNode(
                    action=action,
                    parent=self))

    def backup(self, score=0):
        """Update the node statistics on the path from the passed node to
        root to reflect the value of the given `simulation_statistics`.
        """
        self.num_visits += 1
        self.avg_reward += (score - self.avg_reward) / self.num_visits
        if self.parent:
            self.parent.backup(score=-score)

    def value(self, explore=0):
        return self.lcb(explore=explore)

    def ucb(self, explore=0):
        """Return the upper confidence bound of this node.

        The parameter `explore` specifies how much the value should favor
        nodes that have yet to be thoroughly explored versus nodes that
        seem to have a high win rate. `explore` is set to zero by default
        which means that the action with the highest winrate will have
        the greatest value.
        """
        if self.num_visits == 0:
            if explore == 0:
                return 0
            else:
                return INF
        else:
            return (self.avg_reward
                    + explore
                    * sqrt(2 * log(self.parent.num_visits) / self.num_visits))

    def lcb(self, explore=0):
        """Return the lower confidence bound of this node.

        The parameter `explore` specifies how much the value should favor
        nodes that have yet to be thoroughly explored versus nodes that
        seem to have a high win rate. `explore` is set to zero by default
        which means that the action with the highest winrate will have
        the greatest value.
        """
        # unless explore is set to zero, maximally favor unexplored nodes
        if self.num_visits == 0:
            return 0
        else:
            return (self.avg_reward
                    - explore
                    * sqrt(2 * log(self.parent.num_visits) / self.num_visits))

    def child_nodes(self):
        return self._children

    def is_leaf(self):
        return len(self._children) < 1

    def is_root(self):
        return self.parent is None

    def favorite_children(self, exploration=0):
        max_value = max(
            self.child_nodes(),
            key=lambda n: n.value(exploration)).value(exploration)
        return [n for n in self.child_nodes()
                if (n.value(exploration) == max_value)]

    def num_children(self):
        count = 0
        for child in self.child_nodes():
            count += child.num_children() + 1
        return count

    def num_nodes(self):
        return self.num_children() + 1

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


class MctsAgent(object):

    class Mcts(object):

        class TimeIsUp(Exception):
            pass

        @classmethod
        def with_same_parameters(self, other):
            return self(node_generator=other._node_generator,
                        exploration=other._exploration)

        def __init__(self,
                     random_generator,
                     node_generator=UctNode,
                     exploration=1):
            self._random = random_generator
            self._node_generator = node_generator
            self._exploration = exploration
            self._root = None

        def reset(self):
            self._root = None

        def good_action(self,
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
            self.search(game_state,
                        time_allowed_s=time_allowed_s,
                        num_iterations=num_iterations)
            return self._random.choice(self._root.favorite_children()).action

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

            self._root = self._node_generator()
            self._root.expand(root_state)

            debug.log({'Initial search tree': (
                self._root.info_strings_to_dict()
            ),
                'Time available in seconds': time_allowed_s,
                '# iterations': num_iterations}, level=logging.INFO)
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
                except self.TimeIsUp:
                    break

                debug.log("Executing roll-out from (player {} is acting):"
                          .format(game_state.player_to_act()),
                          level=logging.INFO)
                debug.log(str(game_state), level=logging.INFO, raw=True)

                rollout_results = self.roll_out(game_state, player_of_interest)
                debug.log({'Roll-out results': rollout_results})
                node.backup(**rollout_results)

                debug.log({'Updated search tree': (
                    self._root.info_strings_to_dict()),
                    'Seconds used': time_used_s,
                    '# iterations completed': (num_iterations_completed
                                               + 1)})
                for _ in range(num_actions):
                    game_state.undo()
                num_iterations_completed += 1
            return {'num_iterations_completed': num_iterations_completed,
                    'time_used_s': time_used_s,
                    'num_nodes_expanded': self._root.num_nodes()}

        def node_value(self, n):
            return n.ucb(self._exploration)

        def select_node(self,
                        node,
                        game_state,
                        time_is_available=lambda: True):
            assert(not game_state.is_terminal())

            num_actions = 0
            my_child_nodes = node.child_nodes()
            while len(my_child_nodes) > 0:
                if not time_is_available():
                    raise self.TimeIsUp()

                max_value = self.node_value(
                    max(
                        my_child_nodes,
                        key=lambda n: self.node_value(n)
                    )
                )
                max_nodes = [n for n in my_child_nodes if (self.node_value(n)
                                                           == max_value)]
                node = self._random.choice(max_nodes)

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

        def roll_out(self,
                     state,
                     player_of_interest,
                     roll_out_policy=random_roll_out_policy):
            """
            Simulate a play-out from the passed game state, `state`.

            Return roll out statistics from the perspective of
            `player_of_interest`.
            """
            if state.is_terminal():
                return {'score': state.score(player_of_interest)}
            else:
                outcome = None
                action = roll_out_policy(state, self._random.random())
                with state.play(action):
                    outcome = self.roll_out(state, player_of_interest)
                return outcome

        def __len__(self):
            """Return the number of nodes in search tree."""
            return len(self._root)

        def info_strings_to_dict(self):
            return self._root.info_strings_to_dict()

        def to_dict(self):
            return self._root.to_dict()

    def __init__(self,
                 random_generator,
                 node_generator=UctNode,
                 exploration=1):
        self._search_tree = self.Mcts(random_generator,
                                      node_generator,
                                      exploration)

    def select_action(self,
                      game_state,
                      time_allowed_s=-1,
                      num_iterations=-1,
                      **_):
        return self._search_tree.good_action(
            game_state,
            time_allowed_s=time_allowed_s,
            num_iterations=num_iterations)

    def reset(self): self._search_tree.reset()

    def info_strings_to_dict(self):
        return self._search_tree.info_strings_to_dict()

    def to_dict(self):
        return self._search_tree.to_dict()
