import argparse

from pathlib import Path
from time import time


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--part", "-p", type=int, choices={1, 2}, help="Set puzzle part"
    )
    args = parser.parse_args()
    if not args.part:
        parser.error("Which part are you solving?")
    return args


def parse_input(raw: str) -> None:
    const, ran = raw.split(", ")
    is_x = const.startswith("x")
    const_value = int(const[2:])
    start, end = ran[2:].split("..")
    for i in range(int(start), int(end) + 1):
        key = (const_value, i) if is_x else (i, const_value)
        data[key] = "#"
    if is_x:
        x_const[(const_value, int(end))] = range(int(start), int(end) + 1)
    else:
        y_const[(const_value, int(start))] = range(int(start), int(end) + 1)


def get_floor(x: int, y: int) -> range | None:
    for key, value in y_const.items():
        if key[0] == y and x in value:
            return value
    return None


def get_left_start(y: int, x_range: range) -> int:
    return x_const[(x_range[0], y)][0]


def get_right_start(y: int, x_range: range) -> int:
    return x_const[(x_range[-1], y)][0]


def bigger_bucket(y: int, x_range: range) -> tuple | None:
    for y_key, y_value in y_const.items():
        if y_key[0] > y and set(y_value) & set(x_range) == set(x_range):
            if len(
                set(x_const.get((y_value[0], y_key[0]), []))
                & set(x_const.get((x_range[0], y), []))
            ):
                return y_key
    return None


def smaller_bucket(y: int, x_range: range) -> tuple | None:
    for y_key, y_value in y_const.items():
        if y_key[0] < y and set(y_value) & set(x_range) == set(y_value):
            if len(
                set(x_const.get((y_value[0], y_key[0]), []))
                & set(x_const.get((x_range[0], y), []))
            ):
                return y_key
    return None


def is_closed(y_key: tuple) -> bool:
    x_range = y_const[y_key]
    left = get_left_start(y_key[0], x_range)
    right = get_right_start(y_key[0], x_range)
    return left == right and y_const.get((left, x_range[0]), []) == x_range


