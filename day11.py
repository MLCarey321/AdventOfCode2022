import operator


class Monkey:
    def __init__(self, items, operation, test_denominator, true_destination, false_destination):
        self.items = list(items)
        self.operation = operation
        self.test_denominator = int(test_denominator)
        self.true_destination = int(true_destination)
        self.false_destination = int(false_destination)
        self.inspected_count = 0

    def process_items(self):
        ops = {"+": operator.add, "*": operator.mul}
        op = ops[self.operation[0]]
        val = self.operation[2:]
        destinations = {self.true_destination: [], self.false_destination: []}
        for item in self.items:
            if val == "old":
                new = op(item, item)
            else:
                new = op(item, int(val))
            # new = new // 3  # Part One
            # new = new % 96577  # Part Two Test
            remainder = new % self.test_denominator
            destinations[self.true_destination if remainder == 0 else self.false_destination].append(new)
        self.inspected_count += len(self.items)
        self.items = []
        return destinations

    def catch_items(self, items):
        self.items += items


monkeys = {
    0: Monkey(items=[79, 98], operation="* 19", test_denominator=23, true_destination=2, false_destination=3),
    1: Monkey(items=[54, 65, 75, 74], operation="+ 6", test_denominator=19, true_destination=2, false_destination=0),
    2: Monkey(items=[79, 60, 97], operation="* old", test_denominator=13, true_destination=1, false_destination=3),
    3: Monkey(items=[74], operation="+ 3", test_denominator=17, true_destination=0, false_destination=1)
}

log = False
for r in range(10000):
    # log = r == 0 or (r + 1) % 1000 == 0
    if log:
        print("==After round %d==" % (r + 1))
    for key in monkeys.keys():
        monkey = monkeys[key]
        thrown = monkey.process_items()
        for destination in thrown.keys():
            monkeys[destination].catch_items(thrown[destination])
        if log:
            print("Monkey %d inspected items %d times" % (key, monkey.inspected_count))
    if log:
        print()

active = sorted([monkey.inspected_count for monkey in monkeys.values()], reverse=True)
part_one = active[0] * active[1]
print("Part One: %d" % part_one)
