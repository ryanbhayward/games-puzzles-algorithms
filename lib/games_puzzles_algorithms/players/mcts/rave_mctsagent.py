from __future__ import division
from .mcts_agent import *
from games_puzzles_algorithms.games.dex.game_state import COLORS


class rave_node(node):
	def __init__(self, move = None, parent = None):
		"""
		Initialize a new node with optional move and parent and initially empty
		children list and rollout statistics and unspecified outcome.
		"""
		self.move = move
		self.parent = parent
		self.N = 0 #times this position was visited
		self.Q = 0 #average reward (wins-losses) from this position
		self.Q_RAVE = 0 # times this move has been critical in a rollout
		self.N_RAVE = 0 # times this move has appeared in a rollout
		self.children = {}
		self.outcome = COLORS["none"]

	def value(self, explore, crit):
		"""
		Calculate the UCT value of this node relative to its parent, the parameter
		"explore" specifies how much the value should favor nodes that have
		yet to be thoroughly explored versus nodes that seem to have a high win
		rate.
		Currently explore is set to zero when choosing the best move to play so
		that the move with the highest winrate is always chossen. When searching
		explore is set to EXPLORATION specified above.
		"""
		#unless explore is set to zero, maximally favor unexplored nodes
		if (self.N == 0 or self.N_RAVE == 0):
			if(explore == 0):
				return 0
			else:
				return inf
		else:
			#rave valuation:
			alpha = max(0,(crit - self.N)/crit)
			return self.Q*(1-alpha)/self.N+self.Q_RAVE*alpha/self.N_RAVE

	def child_nodes(self):
		return list(self.children.values())


class rave_mctsagent(mctsagent):
	RAVE_CONSTANT = 300

	def root_node(self):
		return rave_node()

	def new_node(self, move, parent):
		return rave_node(move, parent)

	def node_value(self, n):
		return n.value(self.EXPLORATION, self.RAVE_CONSTANT)

	def backup(self, node, turn, outcome, black_rave_pts, white_rave_pts):
		"""
		Update the node statistics on the path from the passed node to root to reflect
		the outcome of a randomly simulated playout.
		"""
		my_reward = self.reward(turn, outcome)

		while node!=None:
			if turn == COLORS["white"]:
				for point in white_rave_pts:
					if point in node.children:
						node.children[point].Q_RAVE+=-my_reward
						node.children[point].N_RAVE+=1
			else:
				for point in black_rave_pts:
					if point in node.children:
						node.children[point].Q_RAVE+=-my_reward
						node.children[point].N_RAVE+=1

			node.N += 1
			node.Q +=my_reward
			if turn == COLORS["black"]:
				turn = COLORS["white"]
			else:
				turn = COLORS["black"]
			my_reward = -my_reward
			node = node.parent

	def expand(self, parent, state):
		"""
		Generate the children of the passed "parent" node based on the available
		moves in the passed game_state and add them to the tree.
		"""
		if(state.winner() != COLORS["none"]):
		#game is over at this node so nothing to expand
			return False

		for move in state.moves():
			child = rave_node(move, parent)
			parent.children[child.move] = child

		return True

	def roll_out(self, state):
		"""Simulate a random game except that we play all known critical
		cells first, return the winning player and record critical cells at the end."""
		moves = state.moves()
		while(state.winner() == COLORS["none"]):
			random.shuffle(moves)
			state.play(moves.pop())

		black_rave_pts = []
		white_rave_pts = []

		for y, x in state.every_cell():
			if state.color(self.rootstate.turn(), y, x) == COLORS["black"]:
				black_rave_pts.append((x,y))
			elif state.color(self.rootstate.turn(), y, x) == COLORS["white"]:
				white_rave_pts.append((x,y))

		return state.winner(), black_rave_pts, white_rave_pts
