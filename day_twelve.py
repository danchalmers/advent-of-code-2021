from __future__ import annotations

from collections import defaultdict, Counter
from typing import Iterable, Union

from pipe import where, map, t, traverse, tee, chain

REAL_FILE = 'input-12.txt'

CaveName = str
CaveMap = dict[CaveName, list[CaveName]]
CavePaths = Union[None, CaveName, list['CavePaths']]


def make_map(defs: Iterable[str]) -> CaveMap:
    caves = defaultdict(list)
    for line in defs:
        line = line.strip()
        if len(line) == 0:
            continue
        from_to = line.split('-')
        caves[from_to[0]].append(from_to[1])
        caves[from_to[1]].append(from_to[0])
    print(f"cave has {len(caves)} caves: {caves.keys()}")
    return caves


def find_paths_part_one_from(cave_map: CaveMap, start_from: CaveName, path_so_far: list[CaveName]) -> CavePaths:
    if start_from == 'end':
        return ['end']
    prev_from_here = [y for x, y in zip(path_so_far, path_so_far[1:]) if x == start_from]
    prev_small = [x for x in path_so_far if x[0].islower()]
    paths = list(
        cave_map[start_from]
        | where(lambda dest: dest not in prev_from_here)
        | where(lambda dest: dest not in prev_small)
        | map(lambda f: find_paths_part_one_from(cave_map, f, path_so_far + [start_from]))
    )
    paths = start_from | t(paths)
    return paths


def _one_prev_small_can_be_two(prev_small, dest):
    twos = [x for x, c in prev_small.items() if c == 2]
    dest_will_be_two = prev_small[dest] == 1
    if dest_will_be_two:
        return len(twos) == 0
    else:
        return len(twos) <= 1


def find_paths_part_two_from(cave_map: CaveMap, start_from: CaveName, path_so_far: list[CaveName]) -> CavePaths:
    if start_from == 'end':
        return 'end'
    prev_small = Counter([x for x in path_so_far if x[0].islower()])
    if len([x for x, c in prev_small.items() if c >= 2]) > 1:
        return None
    paths = list(
        cave_map[start_from]
        | where(lambda dest: prev_small[dest] <= 1 and dest != 'start')
        | where(lambda dest: _one_prev_small_can_be_two(prev_small, dest))
        | map(lambda f: find_paths_part_two_from(cave_map, f, path_so_far + [start_from]))
        | where(lambda ps: ps is not None)
    )
    paths = list(start_from | t(paths))
    if 'end' in list(paths | traverse):
        return paths


def _count_paths(paths: CavePaths) -> int:
    count = len(list(
        paths
        | traverse
        | where (lambda n: n == 'end')
    ))
    print(f"found {count} paths")
    return count


def count_paths_part_one(defs: Iterable[str]) -> int:
    print("part one")
    cave_map = make_map(defs)
    paths = find_paths_part_one_from(cave_map, 'start', [])
    return _count_paths(paths)


def count_paths_part_two(defs: Iterable[str]) -> int:
    print("part two")
    cave_map = make_map(defs)
    paths = find_paths_part_two_from(cave_map, 'start', [])
    print(paths)
    return _count_paths(paths)


def load_count_paths(file_name: str):
    lines = []
    with open('data/' + file_name, 'r') as f:
        for line in f.readlines():
            lines.append(line)
    count_paths_part_one(lines)
    count_paths_part_two(lines)


if __name__ == "__main__":
    load_count_paths(REAL_FILE)
