import re
from typing import Any, Dict, Set, TextIO, Tuple


def process_file(file: TextIO) -> Dict[str, Any]:
    info: Dict[str, Any] = {"dots": set(), "folds": []}
    regex = re.compile(r"([xy])=(\d+)")
    lines = file.read().splitlines()

    for i, line in enumerate(lines):
        if not line:
            break
        x, y = line.split(",")
        info["dots"].add((int(x), int(y)))

    for fold in lines[i + 1 :]:
        axis, line = regex.findall(fold)[0]
        axis = 0 if axis == "x" else 1
        info["folds"].append((axis, int(line)))

    return info


def get_dots(info: Dict[str, Any], first_fold: bool = True) -> Set[Tuple[int, int]]:
    if first_fold:
        info["folds"] = info["folds"][:1]

    for axis, line in info["folds"]:
        new_dots = set()
        remove_dots = set()
        for dot in info["dots"]:
            if dot[axis] > line:
                new_dot = list(dot)
                new_dot[axis] = 2 * line - dot[axis]
                new_dots.add(tuple(new_dot))
            if dot[axis] >= line:
                remove_dots.add(dot)

        info["dots"] -= remove_dots
        info["dots"] |= new_dots

    return info["dots"]


def print_code(dots: Set[Tuple[int, int]], codes: int = 8) -> None:
    x_max = 0
    y_max = 0

    for x, y in dots:
        if x > x_max:
            x_max = x
        if y > y_max:
            y_max = y

    code = []
    for _ in range(y_max + 1):
        code.append([" " for _ in range(x_max + 1)])
    for x, y in dots:
        code[y][x] = "*"

    for line in code:
        print("".join(line))


if __name__ == "__main__":
    with open("files/input13.txt") as file:
        info = process_file(file)

    # dots = get_dots(info)
    # print(len(dots))
    dots = get_dots(info, first_fold=False)
    print_code(dots)
