from typing import Dict, List


def get_fishes(ages: List[int], days: int) -> int:
    for _ in range(days):
        new_fishes = []
        for i, age in enumerate(ages):
            if age == 0:
                new_fishes.append(8)
                ages[i] = 6
            else:
                ages[i] -= 1
        ages.extend(new_fishes)

    return len(ages)


def get_progenies(days: int, lookup: Dict[int, int]) -> int:
    if not lookup.get(days):
        total = 0
        for i in range(1, days, 7):
            total += get_progenies(days - i - 8, lookup) + 1

        lookup[days] = total

    return lookup[days]


def get_fishes_II(ages: List[int], days: int) -> int:
    fishes = len(ages)
    progenies: Dict[int, int] = dict()
    for age in ages:
        if not progenies.get(age):
            progenies[age] = get_progenies(days - age + 1, {})

        fishes += progenies[age]

    return fishes


if __name__ == "__main__":
    with open("files/input6.txt") as file:
        data = file.readline().split(",")
    print(get_fishes(list(map(int, data)), days=30))
    print(get_fishes_II(list(map(int, data)), days=256))
