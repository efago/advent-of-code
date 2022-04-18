from collections import defaultdict
from typing import Any, Dict, TextIO


def process_file(file: TextIO) -> Dict[str, Any]:
    lines = file.read().splitlines()
    info = {"template": lines[0], "rules": dict()}

    for rule in lines[2:]:
        pair, insert = rule.split(" -> ")
        info["rules"][pair] = insert

    return info


def get_min_max_diff(info: Dict[str, Any], steps: int = 10) -> int:
    template = info["template"]
    rules = info["rules"]

    for _ in range(steps):
        new_template = ""
        for i in range(0, len(template) - 1):
            pair = template[i : i + 2]
            new_template += pair[0] + rules[pair]

        template = new_template + template[-1]

    min_letter = len(template)
    max_letter = 0

    for letter in set(template):
        count = template.count(letter)
        if count < min_letter:
            min_letter = count
        if count > max_letter:
            max_letter = count

    return max_letter - min_letter


def get_counts(
    template: str,
    rules: Dict[str, str],
    pair_counts: defaultdict[int, defaultdict[str, defaultdict[str, int]]],
    step: int,
    max_steps: int = 40,
) -> defaultdict[int, defaultdict[str, defaultdict[str, int]]]:
    if step < max_steps:
        for i in range(0, len(template) - 1):
            pair = template[i : i + 2]
            if pair_counts[step][pair]:
                continue

            insertion = rules[pair]
            pair_counts[step][pair][insertion] += 1
            new_template = pair[0] + insertion + pair[1]
            get_counts(new_template, rules, pair_counts, step + 1, max_steps)

            for p in [pair[0] + insertion, insertion + pair[1]]:
                for letter, count in pair_counts[step + 1][p].items():
                    pair_counts[step][pair][letter] += count

    return pair_counts


def get_min_max_diff_II(info: Dict[str, Any], steps: int = 40) -> int:
    template = info["template"]
    rules = info["rules"]
    pair_counts: defaultdict[
        int, defaultdict[str, defaultdict[str, int]]
    ] = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    letter_counts: defaultdict[str, int] = defaultdict(int)

    template_pairs = get_counts(template, rules, pair_counts, 0, max_steps=steps)[0]

    for i in range(0, len(template) - 1):
        pair = template[i : i + 2]
        letter_counts[template[i]] += 1
        for letter, count in template_pairs[pair].items():
            letter_counts[letter] += count

    letter_counts[template[-1]] += 1

    counts = letter_counts.values()
    return max(counts) - min(counts)


if __name__ == "__main__":
    with open("files/input14.txt") as file:
        info = process_file(file)

    print(get_min_max_diff(info))
    print(get_min_max_diff_II(info))
