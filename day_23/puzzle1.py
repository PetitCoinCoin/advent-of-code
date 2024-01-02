from pathlib import Path

SIZE = 140

def is_valid_child(step: tuple, r: int, c: int, value: str) -> bool:
    if value == ".":
        return True
    if value == "#":
        return False
    if step[0] == r:
        return (c > step[1] and value != "<") or (c < step[1] and value != ">")
    return (r > step[0] and value != "^") or (r < step[0] and value !="v")

def next_steps(step: tuple, data: list, prev_r: int, prev_c: int) -> list:
    if data[step[0]][step[1]] == ">":
        return [(step[0], step[1] + 1)]
    elif data[step[0]][step[1]] == "^":
        return [(step[0] - 1, step[1])]
    elif data[step[0]][step[1]] == "<":
        return [(step[0], step[1] - 1)]
    elif data[step[0]][step[1]] == "v":
        return [(step[0] + 1, step[1])]
    else:
        result = []
        for i, j in (
            (step[0], step[1] + 1),
            (step[0] - 1, step[1]),
            (step[0], step[1] - 1),
            (step[0] + 1, step[1]),
        ):
            if len(data) > i >= 0 and len(data[0]) > j >= 0 and \
                (i != prev_r or j != prev_c) and \
                is_valid_child(step, i, j, data[i][j]):
                result.append((i, j))
        return result

def build_tree(root: tuple, data: list, paths: dict) -> None:
    q = [(root, 0, 0)]
    seen = dict()
    while q:
        node, prev_r, prev_c = q.pop(0)
        seen[node] = True
        children = next_steps(node, data, prev_r, prev_c)
        for child in children:
            paths[child] = paths[node] + 1
            q.append((child, node[0], node[1]))           

if __name__ == "__main__":
    with Path("day_23/input.txt").open("r") as file:
        data = file.read().split()
    start = (0, 1)
    paths = { start: 0 }
    build_tree(start, data, paths)
    print(paths[(SIZE, SIZE - 1)])
