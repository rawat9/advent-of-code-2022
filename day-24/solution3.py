from queue import PriorityQueue
from collections import namedtuple, Counter
import numpy as np
from pprint import pprint

def get_input(path: str):
    with open(path, mode="r") as file:
        data = [list(i) for i in file.read().splitlines()]
    return data

class Blizzard:
	def __init__(self, map: list[list[str]]) -> None:
		self.map = map
		self.row_length = len(self.map)
		self.col_length = len(self.map[0])
		self.directions = {'>': (0, 1), '<': (0, -1), '^': (-1, 0), 'v': (1, 0)}
		self.positions = {}
		self.initialise_positions()

		self.expedition_start = (0, 1)
		self.expedition_destination = (self.row_length-1, self.col_length-2)
		self.expedition_movements = [(0,1), (0,-1), (-1,0), (1,0)]
		self.expedition_current_loc = self.expedition_start
		self.expedition = [self.expedition_start]

	def is_blizzard(self, pos):
		return self.map[pos[0]][pos[1]] in self.directions.keys()

	def is_wall(self, pos) -> bool:
		return self.map[pos[0]][pos[1]] == '#'

	def filter_by_direction(self, direction):
		return dict(filter(lambda x: x[0][0] == direction, self.positions.items()))

	def move_left(self, pos):
		current_pos = self.positions[('<', pos)][-1]

		x, y = current_pos
		dx, dy = self.directions['<']
		target = (x+dx, y+dy)

		if self.is_wall(target):
			self.positions[('<', pos)].append((x, self.col_length-2))
			return
		else:
			self.positions[('<', pos)].append(target)

	def move_up(self, pos):
		current_pos = self.positions[('^', pos)][-1]

		x, y = current_pos
		dx, dy = self.directions['^']
		target = (x+dx, y+dy)

		if self.is_wall(target):
			self.positions[('^', pos)].append((self.row_length-2, y))
			return
		else:
			self.positions[('^', pos)].append(target)

	def move_down(self, pos):
		current_pos = self.positions[('v', pos)][-1]

		x, y = current_pos
		dx, dy = self.directions['v']
		target = (x+dx, y+dy)

		if self.is_wall(target):
			self.positions[('v', pos)].append((1, y))
			return
		else:
			self.positions[('v', pos)].append(target)

	def move_right(self, pos):
		current_pos = self.positions[('>', pos)][-1]

		x, y = current_pos
		dx, dy = self.directions['>']
		target = (x+dx, y+dy)

		if self.is_wall(target):
			self.positions[('>', pos)].append((x, 1))
			return
		else:
			self.positions[('>', pos)].append(target)

	def initialise_positions(self):
		Blizzard = namedtuple('Blizzard', ['value', 'origin'])
		np_map = np.array(self.map)
		original_positions = np.where((np_map == '>') | (np_map == 'v') | (np_map == '^') | (np_map == '<'))
		for r, c in zip(original_positions[0], original_positions[1]):
			value = self.map[r][c]
			self.positions[Blizzard(value, (r,c))] = [(r, c)]

	def traverse(self):
		for value, origin in self.positions.keys():
			match value:
				case '>':
					self.move_right(origin)
				case '<':
					self.move_left(origin)
				case 'v':
					self.move_down(origin)
				case '^':
					self.move_up(origin)

	def trace(self):
		current_pos = list(map(lambda x: (x[0].value, x[1][-1]), self.positions.items()))
		c = Counter(list(map(lambda x: x[1], current_pos)))
		
		for value, pos in current_pos:
			count = c[pos]
			x, y = pos

			if count > 1:
				self.map[x][y] = str(count)
			else:
				self.map[x][y] = value

	def trace_expedition(self):
		e_x, e_y = self.expedition[-1]
		self.map[e_x][e_y] = 'E'

	def clear_expedition(self):
		e_x, e_y = self.expedition_start
		self.map[e_x][e_y] = '.'

	def clear(self):
		for i in range(1, self.row_length-1):
			for j in range(1, self.col_length-1):
				self.map[i][j] = '.' 

	def is_ground(self, pos):
		return self.map[pos[0]][pos[1]] == '.'

	def distance_to_end(self, pos):
		x, y = pos
		end_x, end_y = self.expedition_destination
		return ((x - end_x)**2 + (y - end_y)**2)**0.5 

	def heuristic(self, a, b):
		x1, y1 = a
		x2, y2 = b
		return abs(x1 - x2) + abs(y1 - y2)

	def move(self):
		x, y = self.expedition_current_loc
		possibilities = []

		for movement in self.expedition_movements:
			dx, dy = movement
			target = ((x+dx, y+dy))

			if self.is_wall(target):
				continue
			
			if self.is_ground(target) and target != self.expedition_start:
				possibilities.append(target)

		# filter visited
		if len(possibilities) > 1:
			distances = list(map(lambda x: (x, self.heuristic(x, self.expedition_destination)), possibilities))
			distances.sort(key=lambda x: x[1])
			self.expedition.append(distances[0][0])
		else:
			if possibilities:
				self.expedition.append(possibilities[0])

		pprint(possibilities)
		self.expedition_current_loc = self.expedition[-1]

if __name__ == "__main__":
	data = get_input("day-24/test.txt") 
	blizzard = Blizzard(data)
	end = blizzard.expedition_destination

	j = 0
	while True:
		# if j == 0:
		# 	print(f'--- INITIAL STATE ---')
		# else:
		# 	print(f'---- MINUTE {j} ----')
		blizzard.trace()
		blizzard.traverse()
		blizzard.move()
		blizzard.trace_expedition()
		if blizzard.map[end[0]][end[1]] == 'E':
			print(j)
			break
		blizzard.clear()
		blizzard.clear_expedition()
		j += 1

	pprint(["".join(i) for i in blizzard.map])