def count_water(source: tuple, water: set, remaining_water: set) -> None:
    sx, sy = source
    if source in sources:
        return
    sources.add(source)
    y_floor = sy + 1
    while y_floor <= y_max:
        if data.get((sx, y_floor)) and get_floor(sx, y_floor) and x_const.get((get_floor(sx, y_floor) [0], y_floor)):
            break
        y_floor += 1
    else:
        # Infinite flow below ymax
        water |= {(sx, y) for y in range(sy, y_max + 1)}
        return
    x_range = get_floor(sx, y_floor)
    if x_range:
        big_bucket = bigger_bucket(y_floor, x_range)
        small_bucket = smaller_bucket(y_floor, x_range)
        left_start = get_left_start(y_floor, x_range)
        right_start = get_right_start(y_floor, x_range)
        early_stop = left_start if is_closed((y_floor, x_range[0])) else y_floor
        water |= {(sx, y) for y in range(sy, early_stop) if data.get((sx, y), ".") != "#"}
        # It's just a simple bucket
        if not big_bucket and not small_bucket:
            remaining_water |= {
                (x, y)
                for x in range(x_range[0] + 1, x_range[-1])
                for y in range(max(left_start, right_start), y_floor)
                if data.get((x, y), ".") != "#"
            }
            water |= {
                (x, max(left_start, right_start) - 1)
                for x in range(x_range[0] + 1, x_range[-1])
                if data.get((x, max(left_start, right_start) - 1), ".") != "#"
            } | remaining_water
            if left_start >= right_start:
                water.add((x_range[0], left_start - 1))
                count_water((x_range[0] - 1, left_start - 1), water, remaining_water)
            if left_start <= right_start:
                water.add((x_range[-1], right_start - 1))
                count_water((x_range[-1] + 1, right_start - 1), water, remaining_water)
            return
        # It's a big bucket containing a smaller one
        if small_bucket:
            small_x_range = y_const[small_bucket]
            small_left_start = get_left_start(small_bucket[0], small_x_range)
            small_right_start = get_right_start(small_bucket[0], small_x_range)
            impossible = {
                (x, y)
                for x in range(small_x_range[0] + 1, small_x_range[-1])
                for y in range(small_left_start + 1, small_bucket[0])
             } if is_closed(small_bucket) else set()
            if min(small_left_start, small_right_start) >= max(left_start, right_start):
                remaining_water |= {
                    (x, y)
                    for x in range(x_range[0] + 1, x_range[-1])
                    for y in range(max(left_start, right_start), y_floor)
                    if data.get((x, y), ".") != "#" and (x, y) not in impossible
                }
                y_start = max(left_start, right_start) - 1
                water |= {
                    (x, y_start)
                    for x in range(x_range[0] + 1, x_range[-1])
                    if data.get((x, y_start), ".") != "#" and (x, y_start) not in impossible
                } | remaining_water
                if left_start >= right_start:
                    water.add((x_range[0], left_start - 1))
                    count_water((x_range[0] - 1, left_start - 1), water, remaining_water)
                if left_start <= right_start:
                    water.add((x_range[-1], right_start - 1))
                    count_water((x_range[-1] + 1, right_start - 1), water, remaining_water)
                return
            remaining_water |= {
                (x, y)
                for x in range(x_range[0] + 1, x_range[-1])
                for y in range(small_bucket[0] + 1, y_floor)
                if data.get((x, y), ".") != "#" and (x, y) not in impossible
            }
            water |= remaining_water
            if small_bucket[1] < sx:  # bucket on the left of the source
                if right_start <= small_right_start:
                    water |= {
                        (x, y)
                        for x in range(small_x_range[0] + 1, small_x_range[-1] + 1)
                        for y in range(right_start - 1, small_bucket[0])
                        if data.get((x, y), ".") != "#" and (x, y) not in impossible
                    }
                    remaining_water |= {
                        (x, y)
                        for x in range(small_x_range[0] + 1, small_x_range[-1] + 1)
                        for y in range(right_start, small_bucket[0])
                        if data.get((x, y), ".") != "#" and (x, y) not in impossible
                    }
                water |= {
                    (x, y)
                    for x in range(small_x_range[-1] + 1, x_range[-1])
                    for y in range(right_start - 1, y_floor)
                    if data.get((x, y), ".") != "#" and (x, y) not in impossible
                } | {(x_range[-1], right_start - 1)}
                remaining_water |= {
                    (x, y)
                    for x in range(small_x_range[-1] + 1, x_range[-1])
                    for y in range(right_start, y_floor)
                    if data.get((x, y), ".") != "#" and (x, y) not in impossible
                }
                count_water((x_range[-1] + 1, right_start - 1), water, remaining_water)
                return
            else:  # bucket on the right of the source
                if left_start <= small_left_start:
                    water |= {
                        (x, y)
                        for x in range(small_x_range[0], small_x_range[-1])
                        for y in range(left_start - 1, small_bucket[0])
                        if data.get((x, y), ".") != "#" and (x, y) not in impossible
                    }
                    remaining_water |= {
                        (x, y)
                        for x in range(small_x_range[0], small_x_range[-1])
                        for y in range(left_start, small_bucket[0])
                        if data.get((x, y), ".") != "#" and (x, y) not in impossible
                    }
                water |= {
                    (x, y)
                    for x in range(x_range[0] + 1, small_x_range[0])
                    for y in range(left_start - 1, y_floor)
                    if data.get((x, y), ".") != "#" and (x, y) not in impossible
                } | {(x_range[0], left_start - 1)}
                remaining_water |= {
                    (x, y)
                    for x in range(x_range[0] + 1, small_x_range[0])
                    for y in range(left_start, y_floor)
                    if data.get((x, y), ".") != "#" and (x, y) not in impossible
                } 
                count_water((x_range[0] - 1, left_start - 1), water, remaining_water)
                return
        # It's a small bucket with a bigger one around
        if big_bucket:
            big_x_range = y_const[big_bucket]
            big_left_start = get_left_start(big_bucket[0], big_x_range)
            big_right_start = get_right_start(big_bucket[0], big_x_range)
            impossible = {
                (x, y)
                for x in range(x_range[0] + 1, x_range[-1])
                for y in range(left_start + 1, y_floor)
             } if is_closed((y_floor, x_range[0])) else set()
            if max(big_left_start, big_right_start) <= min(left_start, right_start):
                water |= {
                    (x, y)
                    for x in range(big_x_range[0] + 1, big_x_range[-1])
                    for y in range(max(big_left_start, big_right_start) - 1, big_bucket[0])
                    if data.get((x, y), ".") != "#" and (x, y) not in impossible
                }
                remaining_water |= {
                    (x, y)
                    for x in range(big_x_range[0] + 1, big_x_range[-1])
                    for y in range(max(big_left_start, big_right_start), big_bucket[0])
                    if data.get((x, y), ".") != "#" and (x, y) not in impossible
                }
                if big_left_start >= big_right_start:
                    water.add((big_x_range[0], big_left_start - 1))
                    count_water((big_x_range[0] - 1, big_left_start - 1), water, remaining_water)
                if big_left_start <= big_right_start:
                    water.add((big_x_range[-1], big_right_start - 1))
                    count_water((big_x_range[-1] + 1, big_right_start - 1), water, remaining_water)
                return
            water |= {
                (x, y)
                for x in range(big_x_range[0] + 1, big_x_range[-1])
                for y in range(y_floor + 1, big_bucket[0])
                if data.get((x, y), ".") != "#"  and (x, y) not in impossible
            }
            remaining_water |= {
                (x, y)
                for x in range(big_x_range[0] + 1, big_x_range[-1])
                for y in range(y_floor + 1, big_bucket[0])
                if data.get((x, y), ".") != "#"  and (x, y) not in impossible
            }
            if left_start <= right_start:
                if right_start < big_right_start:
                    water |= {
                        (x, y)
                        for x in range(x_range[0] + 1, x_range[-1] + 2)
                        for y in range(right_start - 1, big_right_start)
                        if data.get((x, y), ".") != "#" and (x, y) not in impossible
                    }
                    remaining_water |= {
                        (x, y)
                        for x in range(x_range[0] + 1, x_range[-1] + 2)
                        for y in range(right_start, big_right_start)
                        if data.get((x, y), ".") != "#" and (x, y) not in impossible
                    }
                water |= {
                    (x, y)
                    for x in range(x_range[0] + 1, big_x_range[-1])
                    for y in range(big_right_start - 1, y_floor + 1)
                    if data.get((x, y), ".") != "#" and (x, y) not in impossible
                }
                remaining_water |= {
                    (x, y)
                    for x in range(x_range[0] + 1, big_x_range[-1])
                    for y in range(big_right_start, y_floor + 1)
                    if data.get((x, y), ".") != "#" and (x, y) not in impossible
                }
                count_water((big_x_range[-1] + 1, big_right_start - 1), water, remaining_water)

            if right_start <= left_start:
                if left_start < big_left_start:
                    water |= {
                        (x, y)
                        for x in range(x_range[0] - 1, x_range[-1])
                        for y in range(left_start - 1, big_left_start)
                        if data.get((x, y), ".") != "#" and (x, y) not in impossible
                    }
                    remaining_water |= {
                        (x, y)
                        for x in range(x_range[0] - 1, x_range[-1])
                        for y in range(left_start, big_left_start)
                        if data.get((x, y), ".") != "#" and (x, y) not in impossible
                    }
                water |= {
                    (x, y)
                    for x in range(big_x_range[0], x_range[-1])
                    for y in range(big_left_start - 1, y_floor + 1)
                    if data.get((x, y), ".") != "#" and (x, y) not in impossible
                }
                water |= {
                    (x, y)
                    for x in range(big_x_range[0], x_range[-1])
                    for y in range(big_left_start, y_floor + 1)
                    if data.get((x, y), ".") != "#" and (x, y) not in impossible
                }
                count_water((big_x_range[0] - 1, big_left_start - 1), water, remaining_water)
            return
    else:
        # never happens, but meh.
        water.add(source)
        count_water((sx + 1, sy), water)
        count_water((sx - 1, sy), water)
        return


if __name__ == "__main__":
    args = _parse_args()
    t = time()
    x_const = {}
    y_const = {}
    data = {}
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        [parse_input(raw) for raw in file.read().split("\n") if raw]
    y_max = max(y[0] for y in y_const.keys())
    y_min = min(key[1] for key in data.keys())
    sources = set()
    water = set()
    remaining_water = set()
    count_water((500, 0), water, remaining_water)
    if args.part == 1:
        print(len(water) - y_min)  # initial source above minimal y value
    else:
        print(len(remaining_water))
    print(time() - t)
