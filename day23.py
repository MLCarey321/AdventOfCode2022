def get_adjacent_positions(pos):
    (x, y) = pos
    return [(x-1, y-1), (x-1, y), (x-1, y+1), (x, y-1), (x, y+1), (x+1, y-1), (x+1, y), (x+1, y+1)]


def get_north_positions(pos):
    (x, y) = pos
    return [(x-1, y-1), (x, y-1), (x+1, y-1)]


def get_south_positions(pos):
    (x, y) = pos
    return [(x-1, y+1), (x, y+1), (x+1, y+1)]


def get_west_positions(pos):
    (x, y) = pos
    return [(x-1, y-1), (x-1, y), (x-1, y+1)]


def get_east_positions(pos):
    (x, y) = pos
    return [(x+1, y-1), (x+1, y), (x+1, y+1)]


def pretty_print():
    global elves
    exes = [x for (x, y) in elves]
    whys = [y for (x, y) in elves]
    for y in range(min(whys)-1, max(whys)+2):
        for x in range(min(exes)-1, max(exes)+2):
            print("#" if (x, y) in elves else ".", end="")
        print()
    print()


elves = []
for y, line in enumerate(open("day23.txt")):
    for x, char in enumerate(line.strip()):
        if char == "#":
            elves.append((x, y))
spaced = False
count = 0
direction = {0: get_north_positions, 1: get_south_positions, 2: get_west_positions, 3: get_east_positions}
while not spaced:
    unspaced = []
    for elf in elves:
        adj = get_adjacent_positions(elf)
        if len(set(adj) - set(elves)) < 8:
            unspaced.append(elf)
    if len(unspaced) == 0:
        spaced = True
    else:
        new_elves = [elf for elf in elves if elf not in unspaced]
        proposed = {}
        for elf in unspaced:
            for c in range(4):
                consider = direction[(count + c) % 4](elf)
                if len(set(consider) - set(elves)) == 3:
                    proposed[elf] = consider[1]
                    break
            if elf not in proposed.keys():
                new_elves.append(elf)
        for elf in proposed.keys():
            new_pos = proposed[elf]
            if len([v for v in proposed.values() if v == new_pos]) > 1:
                new_elves.append(elf)
            else:
                new_elves.append(new_pos)
        elves = new_elves
        count += 1
        if count == 10:
            exes = [x for (x, y) in elves]
            whys = [y for (x, y) in elves]
            width = max(exes) - min(exes) + 1
            height = max(whys) - min(whys) + 1
            size = (width * height) - len(elves)
            print("Part One: %d" % size)
        if count % 100 == 0:
            print("Round %d" % count)
            pretty_print()
pretty_print()
print("Part Two: %d" % (count+1))
