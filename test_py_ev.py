from py_ev.py_ev import Evaluator

ev = Evaluator()


def test_reset():
    ev.reset()
    assert len(ev.deck) == 52
    assert ev.board == []


def test_build_deck():
    ev.reset()
    assert len(ev.build_deck()) == 52
    assert ev.new_deck == [(2, 1), (2, 2), (2, 3), (2, 4), (3, 1), (3, 2), (3, 3), (3, 4),
                           (4, 1), (4, 2), (4, 3), (4, 4),  (5, 1), (5, 2), (5, 3), (5, 4),
                           (6, 1), (6, 2), (6, 3), (6, 4), (7, 1), (7, 2), (7, 3), (7, 4),
                           (8, 1), (8, 2), (8, 3), (8, 4), (9, 1), (9, 2), (9, 3), (9, 4),
                           (10, 1), (10, 2), (10, 3), (10, 4), (11, 1), (11, 2), (11, 3), (11, 4),
                           (12, 1), (12, 2), (12, 3), (12, 4), (13, 1), (13, 2), (13, 3), (13, 4),
                           (14, 1), (14, 2), (14, 3), (14, 4)]


def test_deal():
    ev.reset()
    assert len(ev.deal(5)) == 5
    assert len(ev.deck) == 47


def test_set_cards():
    ev.reset()
    ev.board = ev.set_cards((14, 3), (2, 1), (12, 2))
    assert ev.board == [(14, 3), (2, 1), (12, 2)]
    assert len(ev.deck) == 49


def test_analyze_board():
    ev.reset()
    cards = [(6, 2), (6, 3), (3, 3), (2, 1)]
    board = [(7, 4), (5, 2), (12, 1), (13, 4), (7, 2)]
    total, pairness, suitness = ev.analyze_board(cards, board)
    assert pairness == {14: 0, 13: 1, 12: 1, 11: 0, 10: 0, 9: 0, 8: 0, 7: 2, 6: 2, 5: 1, 4: 0, 3: 1, 2: 1}
    assert suitness == {1: 2, 2: 3, 3: 2, 4: 2}
    assert total == [(13, 4), (12, 1), (7, 4), (7, 2), (6, 2), (6, 3), (5, 2), (3, 3), (2, 1)]


def test_is_str8():
    ev = Evaluator()

    cards, pairness, suitness = ev.analyze_board([(11, 2), (10, 3), (9, 4), (14, 3)],
                                                 [(2, 2), (3, 3), (8, 1), (7, 2), (4, 3)])
    result = ev.is_str8(cards, pairness, suitness)
    assert result == (5, 11, 'Straight')

    cards, pairness, suitness = ev.analyze_board([(11, 2), (10, 3), (12, 4), (14, 3)],
                                                 [(2, 2), (3, 3), (13, 1), (7, 2), (4, 3)])
    result = ev.is_str8(cards, pairness, suitness)
    assert result == (5, 14, 'Straight')

    cards, pairness, suitness = ev.analyze_board([(11, 2), (10, 3), (5, 4), (14, 3)],
                                                 [(2, 2), (3, 3), (13, 1), (7, 2), (4, 3)])
    result = ev.is_str8(cards, pairness, suitness)
    assert result == (5, 5, 'Straight')

    cards, pairness, suitness = ev.analyze_board([(11, 2), (10, 3), (5, 4), (14, 3)],
                                                 [(2, 2), (3, 3), (13, 1), (7, 2), (10, 3)])
    result = ev.is_str8(cards, pairness, suitness)
    assert result == (False, 0, None)


