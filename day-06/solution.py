from more_itertools import all_unique


def get_input(path: str) -> list[str]:
    with open(path, mode="r") as file:
        data_stream = file.readline()

    return data_stream


def get_first_marker_position(iterable: str, character_length: int):
    i, j = 0, character_length

    while i < len(iterable) and j < len(iterable):
        if all_unique(iterable[i:j]):
            return j

        i += 1
        j += 1


if __name__ == "__main__":
    data_stream = get_input("day-06/input.txt")
    print("PART-1", get_first_marker_position(data_stream, 4))
    print("PART-2", get_first_marker_position(data_stream, 14))
