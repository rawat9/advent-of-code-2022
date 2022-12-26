import numpy as np
from math import ceil
from helpers import get_resolved_grid
from collections import Counter
from operator import add
from pprint import pprint


def get_input(path: str):
    with open(path, mode="r") as file:
        data = [list(i) for i in file.read().splitlines()]
    return data


directions = {
    "N": [(-1, -1), (-1, 0), (-1, 1)],    # NW, N, NE
    "S": [(1, -1), (1, 0), (1, 1)],       # SW, S, SE
    "W": [(-1, -1), (0, -1), (1, -1)],    # NW, W, SW
    "E": [(-1, 1), (0, 1), (1, 1)],       # NE, E, SE
}


class Grove:
    def __init__(self, grid) -> None:
        self.grid = grid
        self.proposed_destinations = {}

    def isElf(self, pos):
        return self.grid[pos[0]][pos[1]] == "#"

    def isEmpty(self, pos):
        return self.grid[pos[0]][pos[1]] == "."

    def get_positions(self, direction, pos):
        """
        d + dx
        """
        positions = []
        match direction:
            case "N":
                for d in directions["N"]:
                    position = tuple(map(add, d, pos))
                    positions.append(position)
                return positions
            case "S":
                for d in directions["S"]:
                    position = tuple(map(add, d, pos))
                    positions.append(position)
                return positions
            case "W":
                for d in directions["W"]:
                    position = tuple(map(add, d, pos))
                    positions.append(position)
                return positions
            case "E":
                for d in directions["E"]:
                    position = tuple(map(add, d, pos))
                    positions.append(position)
                return positions

    def get_proposed_position(self, pos: tuple[int], order: str):
        north_directions = self.get_positions("N", pos)
        south_directions = self.get_positions("S", pos)
        west_directions = self.get_positions("W", pos)
        east_directions = self.get_positions("E", pos)

        if all(
            [
                all([self.isEmpty(d) for d in north_directions]),
                all([self.isEmpty(d) for d in south_directions]),
                all([self.isEmpty(d) for d in west_directions]),
                all([self.isEmpty(d) for d in east_directions]),
            ]
        ):
            return pos

        match order:
            case "NSWE":
                if all([self.isEmpty(d) for d in north_directions]):
                    return north_directions[1]
                if all([self.isEmpty(d) for d in south_directions]):
                    return south_directions[1]
                if all([self.isEmpty(d) for d in west_directions]):
                    return west_directions[1]
                if all([self.isEmpty(d) for d in east_directions]):
                    return east_directions[1]
            case "SWEN":
                if all([self.isEmpty(d) for d in south_directions]):
                    return south_directions[1]
                if all([self.isEmpty(d) for d in west_directions]):
                    return west_directions[1]
                if all([self.isEmpty(d) for d in east_directions]):
                    return east_directions[1]
                if all([self.isEmpty(d) for d in north_directions]):
                    return north_directions[1]
            case "WENS":
                if all([self.isEmpty(d) for d in west_directions]):
                    return west_directions[1]
                if all([self.isEmpty(d) for d in east_directions]):
                    return east_directions[1]
                if all([self.isEmpty(d) for d in north_directions]):
                    return north_directions[1]
                if all([self.isEmpty(d) for d in south_directions]):
                    return south_directions[1]
            case "ENSW":
                if all([self.isEmpty(d) for d in east_directions]):
                    return east_directions[1]
                if all([self.isEmpty(d) for d in north_directions]):
                    return north_directions[1]
                if all([self.isEmpty(d) for d in south_directions]):
                    return south_directions[1]
                if all([self.isEmpty(d) for d in west_directions]):
                    return west_directions[1]
        return pos

    def process_round_one(self, order):
        """
        In this round, each elf proposed their destination
        """
        loc = np.where(grid == '#')
        for r, c in zip(loc[0], loc[1]):
            proposed_pos = self.get_proposed_position((r, c), order)
            self.proposed_destinations[(r, c)] = proposed_pos

    def filter_can_move(self):
        counter = Counter(self.proposed_destinations.values())
        elementsToRemove = list(filter(lambda x: counter[x] > 1, counter))
        for k, v in dict(self.proposed_destinations).items():
            if k == v:
                del self.proposed_destinations[k]

            for position in elementsToRemove:
                if v == position:
                    del self.proposed_destinations[k]

    def process_round_two(self):
        """
        In this round, Elves actually make their proposed move
        """
        for current, destination in self.proposed_destinations.items():
            x, y = current
            dest_x, dest_y = destination
            self.grid[x][y] = "."
            self.grid[dest_x][dest_y] = "#"

        self.proposed_destinations.clear()


if __name__ == "__main__":
    data = get_input("day-23/input.txt")
    grid = get_resolved_grid(data)
    grove = Grove(grid)
    rounds = 1100
    order = [
        "NSWE",
        "SWEN",
        "WENS",
        "ENSW",
    ] * ceil(rounds/4)

    for i in range(rounds):
        grove.process_round_one(order[i])
        grove.filter_can_move()
        if len(grove.proposed_destinations) == 0:
            print(i+1)
            break
        grove.process_round_two()
