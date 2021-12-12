from __future__ import annotations

from collections import defaultdict, Counter
from typing import Iterable, Union, Callable


REAL_FILE = 'input-12.txt'

CaveName = str
CaveMap = dict[CaveName, list[CaveName]]
CavePath = list[CaveName]


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


def find_paths_general(cave_map: CaveMap, max_small: int, fn: Callable, path_so_far: CavePath) -> list[CavePath]:
    result = []
    for dest in cave_map[path_so_far[-1]]:
        match dest:
            case 'end':
                result.append(path_so_far + [dest])
            case 'start':
                continue
            case _:
                if dest[0].isupper() or len([c for c in path_so_far if c == dest]) < max_small:
                    result.extend(fn(cave_map, path_so_far + [dest]))
    return result


def find_paths_part_one(cave_map: CaveMap, path_so_far: CavePath) -> list[CavePath]:
    return find_paths_general(cave_map, 1, find_paths_part_one, path_so_far)


def find_paths_part_two(cave_map: CaveMap, path_so_far: CavePath) -> list[CavePath]:
    small_counts = Counter([c for c in path_so_far if c[0].islower()])
    if len([s for s, c in small_counts.items() if c == 2]) > 1:
        return []
    else:
        return find_paths_general(cave_map, 2, find_paths_part_two, path_so_far)


def _count_paths(paths: list[list[CaveName]]) -> int:
    count = len(paths)
    print(f"found {count} paths")
    return count


def count_paths_part_one(defs: Iterable[str]) -> int:
    print("part one")
    cave_map = make_map(defs)
    paths = find_paths_part_one(cave_map, ['start'])
    return _count_paths(paths)


def count_paths_part_two(defs: Iterable[str]) -> int:
    print("part two")
    cave_map = make_map(defs)
    paths = find_paths_part_two(cave_map, ['start'])
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
