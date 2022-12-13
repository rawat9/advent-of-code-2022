from more_itertools import split_at
from itertools import zip_longest


def flatten(S):
    if S == []:
        return S

    if isinstance(S[0], list):
        level += 1
        return flatten(S[0]) + flatten(S[1:])

    return S[:1] + flatten(S[1:])




def get_input(path: str):
    with open(path, mode="r") as file:
        packets = list(split_at(map(str.rstrip, file.readlines()), lambda x: x == ""))

    return packets


def compare(left, right):
    print(left, right)
    if isinstance(left, int):
        return compare([left], right)

    if isinstance(right, int):
        return compare(left, [right])

    for l, r in zip_longest(left, right, fillvalue=''):
        # print(l, r)
        if l == r:
            continue

        if isinstance(l, list):
            return compare(l, r)

        if isinstance(r, list):
            return compare(l, r)

        if left == '':
            return True

        elif right == '':
            return False

        if l != '' and r != '' and l < r:
            return True

        elif l != '' and r != '' and l > r:
            return False

        print(f'left={l}, right={r}')
    return False

def solve(packets):
    return list(map(lambda pair: compare(eval(pair[0]), eval(pair[1])), packets))


if __name__ == "__main__":
    packets = get_input("test.txt")
    # print(packets)
    # print(solve(packets))
    a = [[4,4],4,4]
    b = [[4,4],4,4,4]
    c = compare(a, b)
    print(c)
