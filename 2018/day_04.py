import argparse
import re

from datetime import datetime
from pathlib import Path

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--part", "-p",
        type=int,
        choices={1, 2},
        help="Set puzzle part"
    )
    args = parser.parse_args()
    if not args.part:
        parser.error("Which part are you solving?")
    return args

def parse_input(logs: list) -> dict:
    guards = dict()
    guard = None
    for log in logs:
        timestamp, command = re.findall(r"\[(.+)\] (.+)", log)[0]
        if command not in ("falls asleep", "wakes up"):
            guard = int(re.findall(r"\d+", command)[0])
            continue
        timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M")
        if command == "falls asleep":
            start = timestamp.minute
            continue
        else:
            end = timestamp.minute
            for i in range(start, end):
                guard_data = guards.get(guard, {})
                guard_data[i] = guard_data.get(i, []) + [timestamp.day]
                guards[guard] = guard_data
    return guards

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().split("\n")
    data.sort()
    asleep = parse_input(data)
    if args.part == 1:
        most_asleep = (0, 0, 0)
        for guard, times in asleep.items():
            time_asleep = 0
            max_minute = 0, 0
            for minute, days in times.items():
                time_asleep += len(days)
                if len(days) > max_minute[1]:
                    max_minute = minute, len(days)
            if time_asleep > most_asleep[1]:
                most_asleep = guard, time_asleep, max_minute[0]
        print(most_asleep[0] * most_asleep[2])
    else:
        max_minute = 0, 0, 0
        for guard, times in asleep.items():
            for minute, days in times.items():
                if len(days) > max_minute[2]:
                    max_minute = guard, minute, len(days)
        print(max_minute[0] * max_minute[1])
