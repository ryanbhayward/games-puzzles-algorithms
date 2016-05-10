from __future__ import division
from games_puzzles_algorithms.game.dex.game_state import GameState
from games_puzzles_algorithms.game.dex.game_state import color_to_player
from games_puzzles_algorithms.game.dex.game_state import player_to_color
from games_puzzles_algorithms.game.dex.game_state import next_player
from games_puzzles_algorithms.game.dex.game_state import COLORS
from games_puzzles_algorithms.choose import choose_legal_action_uniformly_randomly
import time
import random
import math
from math import sqrt, log
from copy import copy, deepcopy
from sys import stderr
from queue import Queue
inf = float('inf')


class TimeIsUp(Exception):
    pass


class node:
	"""
	Node for the MCST. Stores the move applied to reach this node from its parent,
	stats for the associated game position, children, parent and outcome
	(outcome==none unless the position ends the game).
	"""

	def __init__(self, move=None, parent=None):
		"""
		Initialize a new node with optional move and parent and initially empty
		children list and rollout statistics and unspecified outcome.
		"""
		self.move = move
		self.parent = parent
		self.N = 0  # times this position was visited
		self.Q = 0  # average reward (wins-losses) from this position
		self.children = []
		self.outcome = COLORS["none"]

	def set_outcome(self, outcome):
		"""
		Set the outcome of this node (i.e. if we decide the node is the end of
		the game)
		"""
		self.outcome = outcome

	def value(self, explore):
		"""
		Calculate the UCT value of this node relative to its parent, the parameter
		"explore" specifies how much the value should favor nodes that have
		yet to be thoroughly explored versus nodes that seem to have a high win
		rate.
		Currently explore is set to zero when choosing the best move to play so
		that the move with the highest winrate is always chossen. When searching
		explore is set to EXPLORATION specified above.
		"""
		# unless explore is set to zero, maximally favor unexplored nodes
		if(self.N == 0):
			if(explore == 0):
				return 0
			else:
				return inf
		else:
			return self.Q / self.N + explore * sqrt(2 * log(self.parent.N) / self.N)

	def lcb(self, explore):
		"""
		Calculate the UCT value of this node relative to its parent, the parameter
		"explore" specifies how much the value should favor nodes that have
		yet to be thoroughly explored versus nodes that seem to have a high win
		rate.
		Currently explore is set to zero when choosing the best move to play so
		that the move with the highest winrate is always chossen. When searching
		explore is set to EXPLORATION specified above.
		"""
		# unless explore is set to zero, maximally favor unexplored nodes
		if(self.N == 0):
			return 0
		else:
			return math.exp(
				self.Q / self.N - explore * sqrt(2 * log(self.parent.N) / self.N)
			)

	def child_nodes(self):
		return self.children


