from collections.abc import Iterable


TEST_FILE = 'test-2.txt'
REAL_FILE = 'input-2.txt'


def _command_lines(file_name: str) -> Iterable[tuple[str, int]]:
    with open('data/' + file_name, 'r') as f:
        for line in f.readlines():
            parts = line.split()
            yield parts[0], int(parts[1])


def count_commands(file_name: str) -> tuple[int, int]:
    x = 0
    y = 0
    for command_arg in _command_lines(file_name):
        match command_arg:
            case ("forward", count):
                x += count
            case ("up", count):
                y -= count
            case ("down", count):
                y += count
    return x, y


def day_two_part_one(file_name: str) -> int:
    x, y = count_commands(file_name)
    return x * y


def day_two_part_one_v2(file_name: str) -> int:
    x = sum([count for command, count in _command_lines(file_name) if command == "forward"])
    y = sum([count for command, count in _command_lines(file_name) if command == "down"])
    y -= sum([count for command, count in _command_lines(file_name) if command == "up"])
    return x * y


def count_commands_part_two(file_name: str) -> tuple[int, int]:
    x = 0
    y = 0
    aim = 0
    for command_arg in _command_lines(file_name):
        match command_arg:
            case ("forward", count):
                x += count
                y += aim * count
            case ("up", count):
                aim -= count
            case ("down", count):
                aim += count
    return x, y


def day_two_part_two(file_name: str) -> int:
    x, y = count_commands_part_two(file_name)
    return x * y


if __name__ == "__main__":
    print(day_two_part_two(REAL_FILE))
