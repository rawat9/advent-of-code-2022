import numpy as np

def expand_cols_right(grid, n=1):
	col = [['.'] * len(grid)] * n
	return np.insert(grid, len(grid[0]), col, axis=1)

def expand_cols_left(grid, n=1):
	col = [['.'] * len(grid)] * n
	return np.insert(grid, 0, col, axis=1)
	

def expand_rows_below(grid, n=1) -> None:
	row = [['.'] * len(grid[0])] * n
	return np.append(grid, row, axis=0)
	

def expand_rows_above(grid, n=1):
	row = [['.'] * len(grid[0])] * n
	return np.insert(grid, 0, row, axis=0)
	
def get_resolved_grid(data):
	new1 = expand_rows_above(np.array(data), 30)
	new2 = expand_rows_below(new1, 60)
	new3 = expand_cols_left(new2, 60)
	new4 = expand_cols_right(new3, 60)
	return new4