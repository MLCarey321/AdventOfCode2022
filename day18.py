def get_adjacent_to_tuple(tup):
    return [(tup[0] + 1, tup[1], tup[2]), (tup[0] - 1, tup[1], tup[2]),
            (tup[0], tup[1] + 1, tup[2]), (tup[0], tup[1] - 1, tup[2]),
            (tup[0], tup[1], tup[2] + 1), (tup[0], tup[1], tup[2] - 1)]


def get_surface_area():
    global cubes
    surface_area = len(cubes) * 6
    for i in range(len(cubes)):
        cube1 = cubes[i]
        for k in range(i + 1, len(cubes)):
            cube2 = cubes[k]
            x_diff = abs(cube1[0] - cube2[0])
            y_diff = abs(cube1[1] - cube2[1])
            z_diff = abs(cube1[2] - cube2[2])
            if x_diff + y_diff + z_diff == 1:
                surface_area -= 2
    return surface_area


with open("day18.txt") as reader:
    lines = reader.readlines()

cubes = []
for line in lines:
    cubes.append(tuple(map(int, line.strip().split(","))))

print("Part One: %d" % get_surface_area())

x_vals = set([x for (x, y, z) in cubes])
y_vals = set([y for (x, y, z) in cubes])
z_vals = set([z for (x, y, z) in cubes])
left = min(x_vals) - 1
right = max(x_vals) + 1
top = min(y_vals) - 1
bottom = max(y_vals) + 1
near = min(z_vals) - 1
far = max(z_vals) + 1
branches = [(min(x_vals), min(y_vals), min(z_vals))]
outside = []
while len(branches) > 0:
    cube = branches.pop()
    outside.append(cube)
    for adj in get_adjacent_to_tuple(cube):
        if left <= adj[0] <= right and top <= adj[1] <= bottom and near <= adj[2] <= far and \
                adj not in outside and adj not in cubes:
            branches.append(adj)

for x in range(left + 1, right):
    for y in range(top + 1, bottom):
        for z in range(near + 1, far):
            pos = (x, y, z)
            if pos not in cubes and pos not in outside:
                cubes.append(pos)

print("Part Two: %d" % get_surface_area())
