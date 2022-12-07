from pprint import pprint
isDirectory = lambda x: x.startswith("dir")
isCommand = lambda x: x.startswith("$")

stack = []
dir_tree = {}

def find_file_size(files):
    return sum(map(lambda x: int(x.split()[0]), list(filter(lambda x: x.split()[0] != 'dir', files))))

def get_cwd() -> str:
    return stack[-1]
    # return " /".join(stack)

def build_dir_tree(terminal_output: list[str]) -> None:
    ls_output = []
    for line in terminal_output:
        if isCommand(line):
            command, *args = line.split()[1:]

            if command == "cd":
                dir = args[0]
                if dir == '..':
                    stack.pop()
                else:
                    stack.append(dir)
                ls_output = []

            elif command == "ls":
                pwd = get_cwd()
                dir_tree[pwd] = ls_output
        else:
            ls_output.append(line)

    
    for files in dir_tree.values():
        filesize = find_file_size(files)
        files.append(filesize)

    return dir_tree

def get_input(path: str) -> list[str]:
    with open(path, mode="r") as file:
        terminal_output = file.read().split("\n")

    return terminal_output[:-1]


if __name__ == "__main__":
    terminal_output = get_input("day-07/test.txt")
    pprint(build_dir_tree(terminal_output))

    """
    To keep track of current working directory
    stack = [/, d]
    ------------------------------------------
    '/': [
            dir a: 
                [dir e: [584 i], 29116 f, 2557 g, 62596 h.lst], 
            14848514 b.txt, 
            8504156 c.dat, 
            dir d: [
                4060174 j,
                8033020 d.log,
                5626152 d.ext,
                7214296 k
            ]
        ]
    ----------------------------------------------
    '/': [
        dir a:
        14848514 b.txt, 
        8504156 c.dat, 
        dir d: [
            4060174 j,
            8033020 d.log,
            5626152 d.ext,
            7214296 k
        ]

    ]
    """
