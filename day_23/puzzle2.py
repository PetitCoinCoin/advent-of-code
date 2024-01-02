from pathlib import Path

def is_valid_child(value: str) -> bool:
    if value == "#":
        return False
    return True

def get_adjacents(step: tuple, data: list) -> list:
    result = []
    for i, j in (
        (step[0], step[1] + 1),
        (step[0] - 1, step[1]),
        (step[0], step[1] - 1),
        (step[0] + 1, step[1]),
    ):
        if len(data) > i >= 0 and len(data[0]) > j >= 0 and data[i][j] != "#":
            result.append((i, j))
    return result

def contract(step: tuple, source: tuple, edges: dict, seen: dict, destination: tuple) -> tuple:
    distance = 1
    adjacents = get_adjacents(step, data)
    while len(adjacents) == 2 or step == (0, 1):
        distance += 1
        seen.add(step)
        step = [n for n in adjacents if n not in seen][0]
        adjacents = get_adjacents(step, data)
    if distance > 1:
        edges[source] = edges.get(source, set()) | {(distance, step)}
        edges[step] = edges.get(step, set()) | {(distance, source)}
    return step, distance

def get_contracted_graph(data: dict, source: tuple, destination: tuple) -> dict:
    edges = dict()
    seen = set()
    queue = [source]
    while queue:
        start = queue.pop(0)
        step = start
        adjacents = get_adjacents(step, data)
        if len(adjacents) > 2:
            seen.add(start)
            for child in [n for n in adjacents if n not in seen]:
                seen.add(child)
                node, dist = contract(child, step, edges, seen, destination)
                if dist > 1:
                    queue.append(node)
            seen.remove(start)
        else:
            node, dist = contract(step, step, edges, seen, destination)
            if dist > 1:
                queue.append(node)
    return edges

def longest_path(step: tuple, destination: tuple, edges: dict, distance: int = 0, seen: set = set()) -> int:
    if step == destination:
        return distance
    seen.add(step)
    max_path = 0
    for dist, neighbor in edges[step]:
        if neighbor in seen:
            continue
        max_path = max(max_path, longest_path(neighbor, destination, edges, distance + dist, seen))
    seen.remove(step)
    return max_path

if __name__ == "__main__":
    with Path("day_23/input.txt").open("r") as file:
        data = file.read().split()
    size = len(data)  # square data
    start = (0, 1)
    destination = (size - 1, size - 2)
    edges = get_contracted_graph(data, start, destination)
    print(longest_path(start, destination, edges) - 1)  # - 1 because path from start to 1st node is 1 unit too long.
