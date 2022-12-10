def get_input(path: str):
    with open(path, mode="r") as file:
        instructions = file.read().split("\n")

    return instructions


isNoop = lambda x: x.startswith("noop")
pixels = ["."] * 240
LIT_PIXEL = "█"


def check(cycle, cycles, X: int) -> int:
    for num in cycles:
        if cycle == num:
            return X * num

    return 0


def process_instructions(instructions):
    X, cycle = 1, 0
    total = 0

    for instruction in instructions:
        if isNoop(instruction):
            if X - 1 <= cycle % 40 <= X + 1:
                pixels[cycle] = LIT_PIXEL
            cycle += 1
            total += check(cycle, (20, 60, 100, 140, 180, 220), X)
        else:
            _, value = instruction.split()
            for _ in range(2):
                if X - 1 <= cycle % 40 <= X + 1:
                    pixels[cycle] = LIT_PIXEL
                cycle += 1
                total += check(cycle, (20, 60, 100, 140, 180, 220), X)

            X += int(value)

    return total


def get_image():
    for i in range(6):
        print("".join(pixels[i * 40 : (i + 1) * 40]))


if __name__ == "__main__":
    instructions = get_input("day-10/input.txt")
    print("PART 1", process_instructions(instructions))
    print("PART 2")
    get_image()
