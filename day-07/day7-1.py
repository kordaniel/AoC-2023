import sys
sys.path.insert(0, '..')

from helpers import filemap


use_test_data = False
inp = filemap('input.txt') if not use_test_data else [
    '32T3K 765',
    'T55J5 684',
    'KK677 28',
    'KTJJT 220',
    'QQQJA 483'
] # 6440


class CamelCardsHand:
    CARD_LABELS   = 'AKQJT98765432'
    CARD_STRENGTH = dict(zip(list(CARD_LABELS), range(len(CARD_LABELS))))


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
    def strength(self) -> int:
        return self.__strength


    def __lt__(self, other: 'CamelCardsHand') -> bool:
        strength_diff = self.strength - other.strength
        return (
            self.__cmp_cards_strength(other) < 0 if strength_diff == 0
            else strength_diff < 0
        )


    def __compute_strength(self) -> int:
        labels_cnt = {}
        for c in self.__cards:
            labels_cnt[c] = labels_cnt.get(c, 0) + 1

        if len(labels_cnt) == 1:
            return 0     # five of a kind
        elif len(labels_cnt) == 2:
            if 4 in labels_cnt.values():
                return 1 # Four of a kind
            return 2     # Full house
        elif len(labels_cnt) == 3:
            if 3 in labels_cnt.values():
                return 3 # Three of a kind
            return 4     # Two pairs
        elif (len(labels_cnt)) == 4:
            return 5     # One pair
        else:
            return 6     # High Card


    def __cmp_cards_strength(self, other: 'CamelCardsHand') -> int:
        for i, card in enumerate(self.__cards):
            if card == other.__cards[i]:
                continue
            return (
                CamelCardsHand.CARD_STRENGTH[self.__cards[i]] -
                CamelCardsHand.CARD_STRENGTH[other.__cards[i]]
            )

        return 0


    def __str__(self):
        return '\t'.join((self.__cards, *map(str, (self.bid_amount, self.strength))))


hands = [CamelCardsHand(*(hand[0], int(hand[1]))) for hand in map(str.split, inp)]
hands.sort(reverse=True)

winnings = sum(i * card.bid_amount for i, card in enumerate(hands, 1))
print(winnings)
