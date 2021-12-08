from collections import Counter
from typing import Iterable
from pipe import map, where, chain, sort, traverse


TEST_FILE = 'test-8.txt'
REAL_FILE = 'input-8.txt'


def read_inputs(file_name: str) -> Iterable[tuple[list[str], list[str]]]:
    with open('data/' + file_name, 'r') as f:
        for line in f.readlines():
            if len(line) > 0:
                patterns_output = line.split('|')[0:2]
                yield patterns_output[0].split(), patterns_output[1].split()


def unique_decode_one(x: str) -> int:
    match len(x):
        case 2:
            return 1
        case 4:
            return 4
        case 3:
            return 7
        case 7:
            return 8


def part_one_decode_outputs(outputs: list[str]):
    return list(
        outputs
        | map(lambda out: unique_decode_one(out))
        | where(lambda out: out is not None)
    )


def decode_one(decoding: dict[list[str], int], to_decode: list[str]):
    return str(decoding[''.join(to_decode)])


def patterns_to_sorted_list(patterns: list[str]) -> list[list[str]]:
    return list(patterns | map(lambda p: (list(p.strip()) | sort)))


def build_decoding(patterns: list[str]) -> dict[list[str], int]:
    encoding = {unique_decode_one(p): p for p in patterns | where(lambda p: len(p) in [2,4,3,7])}
    # the five segment digits have unique combinations of segments b and e
    letter_counts = Counter(list(patterns | traverse))
    b = [l for l, c in letter_counts.items() if c == 6][0]
    e = [l for l, c in letter_counts.items() if c == 4][0]
    five_segments = list(p for p in patterns | where(lambda p: len(p) == 5))
    encoding[2] = list(five_segments | where(lambda p: e in p))[0]
    encoding[5] = list(five_segments | where(lambda p: b in p))[0]
    encoding[3] = list(five_segments | where(lambda p: e not in p and b not in p))[0]
    # the six segment digits can be reduced by what other numbers they contain
    six_segments  = list(p for p in patterns | where(lambda p: len(p) == 6))
    encoding[9] = list(six_segments
                       | where(lambda p: all([b in p for b in encoding[4]]))
                       )[0]
    encoding[0] = list(six_segments
                       | where(lambda p: all([b in p for b in encoding[1]]))
                       | where(lambda p: p not in encoding.values())
                       )[0]
    encoding[6] = list(six_segments
                       | where(lambda p: p not in encoding.values())
                       )[0]
    decoding = {''.join(v): k for k, v in encoding.items()}
    return decoding


def decode_outputs(patterns: list[str], outputs: list[str]):
    patterns = patterns_to_sorted_list(patterns)
    outputs = patterns_to_sorted_list(outputs)
    decoding = build_decoding(patterns)
    digits = list(
        outputs
        | map(lambda out: decode_one(decoding, out))
        | chain
    )
    return int(''.join(digits))


def do_part_one(file_name: str) -> int:
    count_decoded = len(list(
        read_inputs(file_name)
        | map(lambda pattern_output: part_one_decode_outputs(pattern_output[1]))
        | chain
    ))
    print(f"part one decoded {count_decoded}")
    return count_decoded


def do_part_two(file_name: str) -> int:
    count_decoded = sum(list(
        read_inputs(file_name)
        | map(lambda pattern_output: decode_outputs(pattern_output[0], pattern_output[1]))
    ))
    print(f"part two decoded sum {count_decoded}")
    return count_decoded


if __name__ == "__main__":
    # do_part_one(TEST_FILE)
    do_part_two(REAL_FILE)
