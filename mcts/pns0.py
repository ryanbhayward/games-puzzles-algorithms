# Created by Luke Schultz
# Fall 2022, Winter 2023, Spring 2023, Summer 2023, Fall 2023
# Written with the help of GitHub Copilot


import time
import random
from math import sqrt, log

OR = 1
AND = 2

class TreeNode:
    def __init__(self, game, player: int, move=None, parent=None, node_type=OR):
        self.game = game            # Hex object
        self.player = player        # Player to make move
        self.move = move            # Previous move
        self.parent = parent        # Parent node, None if root
        self.node_type = node_type  # Either AND or OR

        self.pn = 1  # Proof number, initialized to one
        self.dn = 1  # Disproof number, initialized to one

        if self.game._check_win():
            if self.node_type == OR:
                self.pn = float('inf')
                self.dn = 0
            else:
                self.pn = 0
                self.dn = float('inf')

        self.generated_children = False  # True if node has been expanded
        self.children = []               # List of child nodes

        # Legal moves from this position
        self.moves = self.game.get_legal_moves()

    def generate_children(self):
        """Generate children of this mode."""

        for move in self.moves:
            game_copy = self.game.copy()
            game_copy.play_move(move, self.player)
            self.children.append(
                TreeNode(game_copy, 3-self.player, move,
                         self, 3-self.node_type)
            )

        self.generated_children = True

class PNS:

    def __init__(self, game, player):
        self.root_node = TreeNode(game, player)

    def pns(self):
        while self.root_node.pn != 0 and self.root_node.dn != 0:
            child = self.select_child()
            child.generate_children()
            self.backpropagate(child)
        print(self.root_node.pn, self.root_node.dn)

    def select_child(self):
        current_node = self.root_node

        while current_node.generated_children:
            if current_node.generated_children == False:
                return current_node

            best_child = None
            if current_node.node_type == OR:
                lowest_pn = float('inf')

                for child in current_node.children:
                    if child.pn < lowest_pn:
                        lowest_pn = child.pn
                        best_child = child
            elif current_node.node_type == AND:
                lowest_dn = float('inf')

                for child in current_node.children:
                    if child.dn < lowest_dn:
                        lowest_dn = child.dn
                        best_child = child
            
            current_node = best_child
        
        return current_node

    def backpropagate(self, child):
        current_node = child.parent

        while current_node != None:
            if current_node.node_type == OR:
                current_node.dn = 0
                current_node.pn = float('inf')
                for child in current_node.children:
                    if child.pn < current_node.pn:
                        current_node.pn = child.pn
                    current_node.dn += child.dn
            else:
                current_node.dn = float('inf')
                current_node.pn = 0
                for child in current_node.children:
                    if child.dn < current_node.dn:
                        current_node.dn = child.dn
                    current_node.pn += child.pn
            
            current_node = current_node.parent
