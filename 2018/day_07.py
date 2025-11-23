import argparse
import re

from dataclasses import dataclass
from heapq import heapify, heappop, heappush
from pathlib import Path
from time import time

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

@dataclass
class Step:
    name: str
    remaining: int

def parse_input(raw: str) -> tuple:
    pattern = r"Step (\w) must be finished before step (\w) can begin."
    return re.findall(pattern, raw)[0]

def letter_duration(letter: str) -> int:
    return 60 + ord(letter.lower()) - 96

def build_path(start: set, path_length: int, end: str) -> str:
    path = ""
    heap_path = list(start)
    heapify(heap_path)
    while len(heap_path) < path_length:
        current = heappop(heap_path)
        path += current
        if current == end:
            break
        for step in liberates[current]:
            if not [
                s for s in blocked_by[step]
                if s not in path
            ]:
                heappush(heap_path, step)
    return path

def work_together(start: set, path_length: int, end: str) -> int:
    sec = 0
    workers: dict[Step] = {}
    available_workers = list(range(5))
    for worker in available_workers:
        workers[worker] = Step("", 0)
    path = ""
    heap_path = list(start)
    heapify(heap_path)
    while len(path) < path_length:
        done = []
        heapify(done)
        for wid, step in workers.items():
            if step.remaining == 0 and step.name != "" and step.name not in path:
                heappush(done, step.name)
                available_workers.append(wid)
            elif step.name:
                step.remaining -= 1
        if done:
            step_done = heappop(done)
            path += step_done
            if step_done == end:
                break
            for step in liberates[step_done]:
                if not [
                    s for s in blocked_by[step]
                    if s not in path
                ]:
                    heappush(heap_path, step)
        while available_workers and heap_path:
            current = heappop(heap_path)
            wid = available_workers.pop()
            workers[wid].name = current
            workers[wid].remaining = letter_duration(current) - 1
        sec += 1
    print(path)
    return sec

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    liberates = dict()
    blocked_by = dict()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        while line:=file.readline():
            first, last = parse_input(line)
            liberates[first] = liberates.get(first, []) + [last]
            blocked_by[last] = blocked_by.get(last, []) + [first]
    start = set(liberates.keys()) - set(blocked_by.keys())
    end = (set(blocked_by.keys()) - set(liberates.keys())).pop()
    path_length = len(liberates.keys()) + len(start)
    if args.part == 1:
        print(build_path(start, path_length, end))
    else:
        print(work_together(start, path_length, end))
    print(time() - t)