def test_is_flush():
    ev = Evaluator()

    cards, pairness, suitness = ev.analyze_board([(11, 2), (9, 2)],
                                                 [(2, 2), (3, 2), (8, 1), (7, 2), (4, 3)])
    result = ev.is_flush(cards, pairness, suitness)
    assert result == (6, 110000+9000+700+30+2, 'Flush')

    cards, pairness, suitness = ev.analyze_board([(11, 2), (10, 2)],
                                                 [(2, 2), (9, 2), (14, 2), (7, 2), (4, 2)])
    result = ev.is_flush(cards, pairness, suitness)
    assert result == (6, 140000+11000+1000+90+7, 'Flush')

    cards, pairness, suitness = ev.analyze_board([(11, 2), (9, 2)],
                                                 [(2, 2), (10, 2), (14, 2), (7, 3), (4, 3)])
    result = ev.is_flush(cards, pairness, suitness)
    assert result == (6, 140000+11000+1000+90+2, 'Flush')

    cards, pairness, suitness = ev.analyze_board([(2, 2), (4, 2)],
                                                 [(5, 2), (7, 2), (3, 2), (7, 4), (14, 2)])
    result = ev.is_flush(cards, pairness, suitness)
    assert result == (6, 140000+7000+500+40+3, 'Flush')

    cards, pairness, suitness = ev.analyze_board([(2, 2), (3, 2)],
                                                 [(5, 2), (7, 4), (8, 3), (7, 4), (4, 3)])
    result = ev.is_flush(cards, pairness, suitness)
    assert result == (False, 0, None)


def test_is_quad():
    ev = Evaluator()

    cards, pairness, suitness = ev.analyze_board([(11, 2), (10, 3), (9, 2), (14, 3)],
                                                 [(2, 2), (3, 2), (8, 1), (7, 2), (4, 3)])
    result = ev.is_quad(cards, pairness, suitness)
    assert result == (False, 0, None)

    cards, pairness, suitness = ev.analyze_board([(11, 2), (11, 3), (9, 2), (14, 3)],
                                                 [(2, 2), (3, 2), (11, 1), (7, 2), (4, 3)])
    result = ev.is_quad(cards, pairness, suitness)
    assert result == (False, 0, None)

    cards, pairness, suitness = ev.analyze_board([(11, 2), (11, 3), (9, 2), (14, 3)],
                                                 [(2, 2), (3, 2), (11, 1), (7, 2), (11, 3)])
    result = ev.is_quad(cards, pairness, suitness)
    assert result == (8, 110+14, 'Four of a Kind')

    cards, pairness, suitness = ev.analyze_board([(11, 2), (11, 3), (14, 2), (14, 3)],
                                                 [(2, 2), (14, 2), (11, 1), (14, 2), (11, 3)])
    result = ev.is_quad(cards, pairness, suitness)
    assert result == (8, 140+11, 'Four of a Kind')

    cards, pairness, suitness = ev.analyze_board([(11, 2), (11, 3)],
                                                 [(2, 2), (11, 4), (11, 1)])
    result = ev.is_quad(cards, pairness, suitness)
    assert result == (8, 110+2, 'Four of a Kind')

def test_is_fullhouse():
    ev = Evaluator()

    cards, pairness, suitness = ev.analyze_board([(11, 2), (11, 3)],
                                                 [(2, 2), (11, 1), (8, 1), (4, 2), (4, 3)])
    result = ev.is_fullhouse(cards, pairness, suitness)
    assert result == (7, 110+4, 'Full House')

    cards, pairness, suitness = ev.analyze_board([(11, 2), (11, 3)],
                                                 [(12, 2), (11, 1), (12, 1), (12, 4), (4, 3)])
    result = ev.is_fullhouse(cards, pairness, suitness)
    assert result == (7, 120+11, 'Full House')

    cards, pairness, suitness = ev.analyze_board([(11, 2), (11, 3)],
                                                 [(11, 4), (11, 1), (5, 1), (12, 4), (4, 3)])
    result = ev.is_fullhouse(cards, pairness, suitness)
    assert result == (False, 0, None)

    cards, pairness, suitness = ev.analyze_board([(11, 2), (11, 3)],
                                                 [(11, 4), (10, 1), (5, 1), (12, 4), (4, 3)])
    result = ev.is_fullhouse(cards, pairness, suitness)
    assert result == (False, 0, None)

    cards, pairness, suitness = ev.analyze_board([(11, 2), (11, 3)],
                                                 [(10, 4), (10, 1), (5, 1), (12, 4), (4, 3)])
    result = ev.is_fullhouse(cards, pairness, suitness)
    assert result == (False, 0, None)

