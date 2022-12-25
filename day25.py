total = 0
decoder = {"=": -2, "-": -1, "0": 0, "1": 1, "2": 2}
encoder = {-2: "=", -1: "-", 0: "0", 1: "1", 2: "2"}
for line in open("day25.txt"):
    digits = list(reversed(line.strip()))
    for i, digit in enumerate(digits):
        total += decoder[digit] * pow(5, i)
exp = 0
while total >= pow(5, exp+1):
    exp += 1
snafu = []
while exp >= 0:
    denominator = pow(5, exp)
    ceil = sum([2 * pow(5, n) for n in range(exp)])
    floor = sum([-2 * pow(5, n) for n in range(exp)])
    options = [k for k in encoder.keys() if floor <= total - (denominator * k) <= ceil]
    snafu.append(encoder[max(options)])
    total -= (denominator * max(options))
    exp -= 1
print("Part One: ", "".join(snafu))
