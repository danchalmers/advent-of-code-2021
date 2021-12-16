from __future__ import annotations

from pipe import permutations, dedup, where, map, chain
from rich import print

from common import load_grid, Coordinate, AxisSize


TEST_FILE = 'test-11.txt'
REAL_FILE = 'input-11.txt'
STEPS = 100


class Octopus:
    def __init__(self, energy: int):
        self.energy = energy
        self.flashed = False
        self.flashes = 0
        self.neighbours = []

    def connect_neighbours(self, neighbours: list[Octopus]):
        self.neighbours = neighbours

    def inc_flash(self):
        if self.flashed:
            return
        self.energy += 1
        if self.energy >= 10:
            self.energy = 0
            self.flashed = True
            self.flashes += 1
            for n in self.neighbours:
                n.inc_flash()

    def new_step(self):
        self.flashed = False


Octopods = list[list[Octopus]]


def adjacent_inc_diagonals(loc: Coordinate, x_size: AxisSize, y_size: AxisSize) -> list[Coordinate]:
    x, y = loc[0], loc[1]
    return list(
        [-1, -1, 0, 1, 1]
        | permutations(2)
        | dedup()
        | map(lambda xy: (xy[0] + x, xy[1] + y))
        | where(lambda xy: all([z >= 0 for z in xy]))
        | where(lambda xy: xy[0] < x_size and xy[1] < y_size)
    )


def setup(file_name: str) -> tuple[Octopods, AxisSize, AxisSize]:
    energy_grid, x_size, y_size = load_grid(file_name)
    octopods = [[Octopus(e) for e in row] for row in energy_grid]
    for y in range(y_size):
        for x in range(x_size):
            neighbours = adjacent_inc_diagonals((x, y), x_size, y_size)
            octopods[y][x].connect_neighbours([octopods[n[1]][n[0]] for n in neighbours])
    return octopods, x_size, y_size


def _do_step(octopods: Octopods):
    for o in octopods | chain:
        o.new_step()
    for o in octopods | chain:
        o.inc_flash()


def print_map(octopods: Octopods):
    for row in octopods:
        for o in row:
            if o.flashed:
                print(f"[bold red]{o.energy}[/bold red] ", end="")
            else:
                print(f"{o.energy} ", end="")
        print("")

        
def part_one(file_name: str):
    octopods, x_size, y_size = setup(file_name)
    for step in range(STEPS):
        _do_step(octopods)
    total_flashes = sum([o.flashes for o in octopods | chain])
    print(f"total flashes {total_flashes}")
    print_map(octopods)


def part_two(file_name: str):
    octopods, x_size, y_size = setup(file_name)
    step = 0
    while True:
        step += 1
        _do_step(octopods)
        if all([o.energy == 0 for o in octopods | chain]):
            break
    print(f"synchronized flashes at step {step}")
    print_map(octopods)


if __name__ == "__main__":
    part_one(REAL_FILE)
    part_two(REAL_FILE)
