from functools import reduce


def get_input(path: str):
    with open(path, mode="r") as file:
        trees = [list(map(int, line)) for line in file.read().split()]

    return trees


def trees_below(row: int, col: int, matrix: list[list[int]]):
    return [r[col] for r in matrix[row + 1 :]]


def trees_above(row: int, col: int, matrix: list[list[int]]):
    return [r[col] for r in matrix[:row]]


def get_distance(trees: list[int], current: int) -> int:
    d = 0
    for t in trees:
        d += 1
        if t >= current:
            break

    return d


def get_visibility_count_and_highest_scenic_score(matrix: list[list[int]]):
    width = 2 * len(matrix[0])
    height = 2 * (len(matrix) - 2)
    visible = width + height
    highest_score = 0

    for row in range(1, len(matrix) - 1):
        for col in range(1, len(matrix[0]) - 1):
            current = matrix[row][col]

            left = matrix[row][:col]
            right = matrix[row][col + 1 :]
            bottom = trees_below(row, col, matrix)
            top = trees_above(row, col, matrix)

            if any(
                [
                    all(tree < current for tree in left),
                    all(tree < current for tree in right),
                    all(tree < current for tree in bottom),
                    all(tree < current for tree in top),
                ]
            ):
                visible += 1

                scenic_score = reduce(
                    lambda x, y: x * y,
                    [
                        get_distance(left[::-1], current),
                        get_distance(right, current),
                        get_distance(top[::-1], current),
                        get_distance(bottom, current),
                    ],
                )

                if scenic_score > highest_score:
                    highest_score = scenic_score

    return visible, highest_score


if __name__ == "__main__":
    trees = get_input("day-08/input.txt")
    visiblility_count, scenic_score = get_visibility_count_and_highest_scenic_score(
        trees
    )
    print("PART 1", visiblility_count)
    print("PART 2", scenic_score)