def test_is_3_of_a_kind():
    ev = Evaluator()

    cards, pairness, suitness = ev.analyze_board([(11, 2), (11, 3)],
                                                 [(2, 2), (11, 1), (8, 1), (3, 2), (4, 3)])
    result = ev.is_3_of_a_kind(cards, pairness, suitness)
    assert result == (4, 1100+80+4, 'Three of a kind')

    cards, pairness, suitness = ev.analyze_board([(11, 2), (11, 3)],
                                                 [(2, 2), (10, 1), (8, 1), (3, 2), (4, 3)])
    result = ev.is_3_of_a_kind(cards, pairness, suitness)
    assert result == (False, 0, None)

    cards, pairness, suitness = ev.analyze_board([(11, 2), (12, 3)],
                                                 [(2, 2), (2, 1), (2, 3), (3, 2), (4, 3)])
    result = ev.is_3_of_a_kind(cards, pairness, suitness)
    assert result == (4, 200+120+11, 'Three of a kind')

    cards, pairness, suitness = ev.analyze_board([(11, 2), (11, 3)],
                                                 [(2, 2), (2, 1), (5, 3), (3, 2), (4, 3)])
    result = ev.is_3_of_a_kind(cards, pairness, suitness)
    assert result == (False, 0, None)

    cards, pairness, suitness = ev.analyze_board([(12, 4), (10, 1)],
                                                 [(10, 4), (10, 2), (4, 1), (3, 2), (2, 3)])
    result = ev.is_3_of_a_kind(cards, pairness, suitness)
    assert result == (4, 1000+120+4, 'Three of a kind')

def test_is_2_pairs():
    ev = Evaluator()

    cards, pairness, suitness = ev.analyze_board([(11, 2), (11, 3)],
                                                 [(12, 2), (12, 1), (3, 1), (3, 2), (4, 3)])
    result = ev.is_2_pairs(cards, pairness, suitness)
    assert result == (3, 1314, 'Two pair')

    cards, pairness, suitness = ev.analyze_board([(11, 2), (11, 3)],
                                                 [(12, 2), (12, 1), (3, 1), (3, 2), (14, 3)])
    result = ev.is_2_pairs(cards, pairness, suitness)
    assert result == (3, 1324, 'Two pair')

    cards, pairness, suitness = ev.analyze_board([(11, 2), (11, 3)],
                                                 [(10, 2), (12, 1), (3, 1), (3, 2), (14, 3)])
    result = ev.is_2_pairs(cards, pairness, suitness)
    assert result == (3, 1144, 'Two pair')

    cards, pairness, suitness = ev.analyze_board([(11, 2), (11, 3)],
                                                 [(10, 2), (12, 1), (2, 1), (3, 2), (14, 3)])
    result = ev.is_2_pairs(cards, pairness, suitness)
    assert result == (False, 0, None)

    cards, pairness, suitness = ev.analyze_board([(11, 2), (11, 3)],
                                                 [(10, 2), (11, 1), (2, 1), (3, 2), (14, 3)])
    result = ev.is_2_pairs(cards, pairness, suitness)
    assert result == (False, 0, None)

    cards, pairness, suitness = ev.analyze_board([(11, 2), (11, 3)],
                                                 [(11, 2), (11, 1), (2, 1), (3, 2), (14, 3)])
    result = ev.is_2_pairs(cards, pairness, suitness)
    assert result == (False, 0, None)

def test_is_pair():
    ev = Evaluator()

    cards, pairness, suitness = ev.analyze_board([(11, 2), (11, 3)],
                                                 [(13, 2), (14, 1), (2, 1), (3, 2), (4, 3)])
    result = ev.is_pair(cards, pairness, suitness)
    assert result == (2, 11000+1400+130+4, 'One pair')

    cards, pairness, suitness = ev.analyze_board([(10, 2), (11, 3)],
                                                 [(13, 2), (14, 1), (2, 1), (3, 2), (4, 3)])
    result = ev.is_pair(cards, pairness, suitness)
    assert result == (False, 0, None)

    cards, pairness, suitness = ev.analyze_board([(11, 2), (14, 3)],
                                                 [(13, 2), (14, 1), (2, 1), (3, 2), (4, 3)])
    result = ev.is_pair(cards, pairness, suitness)
    assert result == (2, 14000+1300+110+4, 'One pair')

