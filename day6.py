from pathlib import Path
from dataclasses import dataclass
# Time:     7   15  30
# Distance: 9   40  200
#
# Time for race 0 = 7 ms. Distance = 9 mm
# Time for race 1 = 15 ms. Distnace = 40 mm
#


@dataclass
class Race:
    time_ms: int
    distance_mm: int


def read_input() -> str:
    return Path("day6.input.txt").read_text()


def parse_input(problem_input: str) -> list[Race]:
    races = []

    times, distances = map(
        lambda s: map(int, s.split(":")[1].split()),
        problem_input.strip().splitlines(),
    )

    for time, distance in zip(times, distances):
        races.append(Race(time, distance))

    return races


def part1():
    # distance = (race_len_ms - hold_len_ms) * hold_len_ms
    #
    races = parse_input(read_input())

    total_ways_to_win = 1
    for race in races:
        win_count = 0
        for hold_len_ms in range(1, race.time_ms):
            distance = (race.time_ms - hold_len_ms) * hold_len_ms
            if distance > race.distance_mm:
                win_count += 1

        total_ways_to_win *= win_count

    print("part1", total_ways_to_win)


def parse_input_part2(problem_input: str) -> Race:
    time_raw, distance_raw = problem_input.strip().splitlines()
    time = int(time_raw.split(":")[1].replace(" ", ""))
    distance = int(distance_raw.split(":")[1].replace(" ", ""))

    return Race(time, distance)


def part2():
    # Surprised I could brute force this one with the previous answer
    race = parse_input_part2(read_input())

    win_count = 0
    for hold_len_ms in range(1, race.time_ms):
        distance = (race.time_ms - hold_len_ms) * hold_len_ms
        if distance > race.distance_mm:
            win_count += 1

    print("part2:", win_count)


part1()
part2()
