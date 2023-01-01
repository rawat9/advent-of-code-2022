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
        self.directions = {0: {'L': 2, 'R': 1}, 1: {'L': 0, 'R': 2}, 2: {'L': 1, 'R': 3}, 3: {'L': 2, 'R': 0}}

    def is_open_tile(self, pos: Position) -> bool:
        # unused
        x, y = pos
        return self.board[x][y] == '.'

    def is_covered_tile(self, pos: Position) -> bool:
        x, y = pos
        return self.board[x][y] in ('▶︎', '◀︎', '▲', '▼')

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
                res = ''.join(self.board[row])
                new_col = res.find('.')
                if new_col == -1:
                    new_col = res.find('#')
                    if new_col == -1:
                        return (row, 0)
                return (row, new_col)
            case 1:
                row, col = pos
                res = "".join([r[col] for r in self.board])
                new_row = res.find('.')
                if new_row == -1:
                    new_row = res.find('#')
                    if new_row == -1:
                        return (0, col)
                return (new_row, col)
            case 2:
                row = pos[0]
                res = ''.join(self.board[row][::1])
                new_col = res.find('.')
                if new_col == -1:
                    new_col = res.find('#')
                    if new_col == -1:
                        return (row, self.col_length-1)
                return (row, len(self.board[row]) - new_col - 1)
            case 3:
                row, col = pos
                res = "".join([r[col] for r in self.board][::-1])
                new_row = res.find('.')
                if new_row == -1:
                    new_row = res.find('#')
                    if new_row == -1:
                        return (self.row_length-1, col)
                return (len(res) - new_row - 1, col)

        return (-1, -1)

    def move_right(self, n: int):
        for _ in range(n):
            x, y = self.current_position
            next_tile: Position = (x, y+1)

            if y+1 > self.col_length-1 or self.is_void(next_tile):
                i, j = self.get_opposite_pos(next_tile)
                if self.is_solid_tile((i, j)):
                    break
                self.board[i][j] = '▶︎'
                self.route.append((i, j))
                self.current_position = (i, j)
            elif self.is_solid_tile(next_tile):
                break
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

            # if IndexError or void
            if x-1 > self.row_length-1 or self.is_void(next_tile):
                i, j = self.get_opposite_pos(next_tile)
                if self.is_solid_tile((i, j)):
                    break
                self.board[i][j] = '▲'
                self.route.append((i, j))
                self.current_position = (i, j)
            elif self.is_solid_tile(next_tile):
                break
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
            if y-1 > self.col_length - 1 or self.is_void(next_tile):
                i, j = self.get_opposite_pos(next_tile)
                if self.is_solid_tile((i, j)):
                    break
                self.board[i][j] = '◀︎'
                self.route.append((i, j))
                self.current_position = (i, j)
            elif self.is_solid_tile(next_tile):
                break
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

            if x + 1 > self.row_length-1 or self.is_void(next_tile):
                i, j = self.get_opposite_pos(next_tile)
                if self.is_solid_tile((i, j)):
                    break
                self.board[i][j] = '▼'
                self.route.append((i, j))
                self.current_position = (i, j)
            elif self.is_solid_tile(next_tile):
                break
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

    def get_final_password(self, row: int, col: int):
        return (1000 * row) + (4 * col) + self.current_direction

    def __repr__(self):
        pprint([" ".join(row) for row in self.board])
        return ' '

if __name__ == "__main__":
    board, directions = get_input("day-22/input.txt")
    board = [list(i) for i in board]
    path_description = re.split('(\\D+)', directions[0])

    board = MapBoard(board, path_description)
    board.move()
    row, col = board.route[-1]
    pprint(board.get_final_password(row+1, col+1))
