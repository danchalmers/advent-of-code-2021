from collections import defaultdict

from common import count_values_in_file_list


TEST_FILE = 'test-6.txt'
REAL_FILE = 'input-6.txt'


def one_day(fish_count: dict[int, int]) -> dict[int, int]:
    result = defaultdict(int)
    for age, c in fish_count.items():
        if age == 0:
            result[6] += c
            result[8] = c
        else:
            result[age-1] += c
    return result


def simulate_breeding(file_name: str, days: int):
    fish_count = count_values_in_file_list(file_name)
    for i in range(days):
        fish_count = one_day(fish_count)
    print(sum(fish_count.values()))


if __name__ == "__main__":
    simulate_breeding(REAL_FILE, 256)
