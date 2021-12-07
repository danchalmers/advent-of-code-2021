from collections import defaultdict


Count = int


def count_values_in_file_list(file_name: str) -> dict[int, int]:
    pos_count = defaultdict(int)
    with open('data/' + file_name, 'r') as f:
        for x in f.readline().split(','):
            pos_count[int(x)] += 1
    return pos_count
