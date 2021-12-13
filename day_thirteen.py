TEST_FILE = 'test-13.txt'
REAL_FILE = 'input-13.txt'


Point = tuple[int, int]
Fold = tuple[str, int]


def read_instructions(file_name: str) -> tuple[set[Point], list[Fold]]:
    points = []
    folds = []
    points_not_folds = True
    with open('data/' + file_name, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if len(line) == 0:
                points_not_folds = False
                continue
            if points_not_folds:
                xy = line.split(',')
                points.append((int(xy[0]), int(xy[1])))
            else:
                fold = line.split()[-1].split('=')
                folds.append((fold[0], int(fold[1])))
    return set(points), folds


def _fold_one(point: Point, axis: int, line: int) -> Point:
    if point[axis] < line:
        return point
    new_point = [p for p in point]
    new_point[axis] = 2 * line - point[axis]
    return tuple(new_point)


def do_fold(points: set[Point], fold: Fold):
    axis = 0 if fold[0] == 'x' else 1
    return set([_fold_one(p, axis, fold[1]) for p in points])


def part_one(file_name: str):
    points, folds = read_instructions(file_name)
    points = do_fold(points, folds[0])
    count = len(points)
    print(f"part one has {count} points")


def display(points: set[Point]):
    max_x = max([p[0] for p in points])
    max_y = max([p[1] for p in points])
    dots = [['.' for x in range(max_x + 1)] for y in range(max_y + 1)]
    for p in points:
        dots[p[1]][p[0]] = '#'
    for line in dots:
        print(''.join(line))
    print()


def part_two(file_name: str):
    points, folds = read_instructions(file_name)
    for fold in folds:
        points = do_fold(points, fold)
    display(points)


if __name__ == "__main__":
    part_one(REAL_FILE)
    part_two(REAL_FILE)
