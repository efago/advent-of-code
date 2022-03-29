"""Problem statement at https://adventofcode.com/2021/day/1"""
from pathlib import Path
from typing import List

import click


def count_increase(measurements: List[int]) -> int:
    increases = 0
    previous_measurement = measurements[0]
    for measurement in measurements:
        if measurement > previous_measurement:
            increases += 1

        previous_measurement = measurement

    return increases


def count_window_increase(measurements: List[int]) -> int:
    increases = 0
    previous = sum(measurements[: 3])
    for i in range(len(measurements) - 2):
        current = sum(measurements[i: i + 3])
        if current > previous:
            increases += 1

        previous = current

    return increases


@click.command()
@click.option("--input_file", type=click.Path(), default="input1.txt")
def cli(input_file: Path) -> None:
    with open(input_file) as file:
        measurements = [int(line) for line in file]

    print("All increases:", count_increase(measurements))
    print("3 window increases:", count_window_increase(measurements))


if __name__ == "__main__":
    print(cli())
