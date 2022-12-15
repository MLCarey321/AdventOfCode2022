import re


class Graph:
    class Sensor:
        def __init__(self, coord, beacon_coord):
            self.coord = coord
            self.beacon_coord = beacon_coord
            self.manhattan = abs(coord[0] - beacon_coord[0]) + abs(coord[1] - beacon_coord[1])

        def get_coords_in_range_on_row(self, row):
            coords = []
            x_diff = self.manhattan - abs(self.coord[1] - row)
            for x in range(self.coord[0] - x_diff, self.coord[0] + x_diff):
                coords.append((x, row))
            return coords

        def get_coord_ranges_in_grid_for_size(self, size):
            row_ranges = {}
            y_min = max(0, self.coord[1] - self.manhattan)
            y_max = min(size, self.coord[1] + self.manhattan)
            for y in range(y_min, y_max):
                x_diff = self.manhattan - abs(self.coord[1] - y)
                x_min = max(0, self.coord[0] - x_diff)
                x_max = min(size, self.coord[0] + x_diff)
                row_ranges.update({y: (x_min, x_max)})
            return row_ranges

    def __init__(self):
        self.sensors = []
        self.beacons = []

    def add_sensor(self, sensor_coord, closest_beacon_coord):
        new_sensor = Graph.Sensor(sensor_coord, closest_beacon_coord)
        self.sensors.append(new_sensor)
        self.beacons.append(closest_beacon_coord)

    def get_covered_count_for_row(self, row):
        relevant = [s for s in self.sensors if s.coord[1] - s.manhattan <= row <= s.coord[1] + s.manhattan]
        relevant_coords = set(self.beacons)
        relevant_coords.update([s.coord for s in self.sensors])
        for sensor in relevant:
            relevant_coords.update(sensor.get_coords_in_range_on_row(row))
        return len([c for c in relevant_coords if c[1] == row])

    def get_covered_count_for_grid(self, size):
        relevant = [s for s in self.sensors if s.coord[0] - s.manhattan <= size and s.coord[0] + s.manhattan >= 0]
        relevant = [s for s in relevant if s.coord[1] - s.manhattan <= size and s.coord[1] + s.manhattan >= 0]
        row_ranges = dict([(b[1], [(b[0], b[0])]) for b in self.beacons if 0 <= b[0] <= size and 0 <= b[1] <= size])
        for sensor in relevant:
            new_ranges = sensor.get_coord_ranges_in_grid_for_size(size)
            for row in new_ranges.keys():
                if row not in row_ranges.keys():
                    row_ranges.update({row: [new_ranges[row]]})
                elif row_ranges[row] != [(0, size)]:
                    row_ranges[row] = Graph.merge_ranges(row_ranges[row], new_ranges[row])
        rows = [r for r in row_ranges.keys() if len(row_ranges[r]) > 1]
        if len(rows) != 1:
            print("Error! Should be 1 and only 1 gap!")
            return -1
        row = rows[0]
        cols = sorted(row_ranges[row], key=lambda c: c[0])
        if len(cols) != 2:
            print("Error! Should be 1 and only 1 gap!")
            return -1
        cols = list(range(cols[0][1] + 1, cols[1][0]))
        if len(cols) != 1:
            print("Error! Should be 1 and only 1 gap!")
            return -1
        col = cols[0]
        return (col * 4000000) + row

    @staticmethod
    def merge_ranges(old, new):
        mergable = [r for r in old if new[0] <= r[0] <= new[1] + 1 or new[0] - 1 <= r[1] <= new[1] or
                    r[0] <= new[0] <= r[1] + 1 or r[0] - 1 <= new[1] <= r[1]]
        ret = [o for o in old if o not in mergable]
        (low, high) = new
        for m in mergable:
            low = min(low, m[0])
            high = max(high, m[1])
        ret.append((low, high))
        return ret


input_pattern = r"^Sensor at x=(?P<sensor_x>.+), y=(?P<sensor_y>.+): closest beacon is at " \
                r"x=(?P<closest_x>.+), y=(?P<closest_y>.+)$"
graph = Graph()
with open("day15.txt") as reader:
    lines = reader.readlines()
for i, line in enumerate(lines):
    matcher = re.match(input_pattern, line.strip())
    if matcher:
        values = matcher.groupdict()
        graph.add_sensor((int(values["sensor_x"]), int(values["sensor_y"])),
                         (int(values["closest_x"]), int(values["closest_y"])))
print("Part One: %d" % graph.get_covered_count_for_row(2000000))
print("Part Two: %d" % graph.get_covered_count_for_grid(4000000))
