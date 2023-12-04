from pathlib import Path
from dataclasses import dataclass


@dataclass
class GameCard:
    winning_numbers: list[int]
    given_numbers: list[int]


def read_input() -> list[str]:
    return Path("./day4.input.txt").read_text().splitlines()


def parse_cards(lines: list[str]) -> list[GameCard]:
    cards = []
    for line in lines:
        # Should just have one colon after the card identifier
        line = line.split(":")[1]

        # Only have one pipe separating number types
        winning_raw, given_raw = map(str.strip, line.split("|"))

        cards.append(
            GameCard(
                winning_numbers=list(
                    map(lambda n: int(n.strip()), winning_raw.split())
                ),
                given_numbers=list(map(lambda n: int(n.strip()), given_raw.split())),
            )
        )
    return cards


def calculate_card_value(card: GameCard) -> int:
    matching_num_count = len(
        set(card.winning_numbers).intersection(set(card.given_numbers))
    )
    if matching_num_count == 0 or matching_num_count == 1:
        return matching_num_count

    return 2 ** (matching_num_count - 1)


def part1():
    input_lines = read_input()
    all_cards = parse_cards(input_lines)

    cumulative_card_value = 0
    for card in all_cards:
        print(card)
        card_val = calculate_card_value(card)
        print(card_val)
        cumulative_card_value += card_val

    print("part1:", cumulative_card_value)


part1()
