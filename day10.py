with open("day10.txt") as reader:
    lines = reader.readlines()

x = 1
index = 2
register_cycles = {1: 1}
for line in lines:
    register_cycles.update({index: x})
    index += 1
    if line.startswith("addx"):
        register_cycles.update({index: x})
        (addx, amount) = line.strip().split()
        x += int(amount)
        register_cycles.update({index: x})
        index += 1

part_one = sum([n * register_cycles[n] for n in [20, 60, 100, 140, 180, 220]])
print("Part One: %d" % part_one)

screen = []
for cycles in range(240):
    pixel = cycles % 40
    sprite = register_cycles[cycles+1]
    screen.append("#" if pixel - 1 <= sprite <= pixel + 1 else ".")

print("Part Two:")
for row in range(6):
    print("".join(screen[row*40:(row+1)*40]))
