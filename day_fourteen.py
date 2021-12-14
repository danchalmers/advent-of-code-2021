from collections import Counter
from cachetools import cached
from cachetools.keys import hashkey


TEST_FILE = 'test-14.txt'
REAL_FILE = 'input-14.txt'

P = str
Template = list[P]
Rules = dict[tuple[P, P], P]
PCount = list[tuple[P, int]]


def read_input(file_name: str) -> tuple[Template, Rules]:
    rules = {}
    with open('data/' + file_name, 'r') as f:
        template = list(f.readline().strip())
        for line in f.readlines():
            line = line.strip()
            if len(line) != 0:
                pattern_result = line.split(' -> ')
                rules[tuple(pattern_result[0])] = pattern_result[1]
    return template, rules


@cached(cache={}, key=lambda xz, rules, step, limit: hashkey(xz, step, limit))
def do_step(xz: tuple[P], rules: Rules, step: int, limit: int) -> PCount:
    y = rules[xz]
    if step == limit - 1:
        return Counter([xz[0], y])
    else:
        return do_step((xz[0], y), rules, step+1, limit) + do_step((y, xz[1]), rules, step+1, limit)


def build_polymer(file_name: str, rounds: int):
    template, rules = read_input(file_name)
    result = sum([do_step(xz, rules, step=0, limit=rounds) for xz in zip(template, template[1:])], Counter())
    result[template[-1]] += 1
    result = result.most_common()
    difference = result[0][1] - result[-1][1]
    print(f"most - least common: {difference}")


if __name__ == "__main__":
    build_polymer(REAL_FILE, 10)
    build_polymer(REAL_FILE, 40)
