with open("day01.txt") as reader:
    lines = reader.readlines()

elves = {}
elf = 1
calorieCount = 0
for line in lines:
    if len(line.strip()) == 0:
        elves[elf] = calorieCount
        elf += 1
        calorieCount = 0
    else:
        calorieCount += int(line)
elves[elf] = calorieCount

loads = sorted(elves.values())[-3:]

print("Part One: %d" % loads[-1])

print("Part Two: %d" % sum(loads))
