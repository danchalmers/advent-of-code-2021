from collections import deque
from typing import Iterable, Optional

from pipe import map, where, sort


TEST_FILE = 'test-10.txt'
REAL_FILE = 'input-10.txt'


MATCHES = {
    '(': ')',
    '{': '}',
    '[': ']',
    '<': '>'
}

PART_ONE_SCORES = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

PART_TWO_SCORES = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}


def file_lines(file_name: str) -> Iterable[str]:
    with open('data/' + file_name, 'r') as f:
        for line in f.readlines():
            yield line.strip()


def wrong_close(line: str) -> tuple[Optional[str], Optional[Iterable[str]]]:
    opened = deque()
    for c in line:
        if c in '({[<':
            opened.append(c)
        else:
            o = opened.pop()
            if MATCHES[o] != c:
                return c, None
    opened.reverse()
    return None, opened


def part_one(file_name: str):
    score = sum(
        file_lines(file_name)
        | map(lambda line: wrong_close(line)[0])
        | where(lambda wrong: wrong is not None)
        | map(lambda wrong: PART_ONE_SCORES[wrong])
    )
    print(f"part one score {score}")


def score_line(scores: list[int]) -> int:
    score = 0
    for s in scores:
        score *= 5
        score += s
    return score


def part_two(file_name: str):
    scores = list(
        file_lines(file_name)
        | map(lambda line: wrong_close(line)[1])
        | where(lambda remaining: remaining is not None)
        | map(lambda remaining: list(
            remaining
            | map(lambda r: MATCHES[r])
            | map(lambda r: PART_TWO_SCORES[r])
        ))
        | map(lambda ss: score_line(ss))
        | sort
    )
    score = scores[len(scores) // 2]
    print(f"part two score {score}")


if __name__ == "__main__":
    part_one(REAL_FILE)
    part_two(REAL_FILE)
