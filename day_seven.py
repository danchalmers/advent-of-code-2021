from typing import Callable

from common import count_values_in_file_list, Count, triangular_number

TEST_FILE = 'test-7.txt'
REAL_FILE = 'input-7.txt'


def constant_fuel_movement_cost(positions: dict[int, int], to_position: int) -> int:
    return sum([abs(p - to_position) * c for p, c in positions.items()])


def _single_part_two_fuel_movement_cost(x: int, y: int) -> float:
    return triangular_number(abs(x - y))


def part_two_fuel_movement_cost(positions: dict[int, int], to_position: int) -> int:
    return int(sum([_single_part_two_fuel_movement_cost(p, to_position) * c for p, c in positions.items()]))


def minimise_movement(position_counts: dict[int, Count], cost_fn: Callable[[dict[int, Count]], int]) -> int:
    start = min(position_counts.keys())
    min_movement = cost_fn(position_counts, start - 1)
    for to_position in range(start, max(position_counts.keys())):
        movement = cost_fn(position_counts, to_position)
        if movement < min_movement:
            min_movement = movement
        else:
            break
    min_pos = to_position - 1
    print(f"moving to {min_pos} costs {min_movement}")
    return min_pos


if __name__ == "__main__":
    position_counts = count_values_in_file_list(REAL_FILE)
    minimise_movement(position_counts, constant_fuel_movement_cost)
    minimise_movement(position_counts, part_two_fuel_movement_cost)
