import pytest

from game.model import Model


def test_create_deck():
    m = Model()
    assert len(m.data["deck"]) == 0
    deck = m.create_deck()
    assert len(deck) == 52


def test_is_busted():
    m = Model()
    assert m.is_busted(1) is False
    assert m.is_busted(10) is False
    assert m.is_busted(21) is False
    assert m.is_busted(22) is True


def test_deal():
    m = Model()
    data = m.deal()
    assert len(data["deck"]) == 49
    assert len(data["player_cards"]) == 2
    assert len(data["dealer_cards"]) == 1
