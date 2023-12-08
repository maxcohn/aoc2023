from pathlib import Path
from dataclasses import dataclass
import math


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


def is_finished(spaces: list[str]) -> bool:
    """Checks if the part2 puzzle is finished"""
    for space in spaces:
        if space[2] != "Z":
            return False
    return True


def part2():
    game = parse_input()

    # Find all starting spaces (those that end in 'A')
    starting_spaces = list(filter(lambda k: k[2] == "A", game.spaces.keys()))
    print(starting_spaces)

    first_cycles = []

    for space in starting_spaces:
        cur_space = space
        steps = 0
        while cur_space[2] != "Z":
            next_move = game.choices[steps % len(game.choices)]

            cur_space = game.spaces[cur_space][0 if next_move == "L" else 1]

            steps += 1
        first_cycles.append(steps)

    print("part2:", math.lcm(*first_cycles))


part1()  # 18827
part2()  # 20220305520997
