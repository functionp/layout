#-*- coding: utf-8 -*-

import unittest
from agent import *
from rule import *
from condition import *
from optimization import *
from condition import *

class TestAgent(unittest.TestCase):

    def setUp(self):
        pass

    def test_align_left(self):
        box1 = BoxAgent([50, 100], [30, 30])
        box2 = BoxAgent([60, 200], [30, 30])

        box2.align_left(box1)
        self.assertEqual(box2.position[0], 50)

    def test_overlap_or_not(self):
        box1 = BoxAgent([50, 50], [30, 30])
        box2 = BoxAgent([70, 70], [30, 30])

        self.assertTrue(BoxAgent.overlap_or_not(box1, box2))


    def test_evaluating_condition(self):
        box1 = BoxAgent()

        rule1 = Rule()
        rule2 = Rule()
        rule3 = Rule()

        rule2.add_weight(3)
        rule3.add_weight(-3)

        box1.add_rule(rule1)
        box1.add_rule(rule2)
        box1.add_rule(rule3)

        self.assertEqual(box1.get_index_of_lightest_rule(), 2)


class TestLayout(unittest.TestCase):

    def setUp(self):
        pass


class TestOptimization(unittest.TestCase):

    def setUp(self):
        pass


class TestRule(unittest.TestCase):

    def setUp(self):
        pass

    def test_default_value(self):
        rule = Rule()
        self.assertTrue(rule.weight, 5)

class TestCondition(unittest.TestCase):

    def setUp(self):
        pass


    def test_evaluating_condition(self):
        box1 = BoxAgent([50, 100], [30, 30])
        box2 = BoxAgent([60, 200], [30, 30])
        box3 = BoxAgent([120, 100], [30, 30])

        layout = Layout([box1, box2, box3])
        condition = Condition.make_condition(layout=layout, box=box1)

        self.assertTrue(condition.evaluate(layout=layout, box=box1))

if __name__ == "__main__":
    unittest.main()
