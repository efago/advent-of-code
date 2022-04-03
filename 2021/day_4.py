from typing import Any, Dict, List


def init_board(dimension: int = 5) -> Dict[str, Any]:
    board: Dict[str, Any] = dict()
    board["rows"] = []
    board["cols"] = [[] for _ in range(dimension)]

    return board


def get_boards(data_: List[str], dimension: int = 5) -> List[Dict]:
    boards = []
    board = init_board(dimension)
    for line in data_:
        if line == "\n":
            boards.append(board)
            board = init_board(dimension)
            continue

        numbers = line.strip().split()
        for i, number in enumerate(numbers):
            board["cols"][i].append(number)

        board["rows"].append(numbers)

    return boards


def sum_unmarked(board: Dict[str, List[Any]]) -> int:
    sum_ = 0
    for row in board["rows"]:
        sum_ += sum(int(num) for num in row)

    return sum_


def get_winner(
    random_numbers_: List[str], data_: List[str], pick_first: bool = True
) -> int:
    if not pick_first:
        winners = set()

    boards = get_boards(data_)
    for number in random_numbers_:
        for board_number, board in enumerate(boards):
            for i, row in enumerate(board["rows"]):
                if number in row:
                    col = row.index(number)
                    row[col] = 0
                    board["cols"][col][i] = 0
                    if not any(row) or not any(board["cols"][col]):
                        winners.add(board_number)
                        if pick_first or len(winners) == len(boards):
                            return int(number) * sum_unmarked(board)

                    break
    return 0


if __name__ == "__main__":
    with open("files/input4.txt") as file:
        random_numbers = file.readline().strip().split(",")
        file.readline()
        data = file.readlines()
    print(get_winner(random_numbers, data, pick_first=False))
