from pathlib import Path
from dataclasses import dataclass


@dataclass
class Game:
    choices: str
    spaces: dict[str, tuple[str]]


def parse_input() -> Game:
    input_lines = Path("./day8.input.txt").read_text().splitlines()

    choices_raw = input_lines.pop(0)

    input_lines.pop(0)

    spaces: dict[str, tuple[str, str]] = {}

    for line in input_lines:
        cur_space, raw_choices = line.split("=")
        tuple(raw_choices.replace("(", "").replace(")", "").replace(" ", "").split(","))
        spaces[cur_space.strip()] = tuple(
            raw_choices.replace("(", "").replace(")", "").replace(" ", "").split(",")
        )

    return Game(choices=choices_raw, spaces=spaces)


def part1():
    game = parse_input()

    cur_space = "AAA"
    steps = 0
    while cur_space != "ZZZ":
        next_move = game.choices[steps % len(game.choices)]

        cur_space = game.spaces[cur_space][0 if next_move == "L" else 1]

        steps += 1

    print("part1:", steps)


part1()  # 18827
