import sys
sys.path.insert(0, '..')

import enum
from collections import defaultdict

from helpers import filemap


use_test_data = False
inp = filemap('input.txt') if not use_test_data else [
    '32T3K 765',
    'T55J5 684',
    'KK677 28',
    'KTJJT 220',
    'QQQJA 483'
] # 5905


class CamelCardsHand:
    CARD_LABELS   = 'AKQT98765432J'
    CARD_STRENGTH = dict(zip(list(CARD_LABELS), range(len(CARD_LABELS))))

    @enum.unique
    class STRENGTH(enum.IntEnum):
        FIVE       = 0 # Five of a kind
        FOUR       = 1 # Four of a kind
        FULL_HOUSE = 2 # Full House
        THREE      = 3 # Three of a kind
        TWO_PAIR   = 4 # Two pairs
        PAIR       = 5 # One pair
        HIGH       = 6 # High card

    def __init__(self, cards: str, bid_amount: int):
        if len(cards) != 5:
            raise ValueError('CamelCardsHand must contain exactly five cards')
        self.__cards = cards
        self.__bid_amount = bid_amount
        self.__strength = self.__compute_strength()


    @property
    def bid_amount(self) -> int:
        return self.__bid_amount

    @property
    def strength(self) -> 'CamelCardsHand.STRENGTH':
        return self.__strength


    def __lt__(self, other: 'CamelCardsHand') -> bool:
        strength_diff = self.strength - other.strength
        return (
            self.__cmp_cards_strength(other) < 0 if strength_diff == 0
            else strength_diff < 0
        )


    def __compute_strength(self) -> 'CamelCardsHand.STRENGTH':
        joker_cnt  = self.__cards.count('J')

        if joker_cnt == 4 or joker_cnt == 5:
            return CamelCardsHand.STRENGTH.FIVE

        labels_cnt = {}
        for c in self.__cards:
            if c == 'J':
                continue
            labels_cnt[c] = labels_cnt.get(c, 0) + 1
        different_cards_cnt = len(labels_cnt)

        # Handle special cases
        def get_hand_val_no_joker():
            if different_cards_cnt == 2:
                if 4 in labels_cnt.values():
                    return CamelCardsHand.STRENGTH.FOUR
                return CamelCardsHand.STRENGTH.FULL_HOUSE
            if different_cards_cnt == 3:
                if 3 in labels_cnt.values():
                    return CamelCardsHand.STRENGTH.THREE
                return CamelCardsHand.STRENGTH.TWO_PAIR

        # Lazy implementation
        # => hand_strengths[amount_of_j's][amount_of_differing_cards] => Best hand
        hand_strengths = {
            0: defaultdict(get_hand_val_no_joker, {
                1: CamelCardsHand.STRENGTH.FIVE,
                4: CamelCardsHand.STRENGTH.PAIR,
                5: CamelCardsHand.STRENGTH.HIGH
            }),
            1: defaultdict(
                lambda: CamelCardsHand.STRENGTH.FOUR if 3 in labels_cnt.values() else CamelCardsHand.STRENGTH.FULL_HOUSE, {
                    1: CamelCardsHand.STRENGTH.FIVE,
                    3: CamelCardsHand.STRENGTH.THREE,
                    4: CamelCardsHand.STRENGTH.PAIR
            }),
            2: {
                1: CamelCardsHand.STRENGTH.FIVE,
                2: CamelCardsHand.STRENGTH.FOUR,
                3: CamelCardsHand.STRENGTH.THREE
            },
            3: {
                1: CamelCardsHand.STRENGTH.FIVE,
                2: CamelCardsHand.STRENGTH.FOUR
            }
        }

        return hand_strengths[joker_cnt][different_cards_cnt]


    def __cmp_cards_strength(self, other: 'CamelCardsHand') -> int:
        for i, card in enumerate(self.__cards):
            if card == other.__cards[i]:
                continue
            return (
                CamelCardsHand.CARD_STRENGTH[card] -
                CamelCardsHand.CARD_STRENGTH[other.__cards[i]]
            )

        return 0


    def __str__(self):
        return '\t'.join((self.__cards, str(self.bid_amount), self.strength.name))


hands = [CamelCardsHand(*(hand[0], int(hand[1]))) for hand in map(str.split, inp)]
hands.sort(reverse=True)

winnings = sum(i * card.bid_amount for i,card in enumerate(hands, 1))
print(winnings)
