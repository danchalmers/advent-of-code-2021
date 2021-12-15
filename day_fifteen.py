import math
from collections import defaultdict, deque
from typing import Generic, TypeVar

from cachetools import cached

from common import Map, Location, adjacents, load_grid


Cost = int
T = TypeVar('T')
Priority = float

START = (0, 0)

TEST_FILE = 'test-15.txt'
REAL_FILE = 'input-15.txt'


class PriorityQueue(Generic[T]):
    def __init__(self, initial_min_priority: float = math.inf):
        self.priority_queue = defaultdict(deque)
        self.min_priority = initial_min_priority

    def put(self, value: T, priority: Priority):
        self.priority_queue[priority].append(value)
        self.min_priority = min(self.min_priority, priority)

    def empty(self) -> bool:
        return len(self.priority_queue.keys()) == 0

    def pop_min(self) -> tuple[T, Priority]:
        if self.empty():
            return None
        result = self.priority_queue[self.min_priority].pop()
        priority = self.min_priority
        if not self.priority_queue[self.min_priority]:
            del self.priority_queue[self.min_priority]
            if not self.empty():
                self.min_priority = sorted(self.priority_queue.keys())[0]
        return result, priority

    def set_priority(self, value: T, old_priority: Priority, new_priority: Priority):
        if not self.priority_queue[old_priority]:
            del self.priority_queue[old_priority]
        self.priority_queue[new_priority].append(value)
        self.min_priority = min(self.min_priority, new_priority)

    def __repr__(self):
        return str(self.priority_queue.items())


def _initial_distance_estimate(cost_map: Map[Cost], x: Location, y: Location) -> Cost:
    return cost_map[y][x] + (x + y) * 9

# Dijkstra, with a priority queue
def shortest_path(cost_map: Map[Cost], x_size: Location, y_size: Location) -> Cost:
    target = (x_size - 1, y_size - 1)
    distances = [[
        _initial_distance_estimate(cost_map, x, y)
        for x in range(x_size)
    ] for y in range(y_size)
    ]
    distances[START[1]][START[0]] = 0
    preds = [[None for x in range(x_size)] for y in range(y_size)]
    pq = PriorityQueue(initial_min_priority=0)
    for x in range(x_size):
        for y in range(y_size):
            pq.put((x, y), distances[y][x])

    while not pq.empty():
        from_node, prioriy = pq.pop_min()
        for to_node in adjacents(from_node, x_size, y_size):
            alt = distances[from_node[1]][from_node[0]] + cost_map[to_node[1]][to_node[0]]
            if alt < distances[to_node[1]][to_node[0]]:
                distances[to_node[1]][to_node[0]] = alt
                preds[to_node[1]][to_node[0]] = from_node
                pq.set_priority(to_node, prioriy, alt)

    distance = int(distances[target[1]][target[0]])
    print(f"shortest path distance {distance}")
    return distance


@cached(cache={})
def _wrap_number(v: Cost) -> Cost:
    return v - 9 if v > 9 else v


def expand_map(floor_map: Map[Cost]) -> Map[Cost]:
    wide_map = []
    for row in floor_map:
        wide_map.append([_wrap_number(v+offset) for offset in range(0, 5) for v in row])
    big_map = []
    for y in range(0, 5):
        big_map.extend([[_wrap_number(v+y) for v in row] for row in wide_map])
    return big_map


if __name__ == "__main__":
    floor_map, x_size, y_size = load_grid(REAL_FILE)
    shortest_path(floor_map, x_size, y_size)
    big_map = expand_map(floor_map)
    shortest_path(big_map, len(big_map[0]), len(big_map))
