with open("day06.txt") as reader:
    buffer = reader.readline()

index = 0
while len(set(buffer[index:index+4])) < 4:
    index += 1

print("Part One: %d" % (index + 4))

index = 0
while len(set(buffer[index:index+14])) < 14:
    index += 1

print("Part Two: %d" % (index + 14))
