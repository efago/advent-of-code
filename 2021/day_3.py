from typing import List


def get_ones(readings: List[str], index: int) -> List[int]:
    ones = []
    for i, reading in enumerate(readings):
        if reading[index] == "1":
            ones.append(i)

    return ones


def calculate_power(readings: List[str]) -> int:
    len_ = len(readings[0].strip())
    half = len(readings) // 2

    gamma_ = ""
    epsilon_ = ""
    for i in range(len_):
        if len(get_ones(readings, i)) >= half:
            gamma_ += "1"
            epsilon_ += "0"
        else:
            gamma_ += "0"
            epsilon_ += "1"

    gamma = int(gamma_, base=2)
    epsilon = int(epsilon_, base=2)

    return gamma * epsilon


def get_rating(readings: List[str], is_oxygen: bool = True) -> str:
    len_ = len(readings[0].strip())
    rating = readings.copy()

    for i in range(len_):
        ones = get_ones(rating, i)
        zeros = set(range(len(rating))) - set(ones)
        if is_oxygen:
            if len(ones) >= len(zeros):
                rating = [rating[i] for i in ones]
            else:
                rating = [rating[i] for i in zeros]
        else:
            if len(zeros) <= len(ones):
                rating = [rating[i] for i in zeros]
            else:
                rating = [rating[i] for i in ones]

        if len(rating) == 1:
            break

    return rating[0]


def calculate_life_support(readings: List[str]) -> int:
    oxygen = int(get_rating(readings), base=2)
    co2 = int(get_rating(readings, is_oxygen=False), base=2)

    return oxygen * co2


if __name__ == "__main__":
    with open("files/input3.txt") as file:
        report = file.readlines()
    print(calculate_power(report))
    print(calculate_life_support(report))
