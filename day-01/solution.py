from more_itertools import split_at


def get_input(path: str) -> list[str]:
    with open(path, mode="r") as file:
        data = list(split_at(file.read().split("\n"), lambda x: x == ""))

    return data


def transform(input_data: list[str]) -> list[int]:
    return [sum(map(int, data)) for data in input_data]


def get_max_calories(calories: list[int]) -> int:
    return max(calories)


def get_top_three_calories(calories: list[int]):
    return sum(sorted(calories)[-3:])


if __name__ == "__main__":
    input_data = get_input("day-01/input.txt")
    print("PART-1", get_max_calories(transform(input_data)))
    print("PART-2", get_top_three_calories(transform(input_data)))
