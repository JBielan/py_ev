import random
from sys import stdout

class Evaluator:
    def __init__(self):
        self.deck = []
        self.board = []
        self.new_deck = self.build_deck()
        self.reset()

    def reset(self):
        self.deck = self.new_deck.copy()

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

    def remove_cards(self, cards):
        for card in cards:
            self.deck.remove(card)

    @staticmethod
    def analyze_board(holecards, board):
        cards = holecards + board

        # is there a necessity to sort for sure?! RIGHT NOW FOR STR8-FLUSH
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
        count = 0
        for i in indexes:
            if pairness[i] != 0:
                count += 1
            else:
                count = 0
            if count == 5:
                if i == 14:
                    kicker = 5
                else:
                    kicker = i+4
                return 5, kicker, 'Straight'

        return False, 0, None

    @staticmethod
    def is_flush(cards, pairness, suitness):
        key = [k for k,v in suitness.items() if v==max(suitness.values())][0]
        if suitness[key] < 5:
            return False, 0, None
        else:
            kickers = [card[0] for card in cards if card[1] == key]
            return 6, kickers[4] + kickers[3]*10 + kickers[2]*100 + kickers[1]*1000 + kickers[0]*10000, 'Flush'

    @staticmethod
    def is_quad(cards, pairness, suitness):
        key_max = max(pairness, key=pairness.get)
        if pairness[key_max] == 4:
            kicker = []
            for key in pairness:
                if pairness[key] > 0 and key != key_max:
                    if len(kicker) < 1:
                        kicker.append(key)
                    else:
                        break
            return 8, key_max * 10 + kicker[0], 'Four of a Kind'
        else:
            return False, 0, None

    @staticmethod
    def is_fullhouse(cards, pairness, suitness):
        key_2_max = sorted(pairness, key=pairness.get, reverse=True)[:2]
        if pairness[key_2_max[0]] < 3 or pairness[key_2_max[1]] < 2:
            return False, 0, None
        else:
            if pairness[key_2_max[1]] == 2:
                return 7, key_2_max[0] * 10 + key_2_max[1], 'Full House'
            elif pairness[key_2_max[1]] == 3:
                return 7, key_2_max[0] * 10 + key_2_max[1], 'Full House'
            else:
                print('Fullhouse pairness > 3')

    @staticmethod
    def is_3_of_a_kind(cards, pairness, suitness):
        key_max = max(pairness, key=pairness.get)
        if pairness[key_max] == 3:
            kickers = []
            for key in pairness:
                if pairness[key] > 0 and key != key_max:
                    if len(kickers) < 2:
                        kickers.append(key)
                    else:
                        break
            return 4, key_max * 100 + kickers[0] * 10 + kickers[1], 'Three of a kind'
        else:
            return False, 0, None

    @staticmethod
    def is_2_pairs(cards, pairness, suitness):
        # it's sorted so 3x2pairs works fine
        key_2_max = sorted(pairness, key=pairness.get, reverse=True)[:2]
        if pairness[key_2_max[0]] != 2 or pairness[key_2_max[1]] != 2:
            return False, 0, None
        elif pairness[key_2_max[0]] == 2 and pairness[key_2_max[1]] == 2:
            for key in pairness:
                if pairness[key] != 0 and key != key_2_max[0] and key != key_2_max[1]:
                    kicker = key
                    break
            return 3, key_2_max[0] * 100 + key_2_max[1] * 10 + kicker, 'Two pair'

    @staticmethod
    def is_pair(cards, pairness, suitness):
        key_max = max(pairness, key=pairness.get)
        if pairness[key_max] == 2:
            kickers = []
            for key in pairness:
                if pairness[key] > 0 and key != key_max:
                    if len(kickers) < 3:
                        kickers.append(key)
                    else:
                        break
            return 2, key_max * 1000 + kickers[0] * 100 + kickers[1] * 10 + kickers[2], 'One pair'
        else:
            return False, 0, None

    @staticmethod
    def is_air(cards, pairness, suitness):
        key_max = max(pairness, key=pairness.get)
        if pairness[key_max] == 1:
            kickers = []
            for key in pairness:
                if pairness[key] > 0:
                    if len(kickers) < 5:
                        kickers.append(key)
                    else:
                        break
            return 1, kickers[0] * 10000 + kickers[1] * 1000 + kickers[2] * 100 + kickers[3] * 10 + kickers[4], 'High card'
        else:
            print('Something missed all filters!')
            print(cards)
            key_max = max(pairness, key=pairness.get)
            print(key_max)
            print(pairness[key_max])
            return False, 0, None

    @staticmethod
    def is_str8_flush(cards, pairness, suitness):
        key = [k for k,v in suitness.items() if v==max(suitness.values())][0]
        if suitness[key] < 5:
            return False, 0, None
        else:
            indexes = [14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 14]
            flush = [card[0] for card in cards if card[1] == key]
            count = 0
            for idx in indexes:
                if idx in flush:
                    count += 1
                else:
                    count = 0
                if count == 5:
                    if idx == 14:
                        return 9, 5, 'Straight Flush'
                    else:
                        return 9, idx+4, 'Straight Flush'
            return False, 0, None

    def evaluate(self, holecards, board, ranking=True, name=False):
        ev = Evaluator()

        functions = [self.is_str8_flush, self.is_quad, self.is_fullhouse, self.is_flush, self.is_str8,
                     self.is_3_of_a_kind, self.is_2_pairs, self.is_pair, self.is_air]
        try:
            self.remove_cards(holecards)
            self.remove_cards(board)
        except:
            raise Exception('It looks like you set 2 or more the same cards.')
        self.reset()

        cards, pairness, suitness = ev.analyze_board(holecards, board)

        for function in functions:
            rank, kickers, name = function(cards, pairness, suitness)
            if rank:
                if ranking and not name:
                    return rank * 1000000 + kickers
                elif ranking and name:
                    return rank * 1000000 + kickers, name
                elif name and not ranking:
                    return name

    def equity(self, n, holecards_1, holecards_2, default_board=[]):
        functions = [self.is_str8_flush, self.is_quad, self.is_fullhouse, self.is_flush, self.is_str8,
                     self.is_3_of_a_kind, self.is_2_pairs, self.is_pair, self.is_air]

        won_1 = 0
        won_2 = 0
        draw = 0

        for hand_number in range(1, n + 1):
            board = default_board.copy()
            self.reset()
            self.remove_cards(holecards_1)
            self.remove_cards(holecards_2)
            if len(board) > 0:
                self.remove_cards(board)

            if len(board) < 5:
                board += self.deal(5 - len(board))

            cards_1, pairness_1, suitness_1 = self.analyze_board(holecards_1, board)
            cards_2, pairness_2, suitness_2 = self.analyze_board(holecards_2, board)

            for function in functions:
                result_1 = function(cards_1, pairness_1, suitness_1)
                result_2 = function(cards_2, pairness_2, suitness_2)
                if result_1[0] and not result_2[0]:
                    won_1 += 1
                    break
                elif not result_1[0] and result_2[0]:
                    won_2 += 1
                    break
                elif result_1[0] and result_2[0]:
                    if result_1[1] > result_2[1]:
                        won_1 += 1
                        break
                    elif result_1[1] < result_2[1]:
                        won_2 += 1
                        break
                    elif result_1[1] == result_2[1]:
                        draw += 1
                        break

            if hand_number % 10000 == 0:
                stdout.write("\r%d hands evaluated" % hand_number)
                stdout.flush()

        percentage_1 = won_1 / n * 100
        percentage_2 = won_2 / n * 100
        percentage_draw = draw / n * 100

        print('\n\nCards 1: {:.2f}%'.format(percentage_1))
        print('Cards 2: {:.2f}%'.format(percentage_2))
        print('Draw: {:.2f}%'.format(percentage_draw))


# ev = Evaluator()
#
# ev.equity(5000000, [(2, 3), (3, 2)], [(3, 3), (4, 2)])
