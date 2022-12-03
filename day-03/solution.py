from abc import ABC, abstractmethod
from more_itertools import sliced
from string import ascii_letters as letters


def get_input(path: str) -> list[str]:
    with open(path, mode="r") as file:
        data = file.read().split()
    return data


class IInterface(ABC):
    @abstractmethod
    def find_common_item(self, groups: list) -> str:
        ...

    @abstractmethod
    def split_rucksacks(self, rucksacks: list[str]) -> list:
        ...

    def get_priority(self, rucksacks: list[str]) -> int:
        common_items = map(self.find_common_item, self.split_rucksacks(rucksacks))
        return sum(map(lambda x: letters.index(x) + 1, common_items))


class PartOne(IInterface):
    def find_common_item(self, groups):
        return "".join(set(groups[0]) & set(groups[1]))

    def get_priority(self, rucksacks):
        return super().get_priority(rucksacks)

    def split_rucksacks(self, rucksacks):
        result = []

        for rucksack in rucksacks:
            mid = len(rucksack) // 2
            result.append((rucksack[:mid], rucksack[mid:]))

        return result


class PartTwo(IInterface):
    def find_common_item(self, groups):
        return "".join(set(groups[0]) & set(groups[1]) & set(groups[2]))

    def get_priority(self, rucksacks):
        return super().get_priority(rucksacks)

    def split_rucksacks(self, rucksacks):
        return list(sliced(rucksacks, 3))


if __name__ == "__main__":
    data = get_input("day-03/input.txt")
    part_one, part_two = PartOne(), PartTwo()
    print("PART-1", part_one.get_priority(data))
    print("PART-2", part_two.get_priority(data))
