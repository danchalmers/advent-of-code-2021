import unittest

from day_seventeen import highest_point_for_target, count_candidate_v0s

EXAMPLE = "target area: x=20..30, y=-10..-5"


class DaySeventeenTestCase(unittest.TestCase):
    def test_example_highest(self):
        max_y = highest_point_for_target(EXAMPLE)
        self.assertEqual(45, max_y)

    def test_example_valid_v0s(self):
        count = count_candidate_v0s(EXAMPLE)
        self.assertEqual(112, count)

if __name__ == '__main__':
    unittest.main()
