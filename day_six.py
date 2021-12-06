from collections import defaultdict


TEST_FILE = 'test-6.txt'
REAL_FILE = 'input-6.txt'


def initial_fish(file_name: str) -> dict[int, int]:
    fish_count = defaultdict(int)
    with open('data/' + file_name, 'r') as f:
        for x in f.readline().split(','):
            fish_count[int(x)] += 1
    return fish_count


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
    fish_count = initial_fish(file_name)
    for i in range(days):
        fish_count = one_day(fish_count)
    print(sum(fish_count.values()))


if __name__ == "__main__":
    simulate_breeding(REAL_FILE, 256)
