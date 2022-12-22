from more_itertools import split_at
from itertools import zip_longest


def get_input(path: str):
    with open(path, mode="r") as file:
        packets = list(split_at(map(str.rstrip, file.readlines()), lambda x: x == ""))

    return packets


def compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        return left - right

    if isinstance(left, int) and isinstance(right, list):
        return compare([left], right)

    if isinstance(right, int) and isinstance(left, list):
        return compare(left, [right])

    for l, r in zip(left, right):
        if l == r:
            continue

    return len(left) - len(right)

# def solve(packets):
#     result = list(map(lambda pair: compare(eval(pair[0]), eval(pair[1])), packets))
#     return sum(map(lambda x: x[0] + 1 if x[1] else 0, enumerate(result)))


if __name__ == "__main__":
    packets = get_input("day-13/input.txt")
    # print(packets)
    # print(solve(packets)) # 5606
    a = [[4,4],4,4,]
    b = [[4,4],4,4,4]
    c = compare(a, b)
    print(c)
