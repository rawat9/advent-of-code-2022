strategy_guide = {
    "A Y": 8,
    "A X": 4,
    "A Z": 3,
    "B Y": 5,
    "B X": 1,
    "B Z": 9,
    "C Y": 2,
    "C X": 7,
    "C Z": 6,
}

strategy_guide_2 = {
    "A Y": 4,
    "A X": 3,
    "A Z": 8,
    "B Y": 5,
    "B X": 1,
    "B Z": 9,
    "C Y": 6,
    "C X": 2,
    "C Z": 7,
}


def get_input(path: str) -> list[str]:
    with open(path, mode="r") as file:
        file_contents = file.read().split("\n")

    return file_contents


def calculate_total_score(data, strategy_guide) -> int:
    return sum(map(lambda x: strategy_guide[x], data))


if __name__ == "__main__":
    data = get_input("day-02/input.txt")
    print("PART-1", calculate_total_score(data, strategy_guide))
    print("PART-2", calculate_total_score(data, strategy_guide_2))
