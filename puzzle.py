import sys
import numpy as np


class Node:
	def __init__(self, state, parent, action):
		self.state = state
		self.parent = parent
		self.action = action


class Stack:
	def __init__(self):
		self.items = []

	def add(self, node):
		self.items.append(node)

	def contains_state(self, state):
		return any((node.state[0] == state[0]).all() for node in self.items)
	
	def empty(self):
		return len(self.items) == 0
	
	def remove(self):
		if self.empty():
			raise Exception("Empty items")
		else:
			node = self.items[-1]
			self.items = self.items[:-1]
			return node


class Queue(Stack):
	def remove(self):
		if self.empty():
			raise Exception("Empty items")
		else:
			node = self.items[0]
			self.items = self.items[1:]
			return node


class Puzzle:
	def __init__(self, start, startIndex, goal, goalIndex):
		self.start = [start, startIndex]
		self.goal = [goal, goalIndex] 
		self.solution = None

	def neighbors(self, state):
		mat, (row, col) = state
		results = []
		
		if row > 0:
			mat1 = np.copy(mat)
			mat1[row][col] = mat1[row - 1][col]
			mat1[row - 1][col] = 0
			results.append(('UP', [mat1, (row - 1, col)]))
		if col > 0:
			mat1 = np.copy(mat)
			mat1[row][col] = mat1[row][col - 1]
			mat1[row][col - 1] = 0
			results.append(('LEFT', [mat1, (row, col - 1)]))
		if row < 2:
			mat1 = np.copy(mat)
			mat1[row][col] = mat1[row + 1][col]
			mat1[row + 1][col] = 0
			results.append(('DOWN', [mat1, (row + 1, col)]))
		if col < 2:
			mat1 = np.copy(mat)
			mat1[row][col] = mat1[row][col + 1]
			mat1[row][col + 1] = 0
			results.append(('RIGHT', [mat1, (row, col + 1)]))

		return results

	def print(self):
		solution = self.solution if self.solution is not None else None
		print("Current board layout:\n ")
		count = 0
		result_list = []
		for action, cell in zip(solution[0], solution[1]):
			if count == 0:
				print("FIRST, from here, move: ", action, "\n", cell[0])
				count += 1
			elif count == 1:
				print("SECOND, from here, move: ", action, "\n", cell[0])
				count += 1
			elif count == 2:
				print("THIRD, from here, move: ", action, "\n", cell[0])
				count += 1
			elif count == 3:
				print("NEXT, from here, move: ", action, "\n", cell[0])
				count += 1
			else:
				print("THEN, from here, move: ", action, "\n", cell[0])
			result_list.append(action[0])
		print("Done")
		print("Final result: ", " ".join(t for t in result_list))

	def does_not_contain_state(self, state):
		for st in self.explored:
			if (st[0] == state[0]).all():
				return False
		return True
	
	def solve(self):
		self.num_explored = 0

		start = Node(state=self.start, parent=None, action=None)
		items = Queue()
		items.add(start)

		self.explored = [] 

		while True:
			if items.empty():
				raise Exception("No solution")

			node = items.remove()
			self.num_explored += 1

			if (node.state[0] == self.goal[0]).all():
				actions = []
				cells = []
				while node.parent is not None:
					actions.append(node.action)
					cells.append(node.state)
					node = node.parent
				actions.reverse()
				cells.reverse()
				self.solution = (actions,  cells)
				return

			self.explored.append(node.state)

			for action, state in self.neighbors(node.state):
				if not items.contains_state(state) and self.does_not_contain_state(state):
					child = Node(state=state, parent=node, action=action)
					items.add(child)


start = np.array([[1, 3, 4], [8, 0, 5], [7, 2, 6]])
goal = np.array([[1, 2, 3], [8, 0, 4], [7, 6, 5]])


startIndex = (1, 1)
goalIndex = (1, 0)


p = Puzzle(start, startIndex, goal, goalIndex)
p.solve()
p.print()