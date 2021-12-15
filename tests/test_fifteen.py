import unittest

from day_fifteen import shortest_path


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


if __name__ == '__main__':
    unittest.main()
