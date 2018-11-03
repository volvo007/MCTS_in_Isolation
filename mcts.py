# Monte Carlo Tree Search for Isolation

import random, math, copy

# Define a MCTS Node class
# This class shold work like a tree: 
# containing node finding, node adding
# otherwise, the visiting times, reward score and whether the sub_node is fully explored
class Node_MCTS():
	def __init__(self, state, parent=None):
		self.visits = 0
		self.reward = 0.0
		self.state = state
		self.children = []
		self.children_actions = []
		self.parent = parent

	def add_child(self, child_state, action):
		# Use recursion here that the 'parent' of this 'child node' is the node defined in '__init__' function
		child = Node_MCTS(child_state, self)
		self.children.append(child)
		self.children_actions.append(action)

	def update(self, reward):
		self.reward += reward
		self.visits += 1

	def all_explored(self):
		# state.actions() defined in 'isolation.py'. no need to achieve this by ourselves
		return len(self.children_actions) == len(self.state.actions())

# a MCTS algorithem contains 4 steps:
# selection, expansion, simulation and backpropagation

# firstly, achieve selection and expansion
def tree_policy(node):
	# the funtion to judge whether the game is over - is defined in isolation.py
	# if the game is over, return the best score node
	# else, look for nodes which were not searched and keep going
	while not node.state.terminal_test():
		if node.all_explored():
			return best_child(node)
		else:
			return expand(node)

def expand(node):
	tried_actions = node.children_actions
	free_actions = node.state.actions()
	for action in free_actions:
		if action not in tried_actions:
		""" Return the resulting game state after applying the action specified
        to the current game state.

        Note that players can choose any open cell on the opening move,
        but all later moves MUST be one of the values in Actions.

        Parameters
        ----------
        action : int
            An index indicating the next position for the active player

        Returns
        -------
        Isolation
            A new state object with the input move applied.
        """
			new_state = node.state.result(action) # defined in isolation.py
			node.add_child(new_state, action)
			return node.children[-1]

C = 1/sqrt(2) # an experienced factor

def best_child(node):
	# find the child node with best score
	# return node
	best_score = float("-inf")
	best_children = []
	for child in node.children:
		score = child.reward/child.visits + math.sqrt(2*math.log(node.visits)/child.visits)
		if score == best_score:
			best_children.append(child)
		elif score > best_score:
			best_children = [child]
			best_score = score
	return random.choice(best_children)

# secondely, achieve a quick simulation method
def default_policy(node):
	# this function will randomly choose an action and return the reward under this new state
	# while the game is not over, keep going forward to "deep" status of the game
	# because the borad is not very large, this will accomplish in a very short time
	# if the agent wins the game, reward = 1; else reward = -1
	current_state = node.state
	while not current_state.terminal_test():
		action = random.choice(current_state.actions())
		state = state.result(action)
	return -1 if state._has_liberties(temp_state.player()) else 1

# finally, the backpropagation
def backpropagation(node, reward):
	while node != None:
		node.update(reward)
		node = node.parent
		reward *= -1