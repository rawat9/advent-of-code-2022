import operator
import math
with open("day-11/test.txt") as text_file:
  instr = text_file.read().strip().split('\n\n')

class Monkey:
  def __init__(self, items, op, change, test, true, false):
    self.items = items
    self.op = op
    self.change = change
    self.test = test
    self.true = true
    self.false = false
    self.inspections = 0

  def inspect(self, mod):
    self.inspections += 1
    if self.change == "old":
      self.items[0] = self.op(self.items[0], self.items[0])%mod
    else: self.items[0] = self.op(self.items[0], int(self.change))%mod

  def test_item(self, mod):
    self.inspect(mod)
    return self.true if self.items[0] % self.test == 0 else self.false

monkeys = []
for monkey in instr:
  m = list(map(str.strip, monkey.split('\n')))
  items = list(map(int, m[1].split(': ')[1].split(', ')))
  op = operator.add if '+' in m[2] else operator.mul
  change = m[2].split(' ')[-1]
  test = int(m[3].split(' ')[-1])
  true, false = int(m[4].split(' ')[-1]), int(m[5].split(' ')[-1])
  monkeys.append(Monkey(items, op, change, test, true, false))

mod = math.prod([m.test for m in monkeys])
print([m.test for m in monkeys])
for _ in range(10000):
  for m in range(len(monkeys)):
    for i in range(len(monkeys[m].items)):
      res = monkeys[m].test_item(mod)
      monkeys[res].items.append(monkeys[m].items.pop(0))

insp = []
for m in monkeys:
  insp.append(m.inspections)
# print(sorted(insp)[-1] * sorted(insp)[-2])