class MctsAgent:
	"""
	Basic no frills implementation of an agent that preforms MCTS for hex.
	"""
	EXPLORATION = 1

	def __init__(self, state=GameState.root(8)):
		self.rootstate = deepcopy(state)
		self.root = self.root_node()
		self.previous_children = self.root.child_nodes()

	def root_node(self):
		return node()

	def new_node(self, move, parent):
		return node(move, parent)

	def distribution(self, exclude=-1):
		d = {}
		s = 0
		if self.root.child_nodes():
			self.previous_children = self.root.child_nodes()
		my_child_nodes = copy(self.previous_children)
		for i in range(len(my_child_nodes)):
			n = my_child_nodes[i]
			index = self.rootstate.cell_index(*n.move)
			if exclude == index:
				self.previous_children.pop(i)
			else:
				d[index] = n.N ** 5
				s += d[index]
				# print("index: {}, d[index]: {}, s: {}, N: {}, Q: {}".format(
				# index, d[index], s, n.N, n.Q))
		# print(d)
		if s > 0:
			for k in d.keys():
				d[k] = d[k] / float(s)
		else:
			for n in self.previous_children:
				index = self.rootstate.cell_index(*n.move)
				d[index] = 1.0 / len(my_child_nodes)
		# move_list = [
		# 	((self.rootstate.column(c), self.rootstate.row(c)), value) for c, value in d.items()]
		# move_list.sort(key=lambda n: n[1])
		# print(move_list)
		return d

	def sorted_moves(self):
		"""
		Return a list of all moves sorted by quality.
		"""
		if(self.rootstate.winner() != game_state.PLAYERS["none"]):
			return game_state.GAMEOVER
		move_list = copy(self.root.child_nodes())
		move_list.sort(key = lambda n: n.N)
		return [self.rootstate.cell_index(*child.move) for child in move_list]

	def best_move(self):
		"""
		Return the best move according to the current tree.
		"""
		if(self.rootstate.winner() != COLORS["none"]):
			return game_state.GAMEOVER

		# choose the move of the most simulated node breaking ties randomly
		max_value = max(self.root.children, key = lambda n: n.N).N
		max_nodes = [n for n in self.root.children if n.N == max_value]
		bestchild = random.choice(max_nodes)
		return bestchild.move

	def move(self, move, player):
		"""
		Make the passed move and update the tree approriately.
		"""
		if self.root.child_nodes():
			self.previous_children = self.root.child_nodes()
		my_player = self.rootstate.player_to_act()
		self.rootstate.place(move, player)
		self.root = self.root_node()
		self.rootstate.set_player_to_act(my_player)

	def search(self, time_budget):
		"""
		Search and update the search tree for a specified amount of time in seconds.
		"""
		self.start_time = time.clock()
		num_rollouts = 0
		self.time_budget = time_budget - 0.4

		# do until we exceed our time budget
		while True:
			try:
				node, state = self.select_node()
				turn = state.player_to_act()
				self.backup(node, turn, *self.roll_out(state))
				num_rollouts += 1
			except TimeIsUp:
				break

		stderr.write("Ran "+str(num_rollouts)+ " rollouts in " +\
			str(time.clock() - self.start_time)+" sec\n")
		stderr.write("Node count: "+str(self.tree_size())+"\n")

	def fill_opponent_stones(self):
		state = deepcopy(self.rootstate)
		potential_moves = []
		num_opponent_stones_to_place = 0
		for y,x in state.every_cell():
			cell = (y, x)
			if state[cell] == COLORS['none']:
				potential_moves.append(cell)
			elif state[cell] == player_to_color(state.player_to_act()):
				num_opponent_stones_to_place += 1
			else:
				num_opponent_stones_to_place -= 1

		if potential_moves and num_opponent_stones_to_place > 0:
			random.shuffle(potential_moves)
			opponent = next_player(state.player_to_act())
			played_moves = []
			while (
				potential_moves and
				num_opponent_stones_to_place > 0
			):
				if not self.time_available():
					raise TimeIsUp()
				move_to_play = potential_moves.pop()
				state.place(move_to_play, opponent)
				if state.winner() != COLORS['none']:
					while played_moves:
						potential_moves.append(played_moves.pop())
						num_opponent_stones_to_place += 1
					state = deepcopy(self.rootstate)
				else:
					played_moves.append(move_to_play)
					num_opponent_stones_to_place -= 1
		return state

	def time_available(self):
		return time.clock() - self.start_time < self.time_budget

	def node_value(self, n):
		return n.value(self.EXPLORATION)

	def node_lcb_value(self, n):
		return n.lcb(self.EXPLORATION)

	def select_node(self, do_fill_opponent_stones=True):
		"""
		Select a node in the tree to preform a single simulation from.
		"""
		node = self.root
		state = self.fill_opponent_stones() if do_fill_opponent_stones else deepcopy(self.rootstate)

		# stop if we find reach a leaf node
		my_child_nodes = copy(node.child_nodes()) if do_fill_opponent_stones else node.child_nodes()
		while my_child_nodes:
			if not self.time_available():
				raise TimeIsUp()
			if do_fill_opponent_stones:
				my_child_nodes.sort(key = lambda n: self.node_value(n))
				new_node = my_child_nodes.pop()
				while state[new_node.move] != COLORS['none']:
					if not my_child_nodes:
						return (node, state)
					else:
						new_node = my_child_nodes.pop()
				node = new_node
			else:
				max_value = self.node_value(
					max(
						my_child_nodes,
						key = lambda n: self.node_value(n)
					)
				)
				max_nodes = [n for n in my_child_nodes if self.node_value(n) == max_value]
				node = random.choice(max_nodes)
			state.play(node.move)

			# if some child node has not been explored select it before expanding
			# other children
			if node.N == 0:
				return (node, state)
			else:
				my_child_nodes = copy(node.child_nodes()) if do_fill_opponent_stones else node.child_nodes()

		# If we reach a leaf node generate its children and return one of them
		if self.expand(node, state):
			node = random.choice(node.child_nodes())
			state.play(node.move)
		return (node, state)

	def roll_out(self, state):
		"""
		Simulate an entirely random game from the passed state and return the winning
		player.
		"""
		moves = state.moves()
		random.shuffle(moves)
		while(state.winner() == COLORS["none"]):
			state.play(moves.pop())
		return (state.winner(),)

	def reward(self, turn, outcome):
		''' note that reward is calculated for player who just played
		at the node and not the next player to play'''
		return -1 if outcome == turn else 1

	def backup(self, node, turn, outcome):
		"""
		Update the node statistics on the path from the passed node to root to reflect
		the outcome of a randomly simulated playout.
		"""
		my_reward = self.reward(turn, outcome)

		while node is not None:
			node.N += 1
			node.Q += my_reward
			my_reward = -my_reward
			node = node.parent

	def expand(self, parent, state):
		"""
		Generate the children of the passed "parent" node based on the available
		moves in the passed game_state and add them to the tree.
		"""
		if (state.winner() != COLORS["none"]):
			return False

		for move in state.moves():
			assert(state[move] == COLORS['none'])
			parent.children.append(node(move, parent))

		return True

	def set_game_state(self, state):
		"""
		Set the rootstate of the tree to the passed game_state, this clears all
		the information stored in the tree since none of it applies to the new
		state.
		"""
		self.rootstate = deepcopy(state)
		self.root = self.root_node()

	def tree_size(self):
		"""
		Count nodes in tree by BFS.
		"""
		Q = Queue()
		count = 0
		Q.put(self.root)
		while not Q.empty():
			node = Q.get()
			count +=1
			for child in node.child_nodes():
				Q.put(child)
		return count
