from collections import defaultdict
from typing import List


def search_paths(
    node: str, all_nodes: defaultdict, traversed: defaultdict, limit: int = 1
) -> int:
    paths = 0
    for leaf in all_nodes[node]:
        if leaf == "end":
            paths += 1
            continue

        if traversed[leaf] < limit:
            if leaf.islower():
                traversed[leaf] += 1
                limit_ = limit
                if traversed[leaf] == 2:
                    limit_ = 1
                paths += search_paths(leaf, all_nodes, traversed, limit_)
                traversed[leaf] -= 1
            else:
                paths += search_paths(leaf, all_nodes, traversed, limit)

    return paths


def get_paths(links: List[str], max_visit: int = 1) -> int:
    nodes = defaultdict(list)
    for link in links:
        start, end = link.split("-")
        if start == "start":
            nodes["start"].append(end)
        elif end == "start":
            nodes["start"].append(start)
        elif start == "end":
            nodes[end].append("end")
        elif end == "end":
            nodes[start].append("end")
        else:
            nodes[start].append(end)
            nodes[end].append(start)

    return search_paths("start", nodes, defaultdict(int), max_visit)


if __name__ == "__main__":
    with open("files/input12.txt") as file:
        data = file.read().splitlines()

    print(get_paths(data))
    print(get_paths(data, max_visit=2))
