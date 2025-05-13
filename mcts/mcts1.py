# by Luke Schultz fall 22, w 23, spr 23, smr 23, f 23
#  * written with help of GitHub Copilot
#  *  MCTS code largely from
#       https://www.geeksforgeeks.org/ml-monte-carlo-tree-search-mcts/
#  rbh 2024: show data from initial VERBOSE_SIMS simulations
#    - every rollout is a simulation
#    - every win discovered after a node expansion is a simulation
#      so the number of simulations is >= number of mcts iterations
#  rbh 2025: 
#    - don't rollout from proven loss leaf
#    - result = 1 - result (works also for infinity)

import time
from math import sqrt, log

#from hex_game0 import BLACK, WHITE
from mcts0 import TreeNode0, Mcts0, VERBOSE_SIMS, MCTS_TIME, \
  root_node_sims, path_from_root, compress

def int_or_inf(results): # int or +-infinity
    if results == float('inf'):  return '  inf'
    if results == float('-inf'): return ' -inf'
    return '{:5d}'.format(results)

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
            t = TreeNode1(game_copy, 3-self.player, move, self)
            rs = root_node_sims(self)
            if rs < VERBOSE_SIMS:
                print('\n    xpnd_nd', path_from_root(self), '>', t.move, end='')
            self.children.append(t)

            if won:
                if rs < VERBOSE_SIMS:
                    print('\n  won sim', '{:1d}.'.format(rs+1), \
                      path_from_root(self), '{:1d}'.format(move), 'win,', end='')
                self.children[-1].backpropagate(float('inf'))
                if rs < VERBOSE_SIMS: print(' no more sibs')
                break # winner found, no need to add rest of children

        self.is_leaf = False

    def backpropagate(self, result: int):
        """Backpropagate simulation results."""

        #print('  backprop', path_from_root(self), 'result', result)
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

            # negate (works also for +/- infinity)
            result = 1 - result

            #if result == float('inf') or result == float('-inf'):
            #    result *= -1
            #else:
            #    result = 1 - result

            node = node.parent

class RootNode1(TreeNode1):
    def show_data(self):
        print('\n  move  sims  wins')
        for child in self.children:
            print('{:5d}'.format(child.move), 
                  '{:5d}'.format(child.sims), 
                  int_or_inf(child.results))
        print('total', '{:5d}'.format(self.sims), 
                  int_or_inf(-self.results))

    def expand_node(self):
        """
        Generate children of this node.

        Returns:
        winning move, if one is found
        """

        print('* > ', end='')
        for move in self.moves:
            game_copy = self.game.copy()
            game_copy.play_move(move, self.player)
            won = game_copy.check_win(move)
            if won:
                print(move, '  win !!!')
                return move
            t = TreeNode1(game_copy, 3-self.player, move, self)
            print(t.move, ', ', sep='', end='')
            self.children.append(t)
        self.is_leaf = False
        return None

class Mcts1(Mcts0):
    # november 27 2022... MCTS code largely taken from
    # https://www.geeksforgeeks.org/ml-monte-carlo-tree-search-mcts/
    def __init__(self, game, player):
        #print('\nroot node init ', end='')
        self.root_node = RootNode1(game, player)
        self.winning_move = self.root_node.expand_node()
        self.c = 0.3  # used for UCT
        #print('done')

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

    def end_msg(self, start_time, msg):
        print('\ndone  ' + msg, '{:.1f}'.format(time.time()-start_time), 'sec')
        #self.root_node.show_data()

    def monte_carlo_tree_search(self):
        """
        Perform Monte Carlo Tree Search.

        Returns:
            best_move: most visited move
        """

        if self.winning_move is not None:
            return self.winning_move

        # return move after set amount of time
        end_time = time.time() + MCTS_TIME
        start_time = time.time()


        while time.time() < end_time:

            max_sims = float('-inf')
            for child in self.root_node.children:
                # return if some child is true win 
                if child.results == float('inf'):
                    #self.root_node.show_data()
                    #print('{:.1f}'.format(time.time()-start_time), 'sec')
                    self.end_msg(start_time, 'proven win')
                    return child.move
                max_sims = max(max_sims, child.results)
            # return if all children are true loss
            if max_sims == float('-inf'):
                self.end_msg(start_time, 'proven loss')
                return self.get_best_move()
                
            rs = self.root_node.sims
            if rs < VERBOSE_SIMS:
                print('\n  trv_xpnd ', end='')
            leaf = self.traverse_and_expand(self.root_node)  # traverse
            #if rs < VERBOSE_SIMS:
            #    print('\n  trv_xpnd leaf ', path_from_root(leaf), end='')
            if leaf.results != float('inf'):
              result = leaf.rollout()  # rollout
              leaf.backpropagate(result)  # backpropagate

        self.end_msg(start_time, 'not proven')
        return self.get_best_move()

    def best_uct(self, node: TreeNode1) -> TreeNode1:
        """
        Return the next move for traversal.

        If node is root, return node.
        If node has unsimulated child, return child.
        Otherwise, return child with best uct score.

        Arguments:
        node (TreeNode): Node in tree to find child to traverse for

        Returns:
        TreeNode: child to traverse
        """

        # for hex, each board-filling move is a winner
        # so this test never passes
        if len(node.moves) == 0: 
            return node  # terminal so return

        best_uct = None
        best_child = None

        rs = root_node_sims(node)
        if rs < VERBOSE_SIMS: 
            print('bu', '*' if node.move == None else node.move, end=' ')
        for child in node.children:
            if child.sims == 0: # unexplored children have priority
                if rs < VERBOSE_SIMS: 
                    print(child.move, 'no-sims child', end=' ')
                return child

            # calculate UCT, update if best
            mean_res = child.results / child.sims
            uct = mean_res+(self.c*sqrt(log(self.root_node.sims)/child.sims))
            if rs < VERBOSE_SIMS:
                print(compress('{:.1f}'.format(uct)), end=' ')
            #uct = mean_res+(self.c*(self.root_node.sims/(child.sims+self.root_node.sims)))
            if best_uct is None or uct > best_uct:
                best_uct, best_child = uct, child
          
        rs = root_node_sims(best_child)
        if rs < VERBOSE_SIMS:
            print(best_child.move, end=' ')
        return best_child
