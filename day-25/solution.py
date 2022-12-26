def get_input(path: str):
    with open(path, mode="r") as file:
        fuel_requirements = file.read().splitlines()
    return fuel_requirements

def get_max_limit(num):
	i = 0
	d = 0
	c = 0

	while d < num:
		d += (2 * 5**i)
		i += 1
		c += 1

	return c

SNAFUS = {
    -2: "=",
    -1: "-",
    0: "0",
    1: "1",
    2: "2"
}

def convert_to_s(num):
	res, val = '', 0
	numDigits = get_max_limit(num)
	for i in range(numDigits-1, -1, -1):
		val = round(num / 5 ** i)
		num -= val * 5 ** i
		res += SNAFUS[val]

	return res

def convert(num):
	total = 0
	for i in range(len(num)-1, -1, -1):
		n = num[len(num) - i - 1]
		if n == '=':
			total += (5**i * -2)
		elif n == '-':
			total += (5**i * -1)
		elif n.isnumeric():
			total += (5**i * int(n))

	return total


if __name__ == '__main__':
	data = get_input("day-25/input.txt")
	n = sum(map(convert, data))
	print('PART 1', n)
	print('PART 2', convert_to_s(n))
