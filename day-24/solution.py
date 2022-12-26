import numpy as np
from pprint import pprint

def get_input(path: str):
    with open(path, mode="r") as file:
        data = [list(i) for i in file.read().splitlines()]
    return data

class Blizzard:
	def __init__(self, map) -> None:
		self.map = map
		self.row_length = len(self.map)
		self.col_length = len(self.map[0])
		self.directions = {'>': (0, 1), '<': (0, -1), '^': (-1, 0), 'v': (1, 0)}

	def is_blizzard(self, pos):
		return self.map[pos[0]][pos[1]] in self.directions.keys()

	def is_ground(self, pos):
		return self.map[pos[0]][pos[1]] == '.'

	def is_wall(self, pos) -> bool:
		return self.map[pos[0]][pos[1]] == '#'

	def move_right(self, pos):
		# if current pos is a wall i.e #, form a new blizzard on the opp side
		x, y = pos
		next_pos = (x, y+1)
		if self.is_wall(next_pos):
			self.map[x][y] = '.'
			if self.is_blizzard((x, 1)):
				self.map[x][1] += '>'
				self.map[x+dx][y+dy] = str(len(self.map[x+dx][y+dy]))
			else:
				self.map[x][1] = '>'
			return

		# set current pos to 'empty'
		self.map[x][y] = '.'

		# update the blizzard pos
		dx, dy = self.directions['>']
		if self.is_blizzard((x+dx, y+dy)):
			self.map[x+dx][y+dy] += '>'
			# self.map[x+dx][y+dy] = str(len(self.map[x+dx][y+dy]))
		else:
			self.map[x+dx][y+dy] = '>'


	def move_left(self, pos):
		# if current pos is a wall i.e #, form a new blizzard on the opp side
		x, y = pos
		next_pos = (x, y-1)
		if self.is_wall(next_pos):
			self.map[x][y] = '.'
			self.map[x][self.col_length-2] = '>'
			return

		# set current pos to 'empty'
		self.map[x][y] = '.'

		# update the blizzard pos
		dx, dy = self.directions['<']
		if self.is_blizzard((x+dx, y+dy)):
			self.map[x+dx][y+dy] += '<'
			# self.map[x+dx][y+dy] = str(len(self.map[x+dx][y+dy]))
		else:
			self.map[x+dx][y+dy] = '<'

	def move_down(self, pos):
		# if current pos is a wall i.e #, form a new blizzard on the opp side
		x, y = pos
		next_pos = (x+1, y)
		if self.is_wall(next_pos):
			self.map[x][y] = '.'
			self.map[1][y] = 'v'
			return

		# set current pos to 'empty'
		self.map[x][y] = '.'

		# update the blizzard pos
		dx, dy = self.directions['v']
		if self.is_blizzard((x+dx, y+dy)):
			self.map[x+dx][y+dy] += 'v'
			# self.map[x+dx][y+dy] = str(len(self.map[x+dx][y+dy]))
		else:
			self.map[x+dx][y+dy] = 'v'

	def move_up(self, pos):
		# if current pos is a wall i.e #, form a new blizzard on the opp side
		x, y = pos
		next_pos = (x-1, y)
		if self.is_wall(next_pos):
			self.map[x][y] = '.'
			self.map[1][y] = '^'
			return

		# set current pos to 'empty'
		self.map[x][y] = '.'

		# update the blizzard pos
		dx, dy = self.directions['^']
		if self.is_blizzard((x+dx, y+dy)):
			self.map[x+dx][y+dy] += '^'
			# self.map[x+dx][y+dy] = str(len(self.map[x+dx][y+dy]))
		else:
			self.map[x+dx][y+dy] = '^'

	def traverse(self):
		np_map = np.array(self.map)
		loc = np.where((np_map == '>') | (np_map == 'v') | (np_map == '^') | (np_map == '<'))

		for r, c in zip(loc[0], loc[1]):
			match self.map[r][c]:
				case '>':
					self.move_right((r,c))
				case '<':
					self.move_left((r,c))
				case 'v':
					self.move_down((r,c))
				case '^':
					self.move_up((r,c))

if __name__ == "__main__":
	data = get_input("day-24/test.txt") 
	blizzard = Blizzard(data)
	for j in range(4):
		if j == 0:
			print(f'--- INITIAL STATE ---')
		else:
			print(f'---- MINUTE {j} ----')
		pprint([" ".join(i) for i in blizzard.map])
		print()
		blizzard.traverse()
