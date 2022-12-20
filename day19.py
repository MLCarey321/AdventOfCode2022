import re
import numpy


def recurse(minute, ore_data, clay_data, obsidian_data, geode_data, time_limit=24):
    global ore_for_ore, ore_for_clay, ore_for_obsidian, ore_for_geode, clay_for_obsidian, obsidian_for_geode, seen
    if minute == time_limit:
        return geode_data[0]
    seen_key = (minute, ore_data, clay_data, obsidian_data, geode_data)
    if seen_key in seen.keys():
        return seen[seen_key]
    if ore_data[0] >= ore_for_geode and obsidian_data[0] >= obsidian_for_geode:
        best = recurse(minute + 1, (ore_data[0] + ore_data[1] - ore_for_geode, ore_data[1]),
                       (clay_data[0] + clay_data[1], clay_data[1]),
                       (obsidian_data[0] + obsidian_data[1] - obsidian_for_geode, obsidian_data[1]),
                       (geode_data[0] + geode_data[1], geode_data[1] + 1), time_limit)
        seen[seen_key] = best
        return best
    if ore_data[0] >= ore_for_obsidian and clay_data[0] >= clay_for_obsidian and \
            obsidian_data[1] < obsidian_for_geode:
        best = recurse(minute + 1, (ore_data[0] + ore_data[1] - ore_for_obsidian, ore_data[1]),
                       (clay_data[0] + clay_data[1] - clay_for_obsidian, clay_data[1]),
                       (obsidian_data[0] + obsidian_data[1], obsidian_data[1] + 1),
                       (geode_data[0] + geode_data[1], geode_data[1]), time_limit)
        seen[seen_key] = best
        return best
    best = recurse(minute + 1, (ore_data[0] + ore_data[1], ore_data[1]),
                   (clay_data[0] + clay_data[1], clay_data[1]),
                   (obsidian_data[0] + obsidian_data[1], obsidian_data[1]),
                   (geode_data[0] + geode_data[1], geode_data[1]), time_limit)
    if ore_data[0] >= ore_for_clay and clay_data[1] < clay_for_obsidian:
        best = max(best, recurse(minute + 1, (ore_data[0] + ore_data[1] - ore_for_clay, ore_data[1]),
                                 (clay_data[0] + clay_data[1], clay_data[1] + 1),
                                 (obsidian_data[0] + obsidian_data[1], obsidian_data[1]),
                                 (geode_data[0] + geode_data[1], geode_data[1]), time_limit))
    if ore_data[0] >= ore_for_ore and time_limit - minute > ore_for_ore and \
            ore_data[1] < max([ore_for_ore, ore_for_clay, ore_for_obsidian, ore_for_geode]):
        best = max(best, recurse(minute + 1, (ore_data[0] + ore_data[1] - ore_for_ore, ore_data[1] + 1),
                                 (clay_data[0] + clay_data[1], clay_data[1]),
                                 (obsidian_data[0] + obsidian_data[1], obsidian_data[1]),
                                 (geode_data[0] + geode_data[1], geode_data[1]), time_limit))
    seen[seen_key] = best
    return best


pattern = r"Blueprint (?P<id>.+): Each ore robot costs (?P<ore_for_ore>.+) ore. " \
          r"Each clay robot costs (?P<ore_for_clay>.+) ore. " \
          r"Each obsidian robot costs (?P<ore_for_obsidian>.+) ore and (?P<clay_for_obsidian>.+) clay. " \
          r"Each geode robot costs (?P<ore_for_geode>.+) ore and (?P<obsidian_for_geode>.+) obsidian."
with open("day19.txt") as reader:
    lines = reader.readlines()

blueprints = []
for line in lines:
    match = re.match(pattern, line.strip())
    if match:
        blueprints.append(dict((k, int(v)) for (k, v) in match.groupdict().items()))

bp_geodes = {}
for bp in blueprints:
    bp_id = bp["id"]
    ore_for_ore = bp["ore_for_ore"]
    ore_for_clay = bp["ore_for_clay"]
    ore_for_obsidian = bp["ore_for_obsidian"]
    clay_for_obsidian = bp["clay_for_obsidian"]
    ore_for_geode = bp["ore_for_geode"]
    obsidian_for_geode = bp["obsidian_for_geode"]
    seen = {}
    geode_count = recurse(0, (0, 1), (0, 0), (0, 0), (0, 0))
    print(geode_count)
    bp_geodes[bp_id] = geode_count
print("Part One: %d" % sum(k * v for (k, v) in bp_geodes.items()))

bp_geodes = {}
for bp in blueprints[:3]:
    bp_id = bp["id"]
    ore_for_ore = bp["ore_for_ore"]
    ore_for_clay = bp["ore_for_clay"]
    ore_for_obsidian = bp["ore_for_obsidian"]
    clay_for_obsidian = bp["clay_for_obsidian"]
    ore_for_geode = bp["ore_for_geode"]
    obsidian_for_geode = bp["obsidian_for_geode"]
    seen = {}
    geode_count = recurse(0, (0, 1), (0, 0), (0, 0), (0, 0), 32)
    print(geode_count)
    bp_geodes[bp_id] = geode_count
print("Part Two: %d" % numpy.prod(list(bp_geodes.values())))
