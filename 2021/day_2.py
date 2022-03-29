from typing import List


def calculate_position(movements: List[str]) -> int:
    vertical = 0
    horizontal = 0
    for movement in movements:
        command, stp = movement.split()
        steps = int(stp)

        if command == "forward":
            horizontal += steps
        elif command == "up":
            vertical -= steps
        else:
            vertical += steps

    return vertical * horizontal


def calculate_position_aim(movements: List[str]) -> int:
    aim = 0
    depth = 0
    horizontal = 0

    for movement in movements:
        command, stp = movement.split()
        steps = int(stp)

        if command == "forward":
            horizontal += steps
            depth += aim * steps
        elif command == "up":
            aim -= steps
        else:
            aim += steps

    return depth * horizontal


if __name__ == "__main__":
    with open("files/input2.txt") as file:
        commands = file.readlines()
    print(calculate_position(commands))
    print(calculate_position_aim(commands))
