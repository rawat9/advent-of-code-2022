from collections import defaultdict

isCommand = lambda x: x.startswith("$ cd")

def get_input(path: str) -> list[str]:
    with open(path, mode="r") as file:
        terminal_output = file.read().split("\n")

    return terminal_output

directory_tree = defaultdict(int)
paths = []

def build_dir_tree(terminal_output):
    for line in terminal_output:
        if isCommand(line):
            dir = line.split()[2]
            if dir == "/":
                paths.append("/")
            elif dir == "..":
                paths.pop()
            else:
                paths.append(f"{paths[-1]}{'/' if paths[-1] != '/' else ''}{dir}")

        if line[0].isnumeric():
            for path in paths:
                directory_tree[path] += int(line.split()[0])

if __name__ == '__main__':
    terminal_output = get_input("day-07/input.txt")
    build_dir_tree(terminal_output)
    print("PART 1", sum(s for s in directory_tree.values() if s <= 100000))
    print("PART 2", min(s for s in directory_tree.values() if s >= 30000000 - (70000000 - directory_tree['/'])))
