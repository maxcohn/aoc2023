from dataclasses import dataclass
from pathlib import Path


@dataclass
class RangeMap:
    destination_range_start: int
    source_range_start: int
    range_len: int
    range_delta: int


@dataclass
class GameBoard:
    maps: dict[tuple[str, str], list[RangeMap]]
    starting_seeds: list[int]


def parse_input(input: str) -> GameBoard:
    lines = input.splitlines()

    # We assume that the first line is always the sstarting eed list
    starting_seeds = list(map(int, lines.pop(0).split(":")[1].split()))

    maps: dict[tuple[str, str], list[RangeMap]] = {}

    cur_map: tuple[str, str] | None = None
    for line in lines:
        # Skip blank lines
        if line.strip() == "":
            continue

        # If this is the start of a mapping, get the new mapping name
        if line.strip().endswith("map:"):
            raw_map_name = line.split(" ")[0]
            cur_map = tuple(raw_map_name.split("-to-"))
            continue

        if not line[0].isdigit():
            assert False, "this shouldn't happen"

        destination_range_start, source_range_start, range_len = map(int, line.split())

        range_map = RangeMap(
            destination_range_start=destination_range_start,
            source_range_start=source_range_start,
            range_len=range_len,
            range_delta=source_range_start - destination_range_start,
        )

        if cur_map in maps:
            maps[cur_map].append(range_map)
        else:
            maps[cur_map] = [range_map]

    return GameBoard(maps, starting_seeds)


def part1():
    input_data = Path("./day5.input.txt").read_text()

    game_board = parse_input(input_data)

    location_nums = []
    for seed in game_board.starting_seeds:
        cur_val = seed

        # The map is actually ordered so that the previous destination is always the current start
        for (source_type, destination_type), range_maps in game_board.maps.items():
            for range_map in range_maps:
                if cur_val not in range(
                    range_map.source_range_start,
                    range_map.source_range_start + range_map.range_len,
                ):
                    continue

                cur_val = range_map.destination_range_start + (
                    cur_val - range_map.source_range_start
                )
                break
        location_nums.append(cur_val)

    print("part1:", min(location_nums))


def range_overlap(range1: tuple[int, int], range2: tuple[int, int]) -> range | None:
    # https://stackoverflow.com/a/6821298, modified

    if range1[1] > range2[0]:
        return None
    return range(max(range1[0], range2[0]), min(range1[-1], range2[-1]) + 1)


def part2():
    # The change to seed ranges in part 2 makes this much trickier.
    # We can't brute force compute this anymore, so we'll need to find a better way to represent this problem.
    input_data = Path("./day5.input.txt").read_text()

    game_board = parse_input(input_data)

    lowest_location_num = 9999999999999999

    # Convert starting seed list into range pairs
    starting_seed_ranges: list[tuple[int, int]] = []
    # Idiom for chunking arrays in Python. This is in Python 3.12 as itertools.batched.
    # https://stackoverflow.com/questions/16789776/iterating-over-two-values-of-a-list-at-a-time-in-python
    for pair in zip(*[iter(game_board.starting_seeds)] * 2):
        starting_seed_ranges.append((pair[0], pair[0] + pair[1]))

    for seed_range in starting_seed_ranges:
        print("starting seed range", seed_range)

        ranges_to_iter = [seed_range]

        # For each seed range, we want to check the overlap of it and the range maps
        # From there, we'll calculate the new ranges and continue onward
        for mapping_name, range_maps in game_board.maps.items():
            print("starting range map set", mapping_name)
            print("total ranges to iter:", len(ranges_to_iter))
            print(ranges_to_iter[0:5])
            modified_ranges = set()
            unmodified_ranges = set()

            seen_ranges = set()
            for range_map in range_maps:
                for cur_range in ranges_to_iter:
                    overlap = range_overlap(
                        cur_range,
                        (
                            range_map.source_range_start,
                            range_map.source_range_start + range_map.range_len,
                        ),
                    )
                    if overlap is None:
                        unmodified_ranges.add(cur_range)
                        continue
                    # print(overlap)

                    updated_range = (
                        overlap.start + range_map.range_delta,
                        overlap.stop + range_map.range_delta,
                    )

                    lower_range = (cur_range[0], overlap.start - 1)
                    upper_range = (overlap.stop + 1, cur_range[1])
                    modified_ranges.add(updated_range)

                    if lower_range not in seen_ranges:
                        seen_ranges.add(lower_range)
                        print(lower_range)
                        ranges_to_iter.append(lower_range)

                    if upper_range not in seen_ranges:
                        seen_ranges.add(upper_range)
                        ranges_to_iter.append(upper_range)

            ranges_to_iter = list(modified_ranges.union(unmodified_ranges))

        for cur_range in ranges_to_iter:
            if lowest_location_num > cur_range[0]:
                lowest_location_num = cur_range[0]

        print("\n\n\n\n\n")
        print("lowest:", lowest_location_num)

    print("part2:", lowest_location_num)


part1()
part2()
# print(range_overlap(range(0, 10), range(100, 200)))
