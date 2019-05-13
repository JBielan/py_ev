import random


class Evaluator:
    def __init__(self):
        self.deck = []
        self.cards_1 = ()
        self.cards_2 = ()
        self.board = []
        self.new_deck = self.build_deck()
        self.reset()

    def reset(self):
        self.deck = self.new_deck.copy()
        self.board = []
        self.cards_1 = self.cards_2 = ()

    @staticmethod
    def build_deck():
        new = []
        for f in range(2, 15):
            for s in range(1, 5):
                new.append((f, s))
        return new

    def deal(self, n):
        cards = []
        for _ in range(n):
            i = random.choice(range(len(self.deck)))
            cards.append(self.deck.pop(i))
        return cards

    def set_cards(self, *args):
        self.deck = [x for x in self.deck if x not in args]
        return list(args)

    @staticmethod
    def analyze_board(holecards, board):
        cards = holecards + board

        def sort_figures(elem):
            return int(elem[0])

        cards.sort(key=sort_figures, reverse=True)

        pairness = {i: 0 for i in range(14, 1, -1)}
        suitness = {i: 0 for i in range(1, 5)}

        for card in cards:
            pairness[card[0]] += 1
            suitness[card[1]] += 1

        return cards, pairness, suitness

    @staticmethod
    def is_str8(cards, pairness, suitness):
        indexes = [14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 14]
        best = 0
        count = 0
        for i in indexes:
            if pairness[i] != 0:
                count += 1
            else:
                count = 0
            if count > best:
                best = count
            if best == 5:
                if i == 14:
                    kicker = 5
                else:
                    kicker = i+4
                return True, kicker

        return False, 0

    @staticmethod
    def is_flush(cards, pairness, suitness):
        key = [k for k,v in suitness.items() if v==max(suitness.values())][0]
        if suitness[key] < 5:
            return False, 0
        else:
            if len(cards) < 10:
                kickers = [card[0] for card in cards if card[1] == key]
                return True, kickers[4] + kickers[3]*10 + kickers[2]*100 + kickers[1]*1000 + kickers[0]*10000
            else:
                second_key = [k for k,v in suitness.items() if v == sorted(suitness.values())[-2]][0]
                if suitness[second_key] < 5:
                    kickers = [card[0] for card in cards if card[1] == key]
                    return True, kickers[4] + kickers[3] * 10 + kickers[2] * 100 + kickers[1] * 1000 + kickers[
                        0] * 10000
                else:
                    kickers_second = [card[0] for card in cards if card[1] == second_key]
                    kickers_second_v = kickers_second[4] + kickers_second[3]*10 + kickers_second[2]*100 \
                                       + kickers_second[1]*1000 + kickers_second[0]*10000

                    kickers = [card[0] for card in cards if card[1] == key]
                    kickers_v = kickers[4] + kickers[3]*10 + kickers[2]*100 + kickers[1]*1000 + kickers[0]*10000

                    if kickers_v >= kickers_second_v:
                        return True, kickers_v
                    else:
                        return True, kickers_second_v
    @staticmethod
    def is_quad(cards, pairness, suitness):
        pass



ev = Evaluator()

cards, pairness, suitness = ev.analyze_board([(14, 3), (10, 3), (9, 3), (14, 3), (5, 4)], [(2, 2), (3, 2), (8, 1), (7, 2), (4, 3)])

print(ev.is_flush(cards, pairness, suitness))