def test_is_air():
    ev = Evaluator()

    cards, pairness, suitness = ev.analyze_board([(11, 2), (11, 3)],
                                                 [(13, 2), (14, 1), (2, 1), (3, 2), (4, 3)])
    result = ev.is_air(cards, pairness, suitness)
    assert result == (False, 0, None)

    cards, pairness, suitness = ev.analyze_board([(11, 2), (10, 3)],
                                                 [(13, 2), (14, 1), (2, 1), (3, 2), (4, 3)])
    result = ev.is_air(cards, pairness, suitness)
    assert result == (1, 140000+13000+1100+100+4, 'High card')

    cards, pairness, suitness = ev.analyze_board([(11, 2), (10, 3)],
                                                 [(13, 2), (14, 1), (2, 1), (3, 2), (2, 3)])
    result = ev.is_air(cards, pairness, suitness)
    assert result == (False, 0, None)

    cards, pairness, suitness = ev.analyze_board([(11, 2), (10, 3)],
                                                 [(13, 2), (14, 1), (2, 1), (3, 2), (8, 3)])
    result = ev.is_air(cards, pairness, suitness)
    assert result == (1, 140000+13000+1100+100+8, 'High card')

def test_is_str8_flush():
    ev = Evaluator()

    cards, pairness, suitness = ev.analyze_board([(11, 2), (12, 2)],
                                                 [(13, 2), (14, 2), (10, 2), (3, 2), (4, 3)])
    result = ev.is_str8_flush(cards, pairness, suitness)
    assert result == (9, 14, 'Straight Flush')

    cards, pairness, suitness = ev.analyze_board([(12, 2), (12, 2)],
                                                 [(13, 2), (14, 2), (10, 2), (3, 2), (4, 3)])
    result = ev.is_str8_flush(cards, pairness, suitness)
    assert result == (False, 0, None)

    cards, pairness, suitness = ev.analyze_board([(12, 2), (13, 2)],
                                                 [(13, 2), (8, 2), (10, 2), (3, 2), (4, 3)])
    result = ev.is_str8_flush(cards, pairness, suitness)
    assert result == (False, 0, None)

    cards, pairness, suitness = ev.analyze_board([(14, 2), (5, 2)],
                                                 [(13, 2), (8, 2), (2, 2), (3, 2), (4, 2)])
    result = ev.is_str8_flush(cards, pairness, suitness)
    assert result == (9, 5, 'Straight Flush')

    cards, pairness, suitness = ev.analyze_board([(14, 2), (5, 2)],
                                                 [(13, 2), (8, 2), (2, 2), (3, 3), (4, 2)])
    result = ev.is_str8_flush(cards, pairness, suitness)
    assert result == (False, 0, None)

def test_evaluate():
    ev = Evaluator()

    assert ev.evaluate([(3, 2), (3, 3)], [(3, 4), (10, 1), (12, 3), (14, 1), (6, 4)]) > \
           ev.evaluate([(10, 2), (12, 4)], [(3, 4), (10, 1), (12, 3), (14, 1), (6, 4)])

    assert ev.evaluate([(3, 2), (3, 3)], [(3, 4), (10, 1), (12, 3), (14, 1), (6, 4)]) > \
           ev.evaluate([(14, 2), (13, 4)], [(12, 4), (11, 1), (9, 3), (8, 1), (7, 4)])

    assert ev.evaluate([(2, 2), (2, 3)], [(2, 4), (3, 1), (3, 3), (14, 1), (6, 4)]) > \
           ev.evaluate([(14, 2), (13, 2)], [(12, 2), (11, 2), (9, 3), (8, 2), (7, 4)])

    assert ev.evaluate([(2, 2), (2, 3)], [(4, 4), (3, 1), (5, 3), (7, 1), (8, 4)]) > \
           ev.evaluate([(14, 2), (13, 2)], [(12, 2), (11, 2), (9, 3), (8, 1), (7, 4)])