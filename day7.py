from pathlib import Path
from dataclasses import dataclass
import functools
from enum import Enum


class HandType(Enum):
    """
    Higher number is better
    """

    FiveOfAKind = 7
    FourOfAKind = 6
    FullHouse = 5
    ThreeOfAKind = 4
    TwoPair = 3
    OnePair = 2
    HighCard = 1


@dataclass
class CardHand:
    cards: str
    bid: int


def parse_input() -> list[CardHand]:
    hands = []
    for line in Path("./day7.input.txt").read_text().splitlines():
        cards, bid_raw = line.split(" ")
        hands.append(CardHand(cards, int(bid_raw)))

    return hands


CARDS_IN_ORDER_LEAST_TO_GREATEST_PART_1 = [
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "T",
    "J",
    "Q",
    "K",
    "A",
]


def get_card_value(card: str) -> int:
    return CARDS_IN_ORDER_LEAST_TO_GREATEST_PART_1.index(card)


def check_hand_type(hand: CardHand) -> HandType:
    # Get the occurences of each char
    char_counts = {}
    for card in hand.cards:
        cur_count = char_counts.get(card, 0)
        char_counts[card] = cur_count + 1

    print(char_counts)
    found_three = False
    pair_count = 0
    for card, count in sorted(char_counts.items(), key=lambda i: i[1]):
        if count == 5:
            return HandType.FiveOfAKind
        if count == 4:
            return HandType.FourOfAKind
        if count == 3:
            found_three = True
        if count == 2:
            pair_count += 1

    if found_three and pair_count > 0:
        return HandType.FullHouse

    if found_three:
        return HandType.ThreeOfAKind

    if pair_count == 2:
        return HandType.TwoPair
    if pair_count == 1:
        return HandType.OnePair

    return HandType.HighCard


def hand_comparison(hand1: CardHand, hand2: CardHand) -> int:
    # Get the hand type for each hand
    hand1_type = check_hand_type(hand1)
    hand2_type = check_hand_type(hand2)
    print(f"{hand1_type=}")
    print(f"{hand2_type=}")

    if hand1_type.value > hand2_type.value:
        return 1
    if hand2_type.value > hand1_type.value:
        return -1

    for i in range(0, 5):
        hand1_card = get_card_value(hand1.cards[i])
        hand2_card = get_card_value(hand2.cards[i])

        if hand1_card > hand2_card:
            return 1
        if hand2_card > hand1_card:
            return -1

    return 0


def part1():
    # I think what we really want, is a sort comparison function.
    # Then I think we can let the default sort, handle it

    all_hands = parse_input()

    # Sorted from least to greatest
    all_hands.sort(key=functools.cmp_to_key(hand_comparison))

    total = 0
    for rank, hand in enumerate(all_hands):
        total += (rank + 1) * hand.bid

    print("part1:", total)


CARDS_IN_ORDER_LEAST_TO_GREATEST_PART_2 = [
    "J",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "T",
    "Q",
    "K",
    "A",
]


def get_card_value_part2(card: str) -> int:
    if card == "J":
        return -1
    return CARDS_IN_ORDER_LEAST_TO_GREATEST_PART_2.index(card)


def check_hand_type_part2(hand: CardHand) -> HandType:
    # Get the occurences of each char
    char_counts = {}
    for card in hand.cards:
        cur_count = char_counts.get(card, 0)
        char_counts[card] = cur_count + 1

    # If there's a joker, we just want to put it into the card with the highest
    if "J" in char_counts:
        joker_count = char_counts["J"]
        # This got a bit hacky here but I don't care
        if joker_count == 5:
            return HandType.FiveOfAKind
        del char_counts["J"]
        highest_card = max(char_counts, key=char_counts.get)
        char_counts[highest_card] += joker_count

    found_three = False
    pair_count = 0
    for card, count in sorted(char_counts.items(), key=lambda i: i[1]):
        if count == 5:
            return HandType.FiveOfAKind
        if count == 4:
            return HandType.FourOfAKind
        if count == 3:
            found_three = True
        if count == 2:
            pair_count += 1

    if found_three and pair_count > 0:
        return HandType.FullHouse

    if found_three:
        return HandType.ThreeOfAKind

    if pair_count == 2:
        return HandType.TwoPair
    if pair_count == 1:
        return HandType.OnePair

    return HandType.HighCard


def hand_comparison_part2(hand1: CardHand, hand2: CardHand) -> int:
    # Get the hand type for each hand
    hand1_type = check_hand_type_part2(hand1)
    hand2_type = check_hand_type_part2(hand2)
    print(f"{hand1_type=}")
    print(f"{hand2_type=}")

    if hand1_type.value > hand2_type.value:
        return 1
    if hand2_type.value > hand1_type.value:
        return -1

    for i in range(0, 5):
        hand1_card = get_card_value_part2(hand1.cards[i])
        hand2_card = get_card_value_part2(hand2.cards[i])

        if hand1_card > hand2_card:
            return 1
        if hand2_card > hand1_card:
            return -1

    return 0


def part2():
    all_hands = parse_input()

    # Sorted from least to greatest
    all_hands.sort(key=functools.cmp_to_key(hand_comparison_part2))

    for hand in all_hands:
        print(hand)

    total = 0
    for rank, hand in enumerate(all_hands):
        total += (rank + 1) * hand.bid

    print("part2:", total)


# print(hand_comparison_part2(CardHand("KTJJT", 0), CardHand("QQQJA", 0)))
# part1()
part2()
