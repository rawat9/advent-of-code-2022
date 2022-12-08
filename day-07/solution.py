from pprint import pprint

def get_input(path: str) -> list[str]:
    with open(path, mode="r") as file:
        terminal_output = file.read().split("\n")

    return terminal_output


stack = []
directory_tree = {}

isCommand = lambda x: x.startswith("$")


def get_cwd() -> str:
    return stack[-1]

def build_dir_tree(terminal_output: list[str]):
    for line in terminal_output:
        if isCommand(line):
            command, *args = line.split()[1:]

            if command == "cd":
                dir = args[0]
                if dir == "..":
                    stack.pop()
                else:
                    stack.append(dir)
                    directory_tree[dir] = []
        else:
            pwd = get_cwd()
            a, b = line.split()
            if a == 'dir':
                directory_tree[pwd].append(b)
            else:
                directory_tree[pwd].append(int(a))

def get_sum(directory):
    total = 0

    for file in directory_tree[directory]:
        if isinstance(file, str):
            total += get_sum(file)
        else:
            total += file
    return total


def find_right_file_size():
    return sum(map(lambda x: get_sum(x) if get_sum(x) <= 100000 else 0, directory_tree.keys()))


if __name__ == "__main__":
    terminal_output = get_input("day-07/test.txt")
    build_dir_tree(terminal_output)
    pprint(directory_tree)
    pprint(find_right_file_size())
