from typing import Dict, List


def get_incremental_fuel(distance: int, lookup: Dict[int, int]) -> int:
    if lookup.get(distance) is not None:  # Avoid mismatch of 0
        return lookup[distance]

    lookup[distance] = get_incremental_fuel(distance - 1, lookup) + distance
    return lookup[distance]


def gradient_descent(positions: List[int], incremental: bool = False) -> int:
    if incremental:
        fuels = {0: 0}
        fuel = lambda x: sum(
            get_incremental_fuel(abs(position - x), fuels) for position in positions
        )
    else:
        fuel = lambda x: sum(abs(position - x) for position in positions)

    search = sorted(set(data))
    while True:
        mid = len(search) // 2
        mid_fuel = fuel(search[mid])
        if mid - 1 >= 0 and fuel(search[mid - 1]) < mid_fuel:
            search = search[0:mid]
        elif mid + 1 < len(search) and fuel(search[mid + 1]) < mid_fuel:
            search = search[mid + 1 :]
        else:
            return mid_fuel


def cheapest_fuel_explore(positions: List[int], incremental: bool = False) -> int:
    positions = sorted(positions)
    if incremental:
        increments = {0: 0}
    fuels = []
    for p in positions:
        fuel = 0
        for position in positions:
            if incremental:
                fuel += get_incremental_fuel(abs(position - p), increments)
            else:
                fuel += abs(position - p)
        fuels.append(fuel)
    print(fuels.index(min(fuels)))
    return min(fuels)


def reddit_solution_partII() -> None:
    import numpy as np

    data = [int(x) for x in open("files/input7.txt", "r").read().split(",")]

    def sum_1_to_n(n):
        return n * (n + 1) / 2

    mean = int(np.mean(data))
    print(
        f"Part 2: The shortest amount of fuel spend is {sum([sum_1_to_n(abs(mean - i)) for i in data])}"
    )


if __name__ == "__main__":
    with open("files/input7.txt") as file:
        data = file.readline().split(",")
    data = list(map(int, data))
    print(gradient_descent(data))
    print(gradient_descent(data, incremental=True))  # 98119749
    reddit_solution_partII()    # 98119739.0
