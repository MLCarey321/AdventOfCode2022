import re
from copy import deepcopy


def calculate_pressure_released(route, limit=30):
    released = 0
    for i, n in enumerate(route):
        if isinstance(n, int):
            released += n * (limit - (i + 1))
    return released


def get_route_string(route):
    return "".join([str(v) for v in route])


pattern = r"^Valve (?P<start>\S+) has flow rate=(?P<flow_rate>.+); tunnel(s?) lead(s?) to valve(s?) (?P<valves>.+)$"
with open("day16.txt") as reader:
    lines = reader.readlines()

valves = {}
shortest_paths = {}
for line in lines:
    match = re.match(pattern, line.strip())
    if match:
        d = match.groupdict()
        valve = d["start"]
        valves[valve] = int(d["flow_rate"])
        shortest_paths[valve] = {valve: []}
        for neighbor in d["valves"].split(", "):
            shortest_paths[valve].update({neighbor: [neighbor]})

for k in valves.keys():
    for i in valves.keys():
        if k not in shortest_paths[i].keys():
            continue
        ik = shortest_paths[i][k]
        for j in valves.keys():
            if j not in shortest_paths[k].keys():
                continue
            kj = shortest_paths[k][j]
            if j not in shortest_paths[i] or len(shortest_paths[i][j]) > len(ik) + len(kj):
                shortest_paths[i][j] = ik + kj
valuable_valves = sorted([v for v in valves.keys() if valves[v] > 0], key=lambda k: valves[k], reverse=True)
print(valuable_valves)

max_released = 0
branches = [([], [])]
while len(branches) > 0:
    (route, opened) = branches.pop(0)
    route_released = calculate_pressure_released(route)
    if max_released < route_released:
        max_released = route_released
    to_open = [v for v in valuable_valves if v not in opened]
    last = "AA" if len(route) == 0 else route[-2]
    for valve in to_open:
        seg = shortest_paths[last][valve]
        if len(route) + len(seg) + 1 < 30:
            new_route = deepcopy(route)
            new_opened = deepcopy(opened)
            new_route += seg
            new_route.append(valves[valve])
            new_opened.append(valve)
            branches.append((new_route, new_opened))
print("Part One: %d" % max_released)

max_released = 0
branches = [([], [], [])]
seen_routes = set()
while len(branches) > 0:
    (route1, route2, opened) = branches.pop(0)
    route_released = calculate_pressure_released(route1, 26) + calculate_pressure_released(route2, 26)
    if max_released < route_released:
        print("New max of %d from routes:\n\t%s\n\t%s" % (route_released, str(route1), str(route2)))
        max_released = route_released
    last1 = "AA" if len(route1) == 0 else route1[-2]
    last2 = "AA" if len(route2) == 0 else route2[-2]
    to_open = sorted([v for v in valuable_valves if v not in opened],
                     key=lambda k: valves[k] * (25 - (len(route1) + len(shortest_paths[last1][k]))), reverse=True)
    new_branches = []
    for valve1 in to_open:
        seg = shortest_paths[last1][valve1]
        if len(route1) + len(seg) + 1 < 26:
            new_route1 = deepcopy(route1)
            new_opened = deepcopy(opened)
            new_route1 += seg
            new_route1.append(valves[valve1])
            new_opened.append(valve1)
            route_str_1 = get_route_string(new_route1)
            route_str_2 = get_route_string(route2)
            if (route_str_1, route_str_2) not in seen_routes:
                seen_routes.update((route_str_1, route_str_2))
                seen_routes.update((route_str_2, route_str_1))
                new_branches.append((new_route1, deepcopy(route2), new_opened))
                to_open_next = sorted([v for v in to_open if v != valve1],
                                      key=lambda k: valves[k] * (25 - (len(route2) + len(shortest_paths[last2][k]))),
                                      reverse=True)
                for valve2 in to_open_next:
                    seg = shortest_paths[last2][valve2]
                    if len(route2) + len(seg) + 1 < 26:
                        new_route2 = deepcopy(route2)
                        new_opened = deepcopy(opened)
                        new_route2 += seg
                        new_route2.append(valves[valve2])
                        new_opened.append(valve1)
                        new_opened.append(valve2)
                        route_str_2 = get_route_string(new_route2)
                        if (route_str_1, route_str_2) not in seen_routes:
                            seen_routes.update((route_str_1, route_str_2))
                            seen_routes.update((route_str_2, route_str_1))
                            new_branches.append((new_route1, new_route2, new_opened))
    branches = new_branches + branches
print("Part Two: %d" % max_released)
