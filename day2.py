from dataclasses import dataclass
import pathlib


@dataclass
class Roll:
    red_count: int
    blue_count: int
    green_count: int


@dataclass
class Game:
    game_id: int
    rolls: list[Roll]


def parse_line(line: str) -> Game:
    game, rest_game = line.split(":")
    game_id = game.replace("Game ", "")

    rolls_raw = rest_game.split(";")
    rolls = []
    for roll in rolls_raw:
        color_counts_raw = roll.split(",")
        color_counts = {"red": 0, "green": 0, "blue": 0}
        for color_count in color_counts_raw:
            num_str, color = color_count.strip().split(" ")
            color_counts[color] = int(num_str)

        rolls.append(
            Roll(
                blue_count=color_counts["blue"],
                green_count=color_counts["green"],
                red_count=color_counts["red"],
            )
        )

    return Game(int(game_id), rolls)


def part1():
    lines = pathlib.Path("day2.input.txt").read_text().splitlines()

    games = list(map(parse_line, lines))

    possible_game_ids = []

    # > only 12 red cubes, 13 green cubes, and 14 blue cubes
    for game in games:
        is_valid_game = True
        for roll in game.rolls:
            if roll.red_count > 12:
                is_valid_game = False
                break
            elif roll.green_count > 13:
                is_valid_game = False
                break
            elif roll.blue_count > 14:
                is_valid_game = False
                break

        if is_valid_game:
            possible_game_ids.append(game.game_id)

    print("part 1:", sum(possible_game_ids))


def part2():
    lines = pathlib.Path("day2.input.txt").read_text().splitlines()

    games = list(map(parse_line, lines))

    total_game_power = 0
    for game in games:
        red_max = max(map(lambda r: r.red_count, game.rolls))
        blue_max = max(map(lambda r: r.blue_count, game.rolls))
        green_max = max(map(lambda r: r.green_count, game.rolls))

        game_power = red_max * blue_max * green_max
        total_game_power += game_power

    print("part 2:", total_game_power)


part1()
part2()
