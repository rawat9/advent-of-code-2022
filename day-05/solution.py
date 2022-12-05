from more_itertools import split_at
import re

stacks_of_crates = {}


def get_input(path: str) -> list[str]:
    with open(path, mode="r") as file:
        file_data = list(split_at(file.read().splitlines(), lambda x: x == ""))

        crates = file_data[0]
        procedures = file_data[1]

    return crates, procedures


def get_matrix(crates: list[str]):
    matrix = []
    for crate in crates:
        row = re.split("    | ", crate)
        matrix.append(row)

    return list(zip(*matrix[::-1]))  # transposed version


def build_stacks_of_crates(crates: list[str]) -> None:
    stacks = crates[-1].split()
    matrix = get_matrix(crates[:-1])

    for stack, row in zip(stacks, matrix):
        stacks_of_crates[stack] = list(
            map(lambda x: x[1], filter(lambda x: x != "", row))
        )


def move(
    from_stack: str, to_stack: str, number_of_crates_to_move: int, keep_ordering: bool
) -> None:
    curr_idx = len(stacks_of_crates[to_stack])

    for _ in range(number_of_crates_to_move):
        if keep_ordering:
            crate = stacks_of_crates[from_stack].pop()
            stacks_of_crates[to_stack].insert(curr_idx, crate)
        else:
            crate = stacks_of_crates[from_stack].pop()
            stacks_of_crates[to_stack].append(crate)


def get_crates_on_top(stacks_of_crates) -> str:
    return "".join(list(map(lambda x: x[-1], stacks_of_crates.values())))


def process_instructions(instructions: list[str], keep_ordering: bool) -> None:
    for instruction in instructions:
        instruction_array = instruction.split()
        number_of_crates_to_move = int(instruction_array[1])
        from_stack = instruction_array[3]
        to_stack = instruction_array[5]
        move(from_stack, to_stack, number_of_crates_to_move, keep_ordering)


if __name__ == "__main__":
    crates, instructions = get_input("day-05/input.txt")
    build_stacks_of_crates(crates)
    # process_instructions(instructions, keep_ordering=True)
    # print("PART-1", get_crates_on_top(stacks_of_crates))
    process_instructions(instructions, keep_ordering=False)
    print("PART-2", get_crates_on_top(stacks_of_crates))

