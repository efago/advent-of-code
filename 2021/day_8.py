import re
from typing import Dict, List, Tuple


def get_groups(
    readings: List[str],
) -> Tuple[Dict[str, str], str, str, List[str], List[str]]:
    mapping = dict()
    fives = []
    sixes = []

    for reading in readings:
        reading = "".join(sorted(reading))
        if len(reading) == 5:
            fives.append(reading)
        elif len(reading) == 6:
            sixes.append(reading)
        elif len(reading) == 2:
            one = reading
            mapping[reading] = "1"
        elif len(reading) == 3:
            mapping[reading] = "7"
        elif len(reading) == 4:
            four = reading
            mapping[reading] = "4"
        else:
            mapping[reading] = "8"

    return mapping, one, four, fives, sixes


def get_mapping(readings: List[str]) -> Dict[str, str]:
    mapping, one, four, fives, sixes = get_groups(readings)
    all_ = set("abcdefg")

    for five in fives:
        if set(five + four) == all_:
            mapping[five] = "2"
        elif set(five + one) == set(five):
            mapping[five] = "3"
        else:
            mapping[five] = "5"

    for six in sixes:
        if set(six + one) == all_:
            mapping[six] = "6"
        elif set(six + four) == set(six):
            mapping[six] = "9"
        else:
            mapping[six] = "0"

    return mapping


def sum_decode(readings: List[str]) -> int:
    total = 0
    for reading in readings:
        outputs = re.findall(r"\w+", reading)
        mapping = get_mapping(outputs[:10])
        subtotal = ""
        for output in outputs[10:]:
            subtotal += mapping["".join(sorted(output))]

        total += int(subtotal)

    return total


def count_unique_segments(readings: List[str]) -> int:
    uniques = 0
    for reading in readings:
        outputs = re.findall(r"\w+", reading)[-4:]
        for output in outputs:
            if len(output.strip()) in [2, 3, 4, 7]:
                uniques += 1

    return uniques


if __name__ == "__main__":
    with open("files/input8.txt") as file:
        data = file.readlines()
    print(count_unique_segments(data))
    print(sum_decode(data))
