# Created by Luke Schultz
# Fall 2022, Winter 2023, Spring 2023, Summer 2023, Fall 2023
# Written with the help of GitHub Copilot

import time
import random
from math import sqrt, log


class TreeNode0:
    def __init__(self, game, player: int, move=None, parent=None):
        self.game = game      # Hex object
        self.player = player  # Player to make move
        self.move = move      # Previous move
        self.parent = parent  # Parent node, None if root

        self.wins = 0  # Number of winning simulations
        self.sims = 0  # Number of simulations

        self.is_leaf = True  # False is node has been expanded
        self.children = []   # List of child nodes

        # Legal moves from this position
        self.moves = self.game.get_legal_moves()

    def expand_node(self):
        """Generate children of this node."""

        for move in self.moves:
            game_copy = self.game.copy()
            game_copy.play_move(move, self.player)
            self.children.append(
                TreeNode0(game_copy, 3-self.player, move, self)
            )

        self.is_leaf = False

    def backpropagate(self, won: bool):
        """Backpropagate simulation results."""

        node = self
        while node is not None:
            node.sims += 1

            if won:
                node.wins += 1
            won = not won

            node = node.parent

    def rollout(self) -> bool:
        """
        Perform a simulation.
        Selects moves uniformly random.

        Returns:
        bool: True if parent player won
        """

        game_copy = self.game.copy()
        player = self.player
        moves = game_copy.get_legal_moves()
        while len(moves) > 0:
            move_index = random.randint(0, len(moves)-1)  # Select random move
            game_copy.play_move(moves[move_index], player)
            won = game_copy.check_win(moves[move_index])

            if won:
                break

            moves[move_index] = moves[-1]
            moves.pop()
            player = 3 - player  # invert color / switch player

        if player != self.player:  # parent player won
            return True
        else:  # parent player lost
            return False


class RootNode0(TreeNode0):
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
                TreeNode0(game_copy, 3-self.player, move, self)
            )

        self.generated_children = True
        return None


class Mcts0:
    # MCTS code largely taken from
    # https://www.geeksforgeeks.org/ml-monte-carlo-tree-search-mcts/
    # November 27, 2022

    def __init__(self, game, player):
        self.root_node = RootNode0(game, player)
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
            won = leaf.rollout()  # rollout
            leaf.backpropagate(won)  # backpropagate

        return self.get_best_move()

    def best_uct(self, node: TreeNode0) -> TreeNode0:
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
            mean_wins = child.wins / child.sims
            uct = mean_wins+(self.c*sqrt(log(self.root_node.sims)/child.sims))
            if best_uct is None or uct > best_uct:
                best_uct = uct
                best_child = child

        # return best uct
        return best_child

    def traverse_and_expand(self, node: TreeNode0):
        """
        Traverse tree and find node to simulate.

        Arguments:
        node (TreeNode): Root (first move) of tree

        Returns:
        Node (TreeNode): move to run simulation on
        """

        while not node.is_leaf:
            node = self.best_uct(node)

        if len(node.moves) > 0 and node.sims > 0:
            node.expand_node()
            node = random.choice(node.children)

        return node
