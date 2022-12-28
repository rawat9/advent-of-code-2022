from rich.pretty import pprint
from rich.console import Console
from time import sleep
import re
from more_itertools import split_at
from _types import Position, Board, Path

console = Console()

def get_input(path: str):
    with open(path, mode="r") as file:
        grid = file.read().splitlines()
        
    return list(split_at(grid, lambda x: x == ''))


class MapBoard:
    def __init__(self, board: Board, path_description: Path) -> None:
        self.board = board
        self.row_length = len(self.board)
        self.col_length = len(self.board[0])
        self.path_description = path_description
        self.current_direction = 0
        self.start = (0, self.board[0].index('.'))
        self.current_position = self.start
        self.route: list[Position] = [self.start]
        # self.movements = {'>': (0, 1), '<': (0, -1), '^': (-1, 0), 'v': (1, 0)}
        self.directions = {0: {'L': 2, 'R': 1}, 1: {'L': 0, 'R': 2}, 2: {'L': 1, 'R': 3}, 3: {'L': 2, 'R': 0}}

    def is_open_tile(self, pos: Position) -> bool:
        x, y = pos
        return self.board[x][y] == '.'

    def is_solid_tile(self, pos: Position) -> bool:
        x, y = pos
        return self.board[x][y] == '#'

    def is_void(self, pos: Position) -> bool:
        x, y = pos
        return self.board[x][y] == ' '

    def get_opposite_pos(self, pos: Position) -> Position:
        match self.current_direction:
            case 0:
                row = pos[0]
                col = self.board[row].index('.')
                return (row, col)
            case 1:
                row, col = pos
                try:
                    new_row = [r[col] for r in self.board].index('.')
                    return (new_row, col)
                except ValueError:
                    new_row = [r[col] for r in self.board].index('#')
                    return (new_row, col)
            case 2:
                pprint('HERE')
            case 3:
                row, col = pos
                try:
                    new_row = [r[col] for r in self.board][::-1].index('.')
                    print('ROW')
                    pprint(new_row)
                    return (new_row, col)
                except ValueError:
                    new_row = [r[col] for r in self.board][::-1].index('#')
                    return (new_row, col)

        return (0, 0)

    def move_right(self, n: int):
        for _ in range(n):
            x, y = self.current_position
            next_tile: Position = (x, y+1)
            if self.is_solid_tile(next_tile):
                break
            elif self.is_void(next_tile):
                i, j = self.get_opposite_pos(next_tile)
                self.board[i][j] = '▶︎'
                self.route.append((i, j))
                self.current_position = (i, j)
            else:
                dx, dy = next_tile 
                self.board[dx][dy] = '▶︎'
                self.route.append(next_tile)
                self.current_position = next_tile

            sleep(0.5)
            console.clear()
            pprint(self)

    def move_up(self, n: int):
        for _ in range(n):
            x, y = self.current_position
            next_tile: Position = (x-1, y)
            if self.is_solid_tile(next_tile):
                break
            elif self.is_void(next_tile):
                i, j = self.get_opposite_pos(next_tile)
                if self.is_solid_tile((i, j)):
                    break
                self.board[i][j] = '▲'
                self.route.append((i, j))
                self.current_position = (i, j)
            else:
                dx, dy = next_tile 
                self.board[dx][dy] = '▲'
                self.route.append(next_tile)
                self.current_position = next_tile

            sleep(0.5)
            console.clear()
            pprint(self)

    def move_left(self, n: int):
        for _ in range(n):
            x, y = self.current_position
            next_tile: Position = (x, y-1)
            if self.is_solid_tile(next_tile):
                break
            elif self.is_void(next_tile):
                i, j = self.get_opposite_pos(next_tile)
                if self.is_solid_tile((i, j)):
                    break
                self.board[i][j] = '◀︎'
                self.route.append((i, j))
                self.current_position = (i, j)
            else:
                dx, dy = next_tile 
                self.board[dx][dy] = '◀︎'
                self.route.append(next_tile)
                self.current_position = next_tile

            sleep(0.5)
            console.clear()
            pprint(self)

    def move_down(self, n: int):
        for _ in range(n):
            x, y = self.current_position
            next_tile: Position = (x+1, y)
            if self.is_solid_tile(next_tile):
                break
            elif self.is_void(next_tile):
                i, j = self.get_opposite_pos(next_tile)
                if self.is_solid_tile((i, j)):
                    break
                self.board[i][j] = '▼'
                self.route.append((i, j))
                self.current_position = (i, j)
            else:
                dx, dy = next_tile 
                self.board[dx][dy] = '▼'
                self.route.append(next_tile)
                self.current_position = next_tile

            sleep(0.5)
            console.clear()
            pprint(self)

    def move(self) -> None:
        for instruction in self.path_description:
            pprint(instruction)
            if instruction.isnumeric():
                match self.current_direction:
                    case 0:
                        self.move_right(int(instruction))
                    case 1:
                        self.move_down(int(instruction))
                    case 2:
                        self.move_left(int(instruction))
                    case 3:
                        self.move_up(int(instruction))
            else:
                self.current_direction = self.directions[self.current_direction][instruction]

    def __repr__(self):
        pprint([" ".join(row) for row in self.board])
        return ' '

if __name__ == "__main__":
    board, directions = get_input("day-22/input.txt")
    board = [list(i) for i in board]
    path_description = re.split('(\\D+)', directions[0])

    board = MapBoard(board, path_description)
    # pprint(board.path_description[:25])
    board.move()
    pprint(board.route)
