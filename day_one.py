from typing import List


TEST_FILE = 'test-1-1.txt'
REAL_FILE = 'input-1-1.txt'


def count_bigger_v1(file_name: str) -> int:
    prev = None
    result = 0
    with open('data/' + file_name, 'r') as f:
        for line in f.readlines():
            line = int(line)
            if prev and line > prev:
                result += 1
            prev = line
    return result


def _numbers(file_name: str) -> List[int]:
    with open('data/' + file_name, 'r') as f:
        return [int(line) for line in f.readlines()]


def _count_bigger(numbers: List[int]) -> int:
    return len([y for x, y in zip(numbers, numbers[1:])
                if y > x])


def count_bigger_v2(file_name: str) -> int:
    numbers = _numbers(file_name)
    return _count_bigger(numbers)


def count_sliding_window(file_name: str, window_size: int) -> int:
    numbers = _numbers(file_name)
    window_averages = [
        sum(numbers[idx:idx+window_size])
        for idx in range(1 + len(numbers) - window_size)
    ]
    return _count_bigger(window_averages)
