import unittest
import time

from common import load_grid
from day_fifteen import shortest_path, TEST_FILE, expand_map

SMALLEST_GRID = [[1,2],[5,13]]
BIGGER_GRID = [
    [1,2,3],
    [4,5,6],
    [7,8,9]
]
BIGGEST_GRID = [
    [1,2,3,4],
    [2,2,3,1],
    [1,4,2,8],
    [2,8,3,4]
]


class DatFifteenTestCase(unittest.TestCase):
    def test_smallest_grid(self):
        result = shortest_path(SMALLEST_GRID, 2, 2)
        self.assertEqual(15, result)

    def test_bigger_grid(self):
        result = shortest_path(BIGGER_GRID, 3, 3)
        self.assertEqual(20, result)

    def test_biggest_grid(self):
        result = shortest_path(BIGGEST_GRID, 4, 4)
        self.assertEqual(16, result)

    def test_example_map(self):
        floor_map, x_size, y_size = load_grid(TEST_FILE, '../data/')
        part_one = shortest_path(floor_map, x_size, y_size)
        self.assertEqual(40, part_one)
        big_map = expand_map(floor_map)
        start_time = time.time_ns()
        part_two = shortest_path(big_map, len(big_map[0]), len(big_map))
        end_time = time.time_ns()
        self.assertEqual(315, part_two)
        duration_ms = (end_time - start_time) / 1_000_000
        print(f"big map took {duration_ms}ms")



if __name__ == '__main__':
    unittest.main()
