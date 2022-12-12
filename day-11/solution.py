from more_itertools import split_at
from typing import Union
import operator
from dataclasses import dataclass

def get_input(path: str):
    with open(path, mode="r") as file:
        notes = list(split_at(file.read().splitlines(), lambda x: x == ''))

    return notes

monkeys = []

# refactor this method
def prepare_data(notes) -> None:
	for note in notes:
		id = note[0].rstrip(':')[-1]
		starting_items = list(map(int, note[1].split(':')[1].strip().split(',')))
		op = '+' if '+' in note[2].split('=')[1].strip() else '*'
		test = note[3].split(':')[1].strip()
		if_true = note[4].split(':')[1].strip()
		if_false = note[5].split(':')[1].strip()

		monkey = Monkey(id, starting_items, op, test, if_true, if_false)
		monkeys.append(monkey)


def throw_item_to_monkey(worry_level: int, monkey_id: int):
	return monkeys[monkey_id].items.append(worry_level)


def get_money_business_level():
	inspection_count = list(map(lambda x: x.inspected_count, monkeys))
	inspection_count.sort()
	return inspection_count[-1] * inspection_count[-2]


@dataclass
class Monkey:
	id: str
	items: list[int]
	operator: str 
	test: str
	if_true: str
	if_false: str
	inspected_count: int = 0

	def run_inspection(self):
		while len(self.items) > 0:
			self.inspected_count += 1

			worry_level = self.items.pop(0)
			result = self.get_result_of_operation(worry_level, self.operation)
			
			# monkey gets bored

			# current_worry_level = result // 3
			self.check_condition(result, self.test)

	def check_condition(self, worry_level: int, condition: str):
		num = int(condition.split()[-1])
		if worry_level % num == 0:
			throw_item_to_monkey(worry_level, int(self.if_true[-1]))
		else:
			throw_item_to_monkey(worry_level, int(self.if_false[-1]))

	def get_result_of_operation(self, change: int, operation: str):
		result = 0
		# _, operator, num = operation.split()
		if num.isnumeric():
			if operator == '*':
				result = old * int(num)
			else:
				result = old + int(num)
		else:
			result = old * old

		return result


if __name__ == "__main__":
	notes = get_input("day-11/test.txt")
	prepare_data(notes)

	for _ in range(10000):
		for monkey in monkeys:
			monkey.run_inspection()

	inspection_count = list(map(lambda x: x.inspected_count, monkeys))
	print(inspection_count)

	# mod = math.prod([m.test for m in monkeys])
	# for _ in range(10000):
	# 	for m in range(len(monkeys)):
	# 		for i in range(len(monkeys[m].items)):
	# 			res = monkeys[m].test_item(mod)
	# 			monkeys[res].items.append(monkeys[m].items.pop(0))

	# insp = []
	# for m in monkeys:
	# insp.append(m.inspections)
	# print(sorted(insp)[-1] * sorted(insp)[-2])