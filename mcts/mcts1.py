# Created by Luke Schultz
# Fall 2022, Winter 2023, Spring 2023, Summer 2023, Fall 2023
# Written with the help of GitHub Copilot

import time
from math import sqrt, log

from mcts0 import TreeNode0, Mcts0


class TreeNode1(TreeNode0):
    def __init__(self, game, player: int, move=None, parent=None):
        super().__init__(game, player, move, parent)

        self.results = 0  # +1 for black win, -1 for white win

    def expand_node(self):
        """Generate children of this mode."""

        for move in self.moves:
            game_copy = self.game.copy()
            game_copy.play_move(move, self.player)
            won = game_copy.check_win(move)
            self.children.append(
                TreeNode1(game_copy, 3-self.player, move, self)
            )

            if won:
                self.children[-1].backpropagate(float('inf'))

        self.is_leaf = False

    def backpropagate(self, result: int):
        """Backpropagate simulation results."""

        node = self
        while node is not None:
            node.sims += 1

            if result == float('inf') and node != self:
                for children in node.children:
                    if children.results != float('-inf'):
                        result = 1
                        break
            elif result == float('inf') and node.parent is None:
                return node.move

            node.results += result

            if result == float('inf') or result == float('-inf'):
                result *= -1
            else:
                result = 1-result

            node = node.parent


class RootNode1(TreeNode1):
    def expand_node(self):
        """
        Generate children of this node.

        Returns:
        winning move, if one is found
        """

        for move in self.moves:
            game_copy = self.game.copy()
            game_copy.play_move(move, self.player)
            won = game_copy.check_win(move)

            if won:
                return move

            self.children.append(
                TreeNode1(game_copy, 3-self.player, move, self)
            )

        self.is_leaf = False
        return None


class Mcts1(Mcts0):
    # MCTS code largely taken from
    # https://www.geeksforgeeks.org/ml-monte-carlo-tree-search-mcts/
    # November 27, 2022

    def __init__(self, game, player):
        self.root_node = RootNode1(game, player)
        self.winning_move = self.root_node.expand_node()

        self.c = 0.3  # used for UCT

    def get_best_move(self):
        """
        Get most simulated move.

        Returns:
        move: most simulated move
        """

        best_node = None
        most_visits = None
        for node in self.root_node.children:
            if node.results == float('-inf'):
                continue

            if most_visits is None or node.sims > most_visits:
                best_node = node
                most_visits = node.sims

        if best_node is None:
            # all moves are losing, choose the one with the most visits
            for node in self.root_node.children:
                if most_visits is None or node.sims > most_visits:
                    best_node = node
                    most_visits = node.sims

        return best_node.move

    def monte_carlo_tree_search(self):
        """
        Perform Monte Carlo Tree Search.

        Returns:
            best_move: most visited move
        """

        if self.winning_move is not None:
            print("number of simulations performed:", self.root_node.sims)
            return self.winning_move

        # return move after set amount of time
        end_time = time.time() + 15

        while time.time() < end_time:
            leaf = self.traverse_and_expand(self.root_node)  # traverse
            result = leaf.rollout()  # rollout
            leaf.backpropagate(result)  # backpropagate

        """
        for child in self.root_node.children:
            print(child.move, child.sims, child.results)
        """
        return self.get_best_move()

    def best_uct(self, node: TreeNode1) -> TreeNode1:
        """
        Return the next move for traversal.

        If node is a root, return node.
        If there is a child of node that has not been simulated, return child.
        Otherwise, return child with best uct score.

        Arguments:
        node (TreeNode): Node in tree to find child to traverse for

        Returns:
        TreeNode: child to traverse
        """

        if len(node.moves) == 0:
            return node  # if terminal node, return node

        best_uct = None
        best_child = None

        for child in node.children:
            if child.sims == 0:
                # if the children of the node have not been
                # fully explored, then explore a move that
                # hasn't been before
                return child

            # calculate UCT, update if best
            mean_res = child.results / child.sims
            uct = mean_res+(self.c*sqrt(log(self.root_node.sims)/child.sims))
            if best_uct is None or uct > best_uct:
                best_uct = uct
                best_child = child

        # return best uct
        return best_child
