from functools import lru_cache

from pipe import map, where, take, tee

from common import Location, Coordinate, triangular_number


REAL_FILE = "input-17.txt"


Time = int
AxisSpeed = int


def read_target_spec(file_name: str) -> str:
    with open('data/' + file_name, 'r') as f:
        return f.readline().strip()


def spec_to_target(target_spec: str) -> tuple[Coordinate, Coordinate]:
    # target area: x=20..30, y=-10..-5
    target_specs = [[y.strip() for y in t.split('=')] for t in target_spec.split(':')[1].split(',')]
    target_specs = {spec[0]: tuple([int(s) for s in spec[1].split('..')]) for spec in target_specs}
    return (min(target_specs['x']), max(target_specs['y'])), (max(target_specs['x']), min(target_specs['y']))


def sign_int(z):
    return -1 if z < 0 else 1


def y_t(vy0: AxisSpeed, end_time: Time) -> Location:
    if vy0 > 0:
        rise_time = max(0, min(end_time, vy0))
        rise = (rise_time * vy0) - triangular_number(rise_time - 1)
        fall = triangular_number(max(end_time - rise_time - 1, 0))
    else:
        rise = 0
        fall = -1 * ((end_time * vy0) - triangular_number(end_time - 1))
    return rise - fall


@lru_cache
def x_t(vx0: AxisSpeed, end_time: Time) -> Location:
    move_time = min(end_time, vx0)
    return (move_time * vx0) - triangular_number(move_time - 1)


def xy_t(vx0: AxisSpeed, vy0: AxisSpeed, time: Time) -> Coordinate:
    return x_t(vx0, time), y_t(vy0, time)


def coord_in_target(coord: Coordinate, top_left: Coordinate, bottom_right: Coordinate) -> bool:
    return top_left[0] <= coord[0] <= bottom_right[0] and bottom_right[1] <= coord[1] <= top_left[1]


def highest_point_for_target(target_str: str) -> Location:
    '''
    The rise to the apex will be a triangular number.
    The ride fall will be the same sequence in reverse, so will pass back through y=0.
    The next step down will be size (vy0 + 1). So this needs to be just inside the target.
    Any larger vy0 will always have a next step outside the target.
    '''
    top_left, bottom_right = spec_to_target(target_str)
    print(f"target {top_left} .. {bottom_right}")
    vy0_max = -1 * (bottom_right[1] + 1)
    apex = y_t(vy0_max, vy0_max)
    print(f"vy0_max {vy0_max} gives apex at {apex}")
    return apex


@lru_cache
def steps_to_check(vy0: AxisSpeed, bottom_right: Coordinate) -> Time:
    y_outside_at = list(
        range(2 * abs(vy0) + abs(bottom_right[1]) + 1)
        | map(lambda t: (t, y_t(vy0, t)))
        | where(lambda t_y: t_y[1] < bottom_right[1])
        | take(1)
    )[0][0]
    return y_outside_at


def _candidate_limits(top_left: Coordinate, bottom_right: Coordinate) -> tuple[Location, Location, Location, Location]:
    max_vx0 = bottom_right[0] + 1
    min_vx0 = list(
        range(top_left[0])
        | map(lambda vx0: (vx0, x_t(vx0, vx0)))
        | where(lambda vx0_x: vx0_x[1] > top_left[0])
        | take(1)
    )[0][0]
    max_vy0 = -1 * (bottom_right[1]) + 1
    min_vy0 = bottom_right[1]
    return min_vx0, max_vx0, min_vy0, max_vy0


def candidate_v0s(top_left: Coordinate, bottom_right: Coordinate) -> list[Coordinate]:
    min_vx0, max_vx0, min_vy0, max_vy0 = _candidate_limits(top_left, bottom_right)
    candidates = set(
        [(vx0, vy0, steps_to_check(vy0, bottom_right))
         for vx0 in range(min_vx0, max_vx0)
         for vy0 in range(min_vy0, max_vy0)
         ]
        | where(lambda vx0_vy0_t: any([
            coord_in_target(xy_t(vx0_vy0_t[0], vx0_vy0_t[1], t), top_left, bottom_right)
            for t in range(vx0_vy0_t[2])
        ]))
        | map(lambda r: tuple(r[0:2]))
    )
    return candidates


def count_candidate_v0s(target_str: str) -> int:
    top_left, bottom_right = spec_to_target(target_str)
    candidates = candidate_v0s(top_left, bottom_right)
    print(f"found {len(candidates)} possible v0s")
    print(candidates)
    return len(candidates)


if __name__ == "__main__":
    target_spec = read_target_spec(REAL_FILE)
    highest_point_for_target(target_spec)
    count_candidate_v0s(target_spec)
