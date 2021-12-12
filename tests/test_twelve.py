import unittest

from day_twelve import count_paths_part_one, count_paths_part_two

EXAMPLE_1 = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

EXAMPLE_2 = """
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""

EXAMPLE_3 = """
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""


class DayTwelveTestCase(unittest.TestCase):
    @staticmethod
    def example_lines(example):
        for line in example.splitlines():
            yield line

    def test_part_one_eg_one(self):
        count = count_paths_part_one(self.example_lines(EXAMPLE_1))
        self.assertEqual(10, count)

    def test_part_one_eg_two(self):
        count = count_paths_part_one(self.example_lines(EXAMPLE_2))
        self.assertEqual(19, count)

    def test_part_one_eg_three(self):
        count = count_paths_part_one(self.example_lines(EXAMPLE_3))
        self.assertEqual(226, count)

    def test_part_two_eg_one(self):
        count = count_paths_part_two(self.example_lines(EXAMPLE_1))
        self.assertEqual(36, count)

    def test_part_two_eg_two(self):
        count = count_paths_part_two(self.example_lines(EXAMPLE_2))
        self.assertEqual(103, count)

    def test_part_two_eg_three(self):
        count = count_paths_part_two(self.example_lines(EXAMPLE_3))
        self.assertEqual(3509, count)


if __name__ == '__main__':
    unittest.main()
