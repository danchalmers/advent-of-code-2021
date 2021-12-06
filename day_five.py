from collections import Counter
from typing import Iterable
from pipe import map, where, chain


TEST_FILE = 'test-5.txt'
REAL_FILE = "input-5.txt"

Coord = tuple[int, int]


def _read_file(file_name: str) -> Iterable[str]:
    with open('data/' + file_name, 'r') as f:
        for line in f.readlines():
            if len(line) > 0:
                yield line


def _pair_from_str(pair_text: str) -> Coord:
    xy = pair_text.strip().split(',')
    return int(xy[0]), int(xy[1])


def _make_line(end1: Coord, end2: Coord) -> list[Coord]:
    x_step = 1 if end1[0] < end2[0] else -1
    y_step = 1 if end1[1] < end2[1] else -1
    if end1[0] == end2[0]:
        return [(end1[0], y) for y in range(end1[1], end2[1]+y_step, y_step)]
    elif end1[1] == end2[1]:
        return [(x, end1[1]) for x in range(end1[0], end2[0]+x_step, x_step)]
    else:
        return [
            (xy[0], xy[1])
            for xy in zip(range(end1[0], end2[0]+x_step, x_step), range(end1[1], end2[1]+y_step, y_step))
        ]


def _file_to_points(file_name: str) -> list[tuple[Coord]]:
    return list(
        _read_file(file_name)
        | map(lambda line: line.split('->'))
        | map(lambda pairs: list(
            pairs
            | map(lambda pair: _pair_from_str(pair))
        ))
    )


def _count_to_intersections(point_count: Counter) -> int:
    point_count.subtract(set(point_count))
    point_count = +point_count
    intersections = len(point_count)
    print(f"{intersections} intersections found")
    return intersections


def count_xy_intersections(file_name: str) -> int:
    point_count = Counter(
        _file_to_points(file_name)
        | where(lambda pairs: pairs[0][0] == pairs[1][0] or pairs[0][1] == pairs[1][1])
        | map(lambda pairs: _make_line(pairs[0], pairs[1]))
        | chain
    )
    return _count_to_intersections(point_count)


def count_all_intersections(file_name: str) -> int:
    point_count = Counter(
        _file_to_points(file_name)
        | map(lambda pairs: _make_line(pairs[0], pairs[1]))
        | chain
    )
    return _count_to_intersections(point_count)


if __name__ == "__main__":
    count_xy_intersections(REAL_FILE)
    count_all_intersections(REAL_FILE)
