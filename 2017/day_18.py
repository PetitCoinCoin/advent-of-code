import argparse

from collections import deque
from dataclasses import dataclass
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

@dataclass
class Instruction:
    action: str
    reg: str | int
    value: str | int | None = None

def parse_input(raw: str) -> Instruction:
    elements = raw.split(" ")
    if elements[1].isdigit() or elements[1].startswith("-"):
        elements[1] = int(elements[1])
    if len(elements) > 2 and (elements[2].isdigit() or elements[2].startswith("-")):
        elements[2] = int(elements[2])
    if elements[0] in ("snd", "rcv"):
        return Instruction(
            action=elements[0],
            reg=elements[1],
        )
    return Instruction(
        action=elements[0],
        reg=elements[1],
        value=elements[2],
    )

def recover_one() -> list:
    i = 31
    a = 1
    p = 0
    while i > 0:
        a *= 2
        i -= 1
    a -= 1
    i = 127
    p = 316
    while i > 0:
        p *= 8505
        p = p % a
        p *= 129749
        p += 12345
        p = p % a
        b = p % 10000
        i -= 1
    return b


def sync_exchange(instructions: list, i: int, register: dict, reg_queue: deque, other_queue: deque | None) -> int:
    inst = instructions[i]
    delta = 1
    if inst.action == "set":
        register[inst.reg] = inst.value if isinstance(inst.value, int) else register.get(inst.value, 0)
    elif inst.action == "add":
        register[inst.reg] = register.get(inst.reg, 0) + (inst.value if isinstance(inst.value, int) else register.get(inst.value, 0))
    elif inst.action == "mul":
        register[inst.reg] = register.get(inst.reg, 0) * (inst.value if isinstance(inst.value, int) else register.get(inst.value, 0))
    elif inst.action == "mod":
        register[inst.reg] = register.get(inst.reg, 0) % (inst.value if isinstance(inst.value, int) else register.get(inst.value, 0))
    elif inst.action == "jgz":
        if (isinstance(inst.reg, int) and inst.reg > 0) or (isinstance(inst.reg, str) and register.get(inst.reg, 0) > 0):
            delta = inst.value if isinstance(inst.value, int) else register.get(inst.value, 0)
    elif inst.action == "snd":
        if other_queue is not None:  # part 2
            other_queue.append(inst.reg if isinstance(inst.reg, int) else register.get(inst.reg, 0))
            register["sent"] += 1
        else:  # part 1
            reg_queue.append(inst.reg if isinstance(inst.reg, int) else register.get(inst.reg, 0))
    else:  # receive
        if other_queue is not None:  # part 2
            if len(reg_queue):
                register[inst.reg] = reg_queue.popleft()
                register["is_waiting"] = False
            else:
                register["is_waiting"] = True
                return i
        else:  # part 1
            register["sent"] = (reg_queue.pop())
            register["is_waiting"] = True
            return 0
    return i + delta

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [parse_input(line) for line in file.read().split("\n")]
    idx_0 = 0
    register_0 = {"is_waiting": False, "p": 0, "sent": 0}
    queue_0 = deque()
    if args.part == 1:
        # print(recover_one())
        while not (register_0["is_waiting"]):
            idx_0 = sync_exchange(data, idx_0, register_0, queue_0, None)
        print(register_0["sent"])
    else:
        idx_1 = 0
        register_1 = {"is_waiting": False, "p": 1, "sent": 0}
        queue_1 = deque()
        while not (register_0["is_waiting"] and register_1["is_waiting"]):
            idx_0 = sync_exchange(data, idx_0, register_0, queue_0, queue_1)
            idx_1 = sync_exchange(data, idx_1, register_1, queue_1, queue_0)
        print(register_1["sent"])
