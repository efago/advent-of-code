from typing import List, Optional, Tuple


def get_syntax_errors(
    chunks: List[str], autocomplete: bool = False
) -> Tuple[int, Optional[int]]:
    error_weights = {")": 3, "]": 57, "}": 1197, ">": 25137}
    closers = {")": "(", "]": "[", "}": "{", ">": "<"}
    if autocomplete:
        completion_weight = {"(": 1, "[": 2, "{": 3, "<": 4}
        autocomplete_scores = []

    syntax_errors = 0
    completion_score = None
    for chunk in chunks:
        delimiters: List[str] = []
        is_corrupt = False
        for delimiter in chunk.strip():
            if delimiter in closers:
                if closers[delimiter] != delimiters.pop():
                    syntax_errors += error_weights[delimiter]
                    is_corrupt = True
                    break
            else:
                delimiters.append(delimiter)

        if autocomplete and not is_corrupt:
            autocomplete_score = 0
            while delimiters:
                autocomplete_score = (
                    autocomplete_score * 5 + completion_weight[delimiters.pop()]
                )

            autocomplete_scores.append(autocomplete_score)

    if autocomplete:
        autocomplete_scores.sort()
        completion_score = autocomplete_scores[len(autocomplete_scores) // 2]

    return syntax_errors, completion_score


if __name__ == "__main__":
    with open("files/input10.txt") as file:
        data = file.readlines()

    print(get_syntax_errors(data))
    print(get_syntax_errors(data, autocomplete=True))
