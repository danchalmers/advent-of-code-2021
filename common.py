from collections import defaultdict
from functools import lru_cache
from operator import xor
from typing import TypeVar

from pipe import permutations, map, where


Count = int

MapParam = TypeVar('MapParam')
AxisSize = int
Location = int
Coordinate = tuple[Location, Location]
Map = list[list[MapParam]]


def count_values_in_file_list(file_name: str) -> dict[int, int]:
    pos_count = defaultdict(int)
    with open('data/' + file_name, 'r') as f:
        for x in f.readline().split(','):
            pos_count[int(x)] += 1
    return pos_count


def load_grid(file_name: str, path: str = 'data/') -> tuple[Map, AxisSize, AxisSize]:
    rows = []
    with open(path + file_name, 'r') as f:
        for line in f.readlines():
            rows.append([int(c) for c in line if c.isdigit()])
    return rows, len(rows[0]), len(rows)


@lru_cache
def adjacents(loc: Coordinate, x_size: AxisSize, y_size: AxisSize) -> list[Coordinate]:
    x, y = loc[0], loc[1]
    return list(
        [-1, 0, 1]
        | permutations(2)
        | map(lambda xy: (xy[0] + x, xy[1] + y))
        | where(lambda xy: xor(xy[0] == x, xy[1] == y))
        | where(lambda xy: all([z >= 0 for z in xy]))
        | where(lambda xy: xy[0] < x_size and xy[1] < y_size)
    )


@lru_cache()
def triangular_number(x: int) -> int:
    return (x * (x + 1)) / 2
