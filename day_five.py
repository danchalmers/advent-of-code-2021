from collections import Counter
from typing import Iterable
from pipe import map, where, chain


TEST_FILE = 'test-5.txt'
REAL_FILE = "input-5.txt"


def _read_file(file_name: str) -> Iterable[str]:
    with open('data/' + file_name, 'r') as f:
        for line in f.readlines():
            if len(line) > 0:
                yield line


def _pair_from_str(pair_text: str) -> tuple[int, int]:
    xy = pair_text.strip().split(',')
    return int(xy[0]), int(xy[1])


def _make_line(end1: tuple[int, int], end2: tuple[int, int]) -> list[tuple[int, int]]:
    if end1[0] == end2[0]:
        return [(end1[0], y) for y in range(min(end1[1], end2[1]), max(end1[1], end2[1])+1)]
    else:
        return [(x, end1[1]) for x in range(min(end1[0], end2[0]), max(end1[0], end2[0])+1)]


def _make_line_part2(end1: tuple[int, int], end2: tuple[int, int]) -> list[tuple[int, int]]:
    if end1[0] == end2[0]:
        return [(end1[0], y) for y in range(min(end1[1], end2[1]), max(end1[1], end2[1])+1)]
    elif end1[1] == end2[1]:
        return [(x, end1[1]) for x in range(min(end1[0], end2[0]), max(end1[0], end2[0])+1)]
    else:
        x_step = 1 if end1[0] < end2[0] else -1
        y_step = 1 if end1[1] < end2[1] else -1
        return [(xy[0], xy[1])
                for xy in zip(range(end1[0], end2[0]+x_step, x_step), range(end1[1], end2[1]+y_step, y_step))
                ]


def count_xy_intersections(file_name: str) -> int:
    point_count = Counter(
        _read_file(file_name)
        | map(lambda line: line.split('->'))
        | map(lambda pairs: list(
            pairs
            | map(lambda pair: _pair_from_str(pair))
        ))
        | where(lambda pairs: pairs[0][0] == pairs[1][0] or pairs[0][1] == pairs[1][1])
        | map(lambda pairs: _make_line(pairs[0], pairs[1]))
        | chain
    )
    point_count.subtract(set(point_count))
    point_count = +point_count
    intersections = len(point_count)
    print(f"{intersections} intersections found")
    return intersections


def count_all_intersections(file_name: str) -> int:
    point_count = Counter(
        _read_file(file_name)
        | map(lambda line: line.split('->'))
        | map(lambda pairs: list(
            pairs
            | map(lambda pair: _pair_from_str(pair))
        ))
        | map(lambda pairs: _make_line_part2(pairs[0], pairs[1]))
        | chain
    )
    point_count.subtract(set(point_count))
    point_count = +point_count
    intersections = len(point_count)
    print(f"{intersections} intersections found")
    return intersections


if __name__ == "__main__":
    # count_xy_intersections(REAL_FILE)
    count_all_intersections(REAL_FILE)
