import operator
import numpy
from copy import deepcopy


class Monkey:
    def __init__(self, items, operation, test_denominator, true_destination, false_destination):
        self.items = list(items)
        self.operation = operation
        self.test_denominator = int(test_denominator)
        self.true_destination = int(true_destination)
        self.false_destination = int(false_destination)
        self.inspected_count = 0

    def process_items(self, worry_reducer):
        global denominator_product

        ops = {"+": operator.add, "*": operator.mul}
        op = ops[self.operation[0]]
        val = self.operation[2:]
        destinations = {self.true_destination: [], self.false_destination: []}
        for item in self.items:
            if val == "old":
                new = op(item, item)
            else:
                new = op(item, int(val))
            new = worry_reducer(new)
            remainder = new % self.test_denominator
            destinations[self.true_destination if remainder == 0 else self.false_destination].append(new)
        self.inspected_count += len(self.items)
        self.items = []
        return destinations

    def catch_items(self, items):
        self.items += items


def part_one_reducer(value):
    return value // 3


def part_two_reducer(value):
    global denominator_product
    return value % denominator_product


def solve(part, monkeys):
    for r in range(20 if part == 1 else 10000):
        for monkey in monkeys.values():
            thrown = monkey.process_items(worry_reducer=part_one_reducer if part == 1 else part_two_reducer)
            for destination in thrown.keys():
                monkeys[destination].catch_items(thrown[destination])

    active = sorted([monkey.inspected_count for monkey in monkeys.values()], reverse=True)
    solution = active[0] * active[1]
    print("Part %s: %d" % ("One" if part == 1 else "Two", solution))


init = {}
with open("day11.txt") as reader:
    while(True):
        line = reader.readline().strip()
        key = int(line.split()[-1].strip(" :"))
        line = reader.readline().strip()
        starting_items = [int(i) for i in line.split(": ")[-1].split(", ")]
        line = reader.readline().strip()
        monkey_do = line.split("=")[-1].strip()[4:]
        line = reader.readline().strip()
        denominator = int(line.split()[-1])
        line = reader.readline().strip()
        if_true = int(line.split()[-1])
        line = reader.readline().strip()
        if_false = int(line.split()[-1])
        init.update({key: Monkey(starting_items, monkey_do, denominator, if_true, if_false)})
        if not reader.readline():
            break

denominator_product = int(numpy.prod([monkey.test_denominator for monkey in init.values()]))
solve(part=1, monkeys=deepcopy(init))
solve(part=2, monkeys=deepcopy(init))
