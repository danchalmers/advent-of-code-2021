import math
from collections import deque

from pipe import map, where, sort

from common import load_grid, AxisSize, Coordinate, Map, adjacents


Height = int

TEST_FILE = 'test-9.txt'
REAL_FILE = 'input-9.txt'


def possible_coords(x_size: AxisSize, y_size: AxisSize) -> list[Coordinate]:
    return [(x, y) for x in range(x_size) for y in range(y_size)]


def is_low_point(floor_map: Map, loc: Coordinate, adjs: list[Coordinate]):
    x, y = loc[0], loc[1]
    return all([floor_map[ay][ax] > floor_map[y][x] for (ax, ay) in adjs])


def risk_level(height: Height) -> int:
    return 1 + height


def part_one(floor_map: Map, x_size: AxisSize, y_size: AxisSize):
    risk = sum(
        possible_coords(x_size, y_size)
        | where(lambda loc: is_low_point(floor_map, loc, adjacents(loc, x_size, y_size)))
        | map(lambda loc: floor_map[loc[1]][loc[0]])
        | map(lambda height: risk_level(height))
    )
    print(f"risk level {risk}")


def baisin(floor_map: Map, x_size: AxisSize, y_size: AxisSize, low_point: Coordinate) -> list[Coordinate]:
    result = []
    work_queue = deque([low_point])
    while work_queue:
        consider = work_queue.pop()
        if floor_map[consider[1]][consider[0]] != 9 and consider not in result:
            work_queue.extend(list(adjacents(consider, x_size, y_size)))
            result.append(consider)
    return result


def part_two(floor_map: Map, x_size: AxisSize, y_size: AxisSize):
    prod = math.prod(list(
        possible_coords(x_size, y_size)
        | where(lambda loc: is_low_point(floor_map, loc, adjacents(loc, x_size, y_size)))
        | map(lambda low_point: len(baisin(floor_map, x_size, y_size, low_point)))
        | sort(reverse=True)
    )[0:3])
    print(f"product of three largest is {prod}")


if __name__ == "__main__":
    floor_map, x_size, y_size = load_grid(REAL_FILE)
    part_one(floor_map, x_size, y_size)
    part_two(floor_map, x_size, y_size)
