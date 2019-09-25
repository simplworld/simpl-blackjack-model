import pytest
from test_plus.test import TestCase

from game.model import Model


class ModelTestCase(TestCase):
    def setUp(self):
        self.m = Model()

    def test_create(self):
        m = Model()
        self.assertNotEqual(m, None)

    def test_first_step(self):
        m = Model()
        total = m.step(5)
        self.assertEquals(total, 5)

    def test_increase_step(self):
        m = Model()
        total = m.step(5, 3)
        self.assertEquals(total, 8)

    def test_decrease_step(self):
        m = Model()
        total = m.step(5, -2.5)
        self.assertEquals(total, 2.5)
