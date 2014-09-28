#-*- coding: utf-8 -*-

import unittest
from agent import *
from rule import *
from condition import *
from optimization import *

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
        rule = Rule(Condition(), Action.stay())
        self.assertTrue(rule.weight, Rule.initial_weight)



class TestAction(unittest.TestCase):

    def setUp(self):
        pass

    def test_movement(self):
        box1 = BoxAgent([100, 100], [30, 30])

        action1 = Action.move_vertically(50)
        action2 = Action.move_horizontally(50)

        action1(box1)
        action2(box1)

        self.assertEqual([150,150], box1.position)

    def test_alignment(self):
        box1 = BoxAgent([100, 100], [30, 30])
        box2 = BoxAgent([100, 200], [30, 30])
        box3 = BoxAgent([150, 180], [30, 30])

        layout = Layout([box1, box2, box3])

        action1 = Action.align_to_nearest_box(layout)
        action1(box3)

        self.assertEqual(box2.position[1], box3.position[1])


class TestCondition(unittest.TestCase):

    def setUp(self):
        pass
        
    def test_evaluating_condition(self):
        box1 = BoxAgent([50, 100], [30, 30])
        box2 = BoxAgent([60, 200], [30, 30])
        box3 = BoxAgent([120, 100], [30, 30])

        layout = Layout([box1, box2, box3])
        situation = Situation(layout, box1)
        condition = Condition.make_condition(situation)

        self.assertTrue(condition.evaluate(situation))

    def test_having_overlapped_box(self):
        box1 = BoxAgent([50, 50], [30, 30])
        box2 = BoxAgent([70, 70], [30, 30])
        box3 = BoxAgent([120, 120], [30, 30])
        box4 = BoxAgent([470, 470], [30, 30])

        layout = Layout([box1, box2, box3, box4])
        situation = Situation(layout, box2)

        condfun = Condition.having_overlapped_box()
        self.assertTrue(condfun(situation))


    def test_having_box_in_given_distance(self):
        box1 = BoxAgent([50, 50], [30, 30])
        box2 = BoxAgent([70, 70], [30, 30])
        box3 = BoxAgent([120, 120], [30, 30])
        box4 = BoxAgent([470, 470], [30, 30])

        layout = Layout([box1, box2, box3, box4])
        situation = Situation(layout, box1)

        condfun = Condition.having_box_in_given_distance(30)
        self.assertTrue(condfun(situation))

if __name__ == "__main__":
    unittest.main()
