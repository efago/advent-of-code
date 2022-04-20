from typing import List, TextIO

import numpy as np


def get_risk_levels(file: TextIO, duplicate: int = 1) -> List[List[int]]:
    risks = []
    for line in file.read().splitlines():
        risks.append([int(risk) for risk in line])

    rows = len(risks)
    cols = len(risks[0])

    for i in range(rows):
        for j in range(0, cols * (duplicate - 1), cols):
            col = risks[i][j : j + cols]
            risks[i].extend([risk + 1 if risk < 9 else 1 for risk in col])

    for i in range(rows, rows * duplicate):
        row = risks[i - rows]
        risks.append([risk + 1 if risk < 9 else 1 for risk in row])

    return risks


def get_minimum_risks(risks: List[List[int]]) -> float:
    max_row = len(risks)
    max_col = len(risks[0])
    minimum_risk = np.full([max_row, max_col], fill_value=np.inf)
    minimum_risk[0, 0] = 0
    queue = {(0, 0): minimum_risk[0, 0]}
    visited = set()

    while queue:
        cave = min(queue, key=queue.get)
        row_, col_ = cave
        risk_level = queue.pop(cave)
        visited.add(cave)
        neighbors = [
            (row_ - 1, col_),
            (row_ + 1, col_),
            (row_, col_ - 1),
            (row_, col_ + 1),
        ]
        for row, col in neighbors:
            if (
                (row, col) not in visited
                and row >= 0
                and row < max_row
                and col >= 0
                and col < max_col
            ):
                risk = risks[row][col] + risk_level
                if risk < minimum_risk[row, col]:
                    minimum_risk[row, col] = risk
                    queue[(row, col)] = risk

    return minimum_risk[-1, -1]


if __name__ == "__main__":
    with open("files/input15.txt") as file:
        risk_levels = get_risk_levels(file, duplicate=5)

    print(get_minimum_risks(risk_levels))
