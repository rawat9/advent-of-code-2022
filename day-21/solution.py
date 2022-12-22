from sympy.solvers import solve
from sympy import Symbol, simplify

dd = {}

def get_input(path: str):
    with open(path, mode="r") as file:
        data = file.read().splitlines()
        for d in data:
            monkey_name, job = d.split(":")
            job = job.strip()
            if job.isnumeric():
                dd[monkey_name] = int(job)
            else:
                dd[monkey_name] = job.split()

    return dd

def get_yelled_number(key: str, data: dict) -> int:
    if isinstance(data[key], list):
        key1, key2 = data[key][0], data[key][2]
        match data[key][1]:
            case '+':
                return simplify(get_yelled_number(key1, data) + get_yelled_number(key2, data))
            case "-":
                return simplify(get_yelled_number(key1, data) - get_yelled_number(key2, data))
            case "*":
                return simplify(get_yelled_number(key1, data) * get_yelled_number(key2, data))
            case "/":
                return simplify(get_yelled_number(key1, data) / get_yelled_number(key2, data))

    return data[key]


if __name__ == "__main__":
    data = get_input("day-21/input.txt")
    print('PART 1', int(get_yelled_number('root', data)))

    x = Symbol('x')
    data['humn'] = x
    left_tree = get_yelled_number('lccz', data)
    right_tree = get_yelled_number('pttp', data)
    print('PART 2', solve(left_tree - right_tree)[0])
