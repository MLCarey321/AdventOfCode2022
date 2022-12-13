class Packet:
    def __init__(self, contents):
        self.content = contents

    def __lt__(self, other):
        return Packet.compare(self.content, other.content)

    @staticmethod
    def compare(left_packet, right_packet):
        for p, l_elem in enumerate(left_packet):
            if p >= len(right_packet):
                return False
            r_elem = right_packet[p]
            if isinstance(l_elem, int):
                if isinstance(r_elem, int):
                    if l_elem < r_elem:
                        return True
                    if l_elem > r_elem:
                        return False
                elif isinstance(r_elem, list):
                    nested = Packet.compare([l_elem], r_elem)
                    if nested is not None:
                        return nested
            elif isinstance(l_elem, list):
                nested = True
                if isinstance(r_elem, int):
                    nested = Packet.compare(l_elem, [r_elem])
                elif isinstance(r_elem, list):
                    nested = Packet.compare(l_elem, r_elem)
                if nested is not None:
                    return nested
        if len(left_packet) < len(right_packet):
            return True
        return None


with open("day13.txt") as reader:
    lines = reader.readlines()

packets = [Packet(eval(line.strip())) for line in lines if len(line.strip()) > 0]
part_one = 0
for i, packet in enumerate(packets):
    if i % 2 == 1:
        continue
    elif packet < packets[i+1]:
        part_one += ((i // 2) + 1)

print("Part One: %d" % part_one)

div1 = Packet([[2]])
div2 = Packet([[6]])
packets += [div1, div2]
packets.sort()
i1 = packets.index(div1) + 1
i2 = packets.index(div2) + 1

print("Part Two: %d" % (i1 * i2))
