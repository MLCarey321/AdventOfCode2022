def get_part1_score(tup):
    them = ord("C") - ord(tup[0]) + 1
    me = ord(tup[1]) - ord("X") + 1
    result = ((them + me) % 3) * 3
    return me + result


def get_part2_score(tup):
    them = ord(tup[0]) - ord("A")
    result = ord(tup[1]) - ord("X")
    me = ((them + result - 1) % 3) + 1
    return me + (result * 3)


with open("day02.txt") as reader:
    lines = reader.readlines()

score1 = 0
score2 = 0
for line in lines:
    move = line.split()
    score1 += get_part1_score(move)
    score2 += get_part2_score(move)

print("Part One: %d" % score1)
print("Part Two: %d" % score2)
