import re
from collections import defaultdict
from typing import Dict, List


def get_dangerous(vents_: List[str], diagonal: bool = False) -> int:
    overlaps: Dict[str, int] = defaultdict(int)
    regex = re.compile(r"\d+")
    for vent in vents_:
        x_1, y_1, x_2, y_2 = map(int, regex.findall(vent))
        if x_1 == x_2:
            if y_1 > y_2:
                y_1, y_2 = y_2, y_1
            for i in range(y_1, y_2 + 1):
                overlaps[f"{x_1},{i}"] += 1
        elif y_1 == y_2:
            if x_1 > x_2:
                x_1, x_2 = x_2, x_1
            for i in range(x_1, x_2 + 1):
                overlaps[f"{i},{y_1}"] += 1
        elif diagonal and abs(y_1 - y_2) == abs(x_1 - x_2):
            for i in range(abs(y_1 - y_2) + 1):
                step_x = i
                step_y = i
                if x_1 > x_2:
                    step_x *= -1
                if y_1 > y_2:
                    step_y *= -1
                overlaps[f"{x_1 + step_x},{y_1 + step_y}"] += 1

    dangerous = 0
    for overlap in overlaps.values():
        if overlap > 1:
            dangerous += 1

    return dangerous


if __name__ == "__main__":
    with open("files/input5.txt") as file:
        data = file.readlines()
    print(get_dangerous(data, diagonal=True))
