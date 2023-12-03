from dataclasses import dataclass
from pathlib import Path
import re

# Brainstorming:
# Puzzle is 140x140
# Let's have upper left be 0x0
# A number can occupy multiple characters width-wise
# Symbols are only in one spot
# I'm wondering if we can parse everything into a series of Number objects and have a data structure storing where all symbols exist and then search after


@dataclass
class PartNumber:
    row: int
    col_start: int
    col_end: int
    value: int


@dataclass
class Schematic:
    part_numbers: list[PartNumber]
    # Mapping from row to a list of columns with a symbol
    symbol_locations: dict[int, list[int]]


def find_all_unique_chars(schematic: str):
    """
    Helper function to find what symbols exist
    """
    unique_chars = set()
    for char in schematic:
        if char.isdigit():
            continue
        unique_chars.add(char)

    print(unique_chars)


def parse_schematic(schematic: str) -> Schematic:
    part_numbers: list[PartNumber] = []
    symbol_locations: dict[int, list[int]] = {}

    # Going to use a regex here to be a bit lazy
    SCHEMATIC_LINE_RE = re.compile(r"\d+|[*#+$%/@=&-]")

    cur_row = 0
    for line in schematic.splitlines():
        for match in SCHEMATIC_LINE_RE.finditer(line):
            if match.group(0).isdigit():
                part_numbers.append(
                    PartNumber(
                        row=cur_row,
                        col_start=match.start(0),
                        col_end=match.end(0) - 1,
                        value=int(match.group(0)),
                    )
                )
            else:
                symbol_pos = match.start(0)
                if cur_row in symbol_locations:
                    symbol_locations[cur_row].append(symbol_pos)
                else:
                    symbol_locations[cur_row] = [symbol_pos]

        cur_row += 1

    return Schematic(part_numbers=part_numbers, symbol_locations=symbol_locations)


def places_to_check(part_number: PartNumber) -> list[tuple[int, int]]:
    locs_to_check: list[tuple[int, int]] = []

    # We have to check above and below every position a number occupies
    # We also have to check on the left and right of each end digit
    # And the diagnals of each end number

    # By doing the range back one and forward one, we'll get the diagnals of our digit too
    for col in range(part_number.col_start - 1, part_number.col_end + 2):
        # One row above
        locs_to_check.append((part_number.row - 1, col))

        # One row below
        locs_to_check.append((part_number.row + 1, col))

    # The left of the number
    locs_to_check.append((part_number.row, part_number.col_start - 1))

    # The right of the number
    locs_to_check.append((part_number.row, part_number.col_end + 1))

    return locs_to_check


def part1():
    raw_schematic = Path("./day3.input.txt").read_text()
    find_all_unique_chars(raw_schematic)

    schematic = parse_schematic(raw_schematic)

    cumulative_part_numbers = 0

    for part_number in schematic.part_numbers:
        # For each part number, we have to check if any of the surrounding spaces has a symbol on it

        locs_to_check = places_to_check(part_number)
        for loc in locs_to_check:
            # Check if this location we need to check is occupied by a symbol
            row, col = loc

            if row in schematic.symbol_locations:
                if col in schematic.symbol_locations[row]:
                    cumulative_part_numbers += part_number.value
                    break

    print("part1:", cumulative_part_numbers)


part1()
