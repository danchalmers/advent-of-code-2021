from typing import Optional

from pipe import chain, where


TEST_FILE = "test-4.txt"
REAL_FILE = "input-4.txt"

Number = int
Score = int


class Board:
    def __init__(self, rows: list[Number]):
        self.rows = rows
        self.columns = [[row [idx] for row in rows] for idx in range(len(rows[0]))]

    @staticmethod
    def _filter(values: list[list[Number]], number: Number) -> list[list[Number]]:
        return [[x for x in xs if x != number] for xs in values]

    def has_won(self) -> bool:
        return len(list(
            self.rows
            | where(lambda r: len(r) == 0)
        )) > 0 or len(list(
            self.columns
            | where(lambda c: len(c) == 0)
        )) > 0

    def play(self, number: Number) -> bool:
        self.rows = Board._filter(self.rows, number)
        self.columns = Board._filter(self.columns, number)
        return self.has_won()


def _read_file(file_name: str) -> tuple[list[Number], list[Board]]:
    boards = []
    with open('data/' + file_name, 'r') as f:
        numbers_to_call = [int(x) for x in f.readline().split(",")]
        rows = []
        for line in f.readlines():
            if len(line.strip()) == 0:
                if rows:
                    boards.append(Board(rows))
                rows = []
            else:
                rows.append([int(x) for x in line.split()])
    if rows:
        boards.append(Board(rows))
    return numbers_to_call, boards


def _play_turn(turn: Number, boards: list[Board]) -> tuple[list[Board], Optional[Score]]:
    score = None
    for board in boards:
        won = board.play(turn)
        if won:
            boards = [b for b in boards if b != board]
            score = sum(board.rows | chain) * turn
    return boards, score


def play_bingo(file_name: str):
    numbers_to_call, boards = _read_file(file_name)
    print(f"playing {numbers_to_call}")
    for turn in numbers_to_call:
        print(f"playing {turn}")
        boards, score = _play_turn(turn, boards)
        if score is not None:
            break
    print(f"winning score {score}")
    return score


def loose_bingo(file_name: str):
    numbers_to_call, boards = _read_file(file_name)
    print(f"playing {numbers_to_call}")
    for turn in numbers_to_call:
        print(f"playing {turn}")
        boards, score = _play_turn(turn, boards)
        if not boards:
            break
    print(f"winning score {score}")
    return score


if __name__ == "__main__":
    loose_bingo(REAL_FILE)