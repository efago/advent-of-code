import re
from typing import List, Set, TextIO, Tuple


def process_data(file: TextIO) -> List[List[int]]:
    regex = re.compile(r"\d")
    data = [list(map(int, regex.findall(digits))) for digits in file]
    return data


def increment_energies(
    row: int, column: int, energies: List[List[int]], flashed: Set[Tuple[int, int]]
) -> None:
    for r in range(row - 1, row + 2):
        for c in range(column - 1, column + 2):
            if r < 0 or c < 0 or r > ROW_LIMIT or c > COL_LIMIT:
                continue

            energy = energies[r][c]
            if energy == 9:
                flashed.add((r, c))
                energies[r][c] = 0
                increment_energies(r, c, energies, flashed)
            elif energy > 0 or (r, c) not in flashed:
                energies[r][c] += 1


def get_flashes(
    energies: List[List[int]], steps: int, all_simultaneous: bool = False
) -> int:
    flashes = 0
    step = 0

    while True:
        flashed = set()
        for row, energy_row in enumerate(energies):
            for column, energy in enumerate(energy_row):
                if energy == 9:
                    flashed.add((row, column))
                    energies[row][column] = 0
                    increment_energies(row, column, energies, flashed)
                elif energy > 0 or (row, column) not in flashed:
                    energies[row][column] += 1

        step += 1
        if all_simultaneous:
            if len(flashed) == (ROW_LIMIT + 1) * (COL_LIMIT + 1):

                return step
        else:
            flashes += len(flashed)
            if step == steps:
                break

    return flashes


if __name__ == "__main__":
    with open("files/input11.txt") as file:
        data = process_data(file)

    ROW_LIMIT = len(data) - 1
    COL_LIMIT = len(data[0]) - 1
    print(get_flashes(data, 100, all_simultaneous=True))
