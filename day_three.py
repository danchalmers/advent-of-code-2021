from pipe import map

import operator


TEST_FILE = 'test-3.txt'
REAL_FILE = 'input-3.txt'

VALUE = int
BIT_WIDTH = int


def _bin_lines(file_name: str) -> tuple[list[VALUE], BIT_WIDTH]:
    lines = []
    with open('data/' + file_name, 'r') as f:
        for line in f.readlines():
            if line:
                lines.append(int(line, 2))
            bit_width = len(line.strip())
    return lines, bit_width


def count_bits(input: list[VALUE], position: int) -> int:
    mask = 2**position
    return sum(input | map (lambda x: (x & mask) >> position))


def gamma(input: list[VALUE], bit_width: BIT_WIDTH) -> int:
    half_lines = len(input) / 2
    gamma = 0
    for i in range(bit_width):
        if count_bits(input, i) > half_lines:
            gamma += 2**i
    return gamma


def day_three_part_one(file_name: str) -> int:
    lines, bit_width = _bin_lines(file_name)
    print(f"{len(lines)} lines of width {bit_width}")
    g = gamma(lines, bit_width)
    epsilon = 2**bit_width + ~g
    return g * epsilon


def count_filter(input: list[VALUE], bit_width: BIT_WIDTH, op: operator):
    position = bit_width - 1
    remainder = input
    while position >= 0 and len(remainder) > 1:
        half_remainder = len(remainder) / 2
        mask = 2**position
        if op(count_bits(remainder, position), half_remainder):
            remainder = [x for x in remainder if x & mask == mask]
        else:
            remainder = [x for x in remainder if x & mask == 0]
        position -= 1
    return remainder[0]


def day_three_part_two(file_name: str):
    lines, bit_width = _bin_lines(file_name)
    oxygen = count_filter(lines, bit_width, operator.ge)
    co2 = count_filter(lines, bit_width, operator.lt)
    return oxygen * co2


if __name__ == "__main__":
    print(day_three_part_two(REAL_FILE))
