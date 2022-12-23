from collections import Counter
from operator import add
from pprint import pprint

def get_input(path: str):
    with open(path, mode="r") as file:
        data = [list(i) for i in file.read().splitlines()]
    return data

# TODO: consider the order by rounds
directions = {
    "N": [(-1, -1), (-1, 0), (-1, 1)],   # NW, N, NE
    "S": [(1,-1), (1,0), (1,1)],         # SW, S, SE
    "E": [(-1,-1), (0, -1), (1,-1)],     # NW, W, SW
    "W": [(-1, 1), (0,1), (1,1)]         # NE, E, SE
}

class Grove:
    def __init__(self, grid) -> None:
        self.grid = grid
        self.expand_columns(n=3)
        self.expand_rows(n=3)
        self.proposed_destinations = {}

    def isElf(self, pos):
        return self.grid[pos[0]][pos[1]] == '#'

    def isEmpty(self, pos):
        return self.grid[pos[0]][pos[1]] == '.'
        
    def expand_rows(self, n=1) -> None:
        row = ['.' for _ in range(len(self.grid[0]))]
        for _ in range(n):
            self.grid.insert(0, row)
            self.grid.append(row)

    def expand_columns(self, n=1) -> None:
        for _ in range(n):
            for row in self.grid:
                row.insert(0, '.')
                row.append('.')

    def get_positions(self, direction, pos):
        positions = []
        match direction:
            case 'N':
                for d in directions['N']:
                    position = tuple(map(add, d, pos))
                    positions.append(position)
                return positions
            case 'S':
                for d in directions['S']:
                    position = tuple(map(add, d, pos))
                    positions.append(position)
                return positions
            case 'W':
                for d in directions['W']:
                    position = tuple(map(add, d, pos))
                    positions.append(position)
                return positions
            case 'E':
                for d in directions['E']:
                    position = tuple(map(add, d, pos))
                    positions.append(position)
                return positions

    def get_proposed_position(self, pos: tuple[int]):
        north_directions = self.get_positions('N', pos)
        south_directions = self.get_positions('S', pos)
        west_directions = self.get_positions('W', pos)
        east_directions = self.get_positions('E', pos)

        if all([self.isEmpty(d) for d in north_directions]):
            return north_directions[1]
        if all([self.isEmpty(d) for d in south_directions]):
            return south_directions[1]
        if all([self.isEmpty(d) for d in west_directions]):
            return west_directions[1]
        if all([self.isEmpty(d) for d in east_directions]):
            return east_directions[1]
        else:
            return pos

    def process_round_one(self):
        '''
        In this round, each elf proposed their destination
        '''
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.isEmpty((r,c)):
                    continue

                proposed_pos = self.get_proposed_position((r,c))
                self.proposed_destinations[(r,c)] = proposed_pos

    def filter_can_move(self):
        counter = Counter(self.proposed_destinations.values())
        elementsToRemove = list(filter(lambda x: counter[x] > 1, counter))
        for k, v in dict(self.proposed_destinations).items():
            for position in elementsToRemove:
                if k == v or v == position:
                    del self.proposed_destinations[k]

    def process_round_two(self):
        '''
        In this round, Elves actually make their proposed move
        '''
        self.filter_can_move()
        # for current, destination in self.proposed_destinations.items():
        #     x, y = current
        #     dest_x, dest_y = destination
            # self.grid[x][y] = '.'
            # self.grid[dest_x][dest_y] = '#'

        self.grid[12][8] = '#'

if __name__ == "__main__":
    data = get_input("day-23/test.txt")
    grove = Grove(data)
    grove.process_round_one()
    grove.process_round_two()
    pprint(grove.grid)
