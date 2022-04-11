import re
from typing import List, Set, TextIO, Tuple


def process_data(file: TextIO) -> List[List[int]]:
    regex = re.compile(r"\d")
    data = [list(map(int, regex.findall(digits))) for digits in file]
    return data


def get_basin_size(
    row: int,
    column: int,
    row_limit: int,
    col_limit: int,
    visited: Set[Tuple[int, int]],
    data: List[List[int]],
) -> int:
    basin_size = 1
    visited.add((row, column))
    digit = data[row][column]
    condition = (
        lambda r, c: data[r][c] > digit and data[r][c] < 9 and (r, c) not in visited
    )
    if row > 0 and condition(row - 1, column):
        basin_size += get_basin_size(
            row - 1, column, row_limit, col_limit, visited, data
        )
    if row < row_limit and condition(row + 1, column):
        basin_size += get_basin_size(
            row + 1, column, row_limit, col_limit, visited, data
        )
    if column > 0 and condition(row, column - 1):
        basin_size += get_basin_size(
            row, column - 1, row_limit, col_limit, visited, data
        )
    if column < col_limit and condition(row, column + 1):
        basin_size += get_basin_size(
            row, column + 1, row_limit, col_limit, visited, data
        )

    return basin_size


def get_largest_basins(data: List[List[int]]) -> int:
    rows = len(data)
    columns = len(data[0])
    basin_sizes = []

    for row, digits in enumerate(data):
        for column, digit in enumerate(digits):
            if digit < 9:
                basin_sizes.append(
                    get_basin_size(row, column, rows - 1, columns - 1, set(), data)
                )

    basin_sizes.sort(reverse=True)
    return basin_sizes[0] * basin_sizes[1] * basin_sizes[2]


def get_risk_level(data: List[List[int]]) -> int:
    row_limit = len(data) - 1
    col_limit = len(data[0]) - 1
    risk_level = 0

    for row, digits in enumerate(data):
        for column, digit in enumerate(digits):
            if (
                (row == 0 or data[row - 1][column] > digit)
                and (row == row_limit or data[row + 1][column] > digit)
                and (column == 0 or digits[column - 1] > digit)
                and (column == col_limit or digits[column + 1] > digit)
            ):
                risk_level += int(digit) + 1

    return risk_level


if __name__ == "__main__":
    with open("files/input9.txt") as file:
        data = process_data(file)

    print(get_risk_level(data))
    print(get_largest_basins(data))
