def get_input(path: str) -> list[str]:
    with open(path, mode="r") as file:
        data = file.read().split()
    return data


def find_overlap(sections: list[str], complete_overlap: bool = True) -> int:
    count = 0
    for section in sections:
        pair_a, pair_b = section.split(",")
        start_a, end_a = map(int, pair_a.split("-"))
        start_b, end_b = map(int, pair_b.split("-"))

        if complete_overlap:
            if (start_a >= start_b and end_a <= end_b) or (
                start_b >= start_a and end_b <= end_a
            ):
                count += 1

        else:
            if start_a <= end_b and end_a >= start_b:
                count += 1

    return count


if __name__ == "__main__":
    data = get_input("day-04/input.txt")
    print("PART-1", find_overlap(data, complete_overlap=True))
    print("PART-2", find_overlap(data, complete_overlap=False))
