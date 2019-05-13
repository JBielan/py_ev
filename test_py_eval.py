from py_eval import Evaluator

ev = Evaluator()


def test_reset():
    ev.reset()
    assert len(ev.deck) == 52
    assert ev.cards_1 == ev.cards_2 == ()
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
    assert result == (True, 11)

    cards, pairness, suitness = ev.analyze_board([(11, 2), (10, 3), (12, 4), (14, 3)],
                                                 [(2, 2), (3, 3), (13, 1), (7, 2), (4, 3)])
    result = ev.is_str8(cards, pairness, suitness)
    assert result == (True, 14)

    cards, pairness, suitness = ev.analyze_board([(11, 2), (10, 3), (5, 4), (14, 3)],
                                                 [(2, 2), (3, 3), (13, 1), (7, 2), (4, 3)])
    result = ev.is_str8(cards, pairness, suitness)
    assert result == (True, 5)

    cards, pairness, suitness = ev.analyze_board([(11, 2), (10, 3), (5, 4), (14, 3)],
                                                 [(2, 2), (3, 3), (13, 1), (7, 2), (10, 3)])
    result = ev.is_str8(cards, pairness, suitness)
    assert result == (False, 0)


def test_is_flush():
    ev = Evaluator()

    cards, pairness, suitness = ev.analyze_board([(11, 2), (10, 3), (9, 2), (14, 3)],
                                                 [(2, 2), (3, 2), (8, 1), (7, 2), (4, 3)])
    result = ev.is_flush(cards, pairness, suitness)
    assert result == (True, 110000+9000+700+30+2)

    cards, pairness, suitness = ev.analyze_board([(11, 2), (10, 2), (9, 2), (14, 2)],
                                                 [(2, 2), (3, 2), (8, 1), (7, 2), (4, 2)])
    result = ev.is_flush(cards, pairness, suitness)
    assert result == (True, 140000+11000+1000+90+7)

    cards, pairness, suitness = ev.analyze_board([(11, 2), (10, 2), (9, 2), (14, 2), (14, 3)],
                                                 [(2, 2), (3, 3), (8, 3), (7, 3), (4, 3)])
    result = ev.is_flush(cards, pairness, suitness)
    assert result == (True, 140000+11000+1000+90+2)

    cards, pairness, suitness = ev.analyze_board([(2, 2), (3, 2), (4, 2), (14, 2), (14, 3)],
                                                 [(5, 2), (7, 2), (8, 3), (7, 4), (4, 3)])
    result = ev.is_flush(cards, pairness, suitness)
    assert result == (True, 140000+7000+500+40+3)

    cards, pairness, suitness = ev.analyze_board([(2, 2), (3, 2), (4, 4), (14, 2), (14, 3)],
                                                 [(5, 2), (7, 4), (8, 3), (7, 4), (4, 3)])
    result = ev.is_flush(cards, pairness, suitness)
    assert result == (False, 0)


def test_is_quad():
    # ev = Evaluator()
    #
    # cards, pairness, suitness = ev.analyze_board([(11, 2), (10, 3), (9, 2), (14, 3)],
    #                                              [(2, 2), (3, 2), (8, 1), (7, 2), (4, 3)])
    pass
