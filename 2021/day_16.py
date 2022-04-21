from math import prod
from typing import List, Tuple

MAP = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


def sum_version_numbers(packet: str) -> int:
    if int(packet) == 0 or not packet:
        return 0

    versions = 0
    index = 0

    version = packet[index : index + 3]
    versions += int(version, base=2)
    index += 3
    packet_type = packet[index : index + 3]
    index += 3

    if packet_type != "100":
        if packet[index] == "0":
            index += 16
        else:
            index += 12
    else:
        for i in range(index, len(packet), 5):
            index += 5
            if packet[i] == "0":
                break

    versions += sum_version_numbers(packet[index:])

    return versions


def apply_operator(operator: str, numbers: List[int]) -> int:
    if operator == "000":
        decoded = sum(numbers)
    elif operator == "001":
        decoded = prod(numbers)
    elif operator == "010":
        decoded = min(numbers)
    elif operator == "011":
        decoded = max(numbers)
    elif operator == "101":
        if numbers[0] > numbers[1]:
            decoded = 1
        else:
            decoded = 0
    elif operator == "110":
        if numbers[0] < numbers[1]:
            decoded = 1
        else:
            decoded = 0
    else:
        if numbers[0] == numbers[1]:
            decoded = 1
        else:
            decoded = 0
    return decoded


def decode_literal(packet: str) -> Tuple[int, str]:
    literal = ""
    for i in range(0, len(packet), 5):
        literal += packet[i + 1 : i + 5]
        if packet[i] == "0":
            break

    return int(literal, 2), packet[i + 5 :]


def get_expression(all_packets: str) -> Tuple[List[int], str]:
    if not all_packets or int(all_packets) == 0:
        return [], ""

    expression = []
    packet_type = all_packets[3:6]
    if packet_type == "100":
        code_, packet = decode_literal(all_packets[6:])
        expression.append(code_)
    else:
        codes_subpackets = []
        if all_packets[6] == "0":
            len_subpackets = int(all_packets[7:22], 2)
            packet = all_packets[22 + len_subpackets :]
            next_packet = all_packets[22:]
            while next_packet != packet:
                code, next_packet = get_expression(next_packet)
                codes_subpackets.append(int(code[0]))
        else:
            subpackets = int(all_packets[7:18], 2)
            packet = all_packets[18:]
            for _ in range(subpackets):
                code, packet = get_expression(packet)
                codes_subpackets.append(int(code[0]))

        expression.append(apply_operator(packet_type, codes_subpackets))

    return expression, packet


if __name__ == "__main__":
    with open("files/input16.txt") as file:
        message = ""
        codes = file.read().strip()
        for code in codes:
            message += MAP[code]

    print(sum_version_numbers(message))
    print(get_expression(message)[0][0])
