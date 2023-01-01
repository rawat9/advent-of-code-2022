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

		pprint([" ".join(i) for i in self.map])

	def clear(self):
		for i in range(1, self.row_length-1):
			for j in range(1, self.col_length-1):
				self.map[i][j] = '.' 


class Me(Blizzard):
	'''
	Handle moving through the map	
	'''
	def __init__(self, map, start, destination):
		super().__init__(map)
		self.start = start
		self.destination = destination
		self.movements = [(0,1), (0,-1), (-1,0), (1,0)]
		self.current_loc = start
		self.expedition = [start]

	def is_ground(self, pos):
		return self.map[pos[0]][pos[1]] == '.'

	def move(self):
		x, y = self.current_loc

		for movement in self.movements:
			dx, dy = movement
			target = ((x+dx, y+dy))
			
			if self.is_ground(target) and target != self.start:
				self.expedition.append(target)
				break

		self.current_loc = self.expedition[-1]

	def update_location(self, pos):
		x, y = pos
		self.map[x][y] = 'E'

if __name__ == "__main__":
	data = get_input("day-24/test.txt") 
	blizzard = Blizzard(data)
	start = (0, 1)
	end = (5, 6)
	me = Me(blizzard.map, start, end)

	for j in range(5):
		if j == 0:
			print(f'--- INITIAL STATE ---')
		else:
			print(f'---- MINUTE {j} ----')
		blizzard.trace()
		blizzard.traverse()
		me.move()
		print()
		blizzard.clear()