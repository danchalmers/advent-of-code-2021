from collections import defaultdict

Count = int

Height = int
Location = int
Coordinate = tuple[Location, Location]
Map = list[list[Height]]


def count_values_in_file_list(file_name: str) -> dict[int, int]:
    pos_count = defaultdict(int)
    with open('data/' + file_name, 'r') as f:
        for x in f.readline().split(','):
            pos_count[int(x)] += 1
    return pos_count


def load_grid(file_name: str) -> tuple[Map, Location, Location]:
    rows = []
    with open('data/' + file_name, 'r') as f:
        for line in f.readlines():
            rows.append([int(c) for c in line if c.isdigit()])
    return rows, len(rows[0]), len(rows)

