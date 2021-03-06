#-*- coding: utf-8 -*-

import unittest
from agent import *
from rule import *
from condition import *
from optimization import *
from specification import *

class TestAgent(unittest.TestCase):

    def setUp(self):
        pass

    def test_align_left(self):
        box1 = BoxAgent(Style([50, 100], [30, 30]))
        box2 = BoxAgent(Style([60, 200], [30, 30]))

        Layout([box1, box2])

        box2.align_left(box1)
        self.assertEqual(box2.get_x(), 50)

    def test_overlap_or_not(self):
        box1 = BoxAgent(Style([50, 50], [30, 30]))
        box2 = BoxAgent(Style([70, 70], [30, 30]))

        self.assertTrue(BoxAgent.overlap_or_not(box1, box2))

        box3 = BoxAgent(Style([50, 50], [30, 30]))
        box4 = BoxAgent(Style([90, 90], [50, 50]))

        self.assertFalse(BoxAgent.overlap_or_not(box3, box4))

        box5 = BoxAgent(Style([50, 50], [100, 100]))
        box6 = BoxAgent(Style([60, 60], [20, 20]))

        self.assertTrue(BoxAgent.overlap_or_not(box5, box6))

    def test_evaluating_condition(self):
        box1 = BoxAgent(Style())

        rule1 = Rule()
        rule2 = Rule()
        rule3 = Rule()

        rule2.add_strength(3)
        rule3.add_strength(-3)

        box1.add_rule(rule1)
        box1.add_rule(rule2)
        box1.add_rule(rule3)

        self.assertEqual(box1.get_index_of_weakest_rule(), 2)

    def test_overlapped_area(self):
        box1 = BoxAgent(Style([100, 100], [200, 200]))
        box2 = BoxAgent(Style([320, 321], [100, 200]))

        self.assertEqual(BoxAgent.get_overlaped_area(box1, box2), 0)


    def test_set_size(self):
        base_box = BoxAgent(Style([100, 100], [400, 400]))
        box1 = BoxAgent(Style([150, 150], [100, 100]))

        layout = Layout([box1], base_box)
        box1.set_width(400)

        self.assertEqual(box1.get_width(), 400)


class TestLayout(unittest.TestCase):

    def setUp(self):
        pass

    def test_rulesets(self):
        box1 = BoxAgent(Style([50, 100], [30, 30]))
        box2 = BoxAgent(Style([60, 200], [30, 30]))
        box3 = BoxAgent(Style([120, 100], [30, 30]))

        layout = Layout([box1, box2, box3])

        box1.add_rule_with_random_action(layout)
        box1.add_rule_with_random_action(layout)
        box2.add_rule_with_random_action(layout)
        box2.add_rule_with_random_action(layout)
        box3.add_rule_with_random_action(layout)
        box3.add_rule_with_random_action(layout)

        rulesets = layout.get_rulesets()

        self.assertEqual(box2.ruleset[1], rulesets[1][1])

    def test_generating_rule(self):
        box1 = BoxAgent(Style([50, 100], [30, 30]))
        box2 = BoxAgent(Style([60, 200], [30, 30]))
        box3 = BoxAgent(Style([120, 100], [30, 30]))

        layout = Layout([box1, box2, box3])

        layout.generate_rules()
        matching_rule = box2.get_matching_rule(layout)

        self.assertNotEqual(matching_rule, None)


    def test_generating_rule(self):
        box1 = BoxAgent(Style([50, 100], [30, 30]))
        box2 = BoxAgent(Style([50, 200], [30, 30]))
        box3 = BoxAgent(Style([150, 100], [30, 30]))
        box3 = BoxAgent(Style([320, 200], [30, 30]))

        layout = Layout([box1, box2, box3])
        situation = Situation(agent_set=layout)

        alignment_distance = Objective.sum_of_alignment_distance(situation)
        self.assertEqual(alignment_distance, 0)


class TestOptimization(unittest.TestCase):

    def setUp(self):
        pass

class TestRule(unittest.TestCase):

    def setUp(self):
        pass

    def test_default_value(self):
        rule = Rule(Condition(), BoxAction.stay())
        self.assertEqual(rule.strength, Rule.initial_strength)

    def test_reinforce(self):
        box1 = BoxAgent(Style([50, 100], [30, 30]))
        box2 = BoxAgent(Style([60, 200], [30, 30]))
        box3 = BoxAgent(Style([120, 100], [30, 30]))
        box4 = BoxAgent(Style([100, 30], [30, 30]))
        box5 = BoxAgent(Style([220, 200], [50, 50]))

        layout1 = Layout([box1, box2, box3])
        layout2 = Layout([box1, box4, box5])

        box1.add_rule_with_random_action(layout1)
        box1.add_rule_with_random_action(layout1)
        box1.add_rule_with_random_action(layout2)
        box1.add_rule_with_random_action(layout2)

        selected_rule = box1.rule_select()

        reward_function = (lambda x: 0.1)
        #reward_function = (lambda x: (0.5)**x)
        episode = 5

        for i in range(5):
            selected_rule.reinforce(episode, reward_function)

        self.assertTrue((selected_rule.strength - 1.0) < 0.0001)


class TestAction(unittest.TestCase):

    def setUp(self):
        pass

    def test_movement(self):
        box1 = BoxAgent(Style([100, 100], [30, 30]))

        Layout([box1])

        action1 = BoxAction.move_vertically(50)
        action2 = BoxAction.move_horizontally(50)

        action1(box1)
        action2(box1)

        self.assertEqual([150,150], box1.get_position())

    def test_alignment(self):
        box1 = BoxAgent(Style([100, 100], [30, 30]))
        box2 = BoxAgent(Style([100, 200], [30, 30]))
        box3 = BoxAgent(Style([150, 180], [30, 30]))

        layout = Layout([box1, box2, box3])

        action1 = BoxAction.align_to_nearest_box(layout)
        action1(box3)

        self.assertEqual(box2.get_y(), box3.get_y())

    def test_stay_away(self):
        box1 = BoxAgent(Style([100, 100], [150, 200]))
        box2 = BoxAgent(Style([150, 150], [300, 100]))
        box3 = BoxAgent(Style([170, 170], [50, 50]))

        layout = Layout([box1, box2])

        action1 = BoxAction.stay_away_to_nearest_box(layout)
        action1(box2)

        self.assertFalse(BoxAgent.overlap_or_not(box1,box2))

    def test_spacing(self):
        box1 = BoxAgent(Style([100, 100], [150, 100]))
        box2 = BoxAgent(Style([100, 250], [300, 100]))
        box3 = BoxAgent(Style([170, 500], [250, 150]))
        box4 = BoxAgent(Style([100, 570], [50, 50]))

        layout = Layout([box1, box2, box3, box4])

        action1 = BoxAction.space_most_aligned_box(30, layout)
        action1(box4)

        self.assertEqual(box4.get_y(), 380)

    def test_unify_size(self):
        box1 = BoxAgent(Style([100, 100], [200, 40]))
        box2 = BoxAgent(Style([100, 200], [50, 80]))
        box3 = BoxAgent(Style([120, 290], [250, 150]))

        layout = Layout([box1, box2, box3])

        action1 = BoxAction.unify_size_to_most_aligned_box(layout)
        action1(box2)

        self.assertEqual(box2.get_width(), box1.get_width())


class TestCondition(unittest.TestCase):

    def setUp(self):
        pass
        
    def test_all_aligned(self):
        box1 = BoxAgent(Style([100, 100], [40, 40]))
        box2 = BoxAgent(Style([200, 100], [30, 30]))
        box3 = BoxAgent(Style([200, 230], [50, 50]))
        box4 = BoxAgent(Style([400, 230], [50, 50]))

        layout = Layout([box1, box2, box3, box4])
        situation = Situation(agent_set=layout)

        condfun = BoxCondFun.all_aligned()

        self.assertTrue(condfun.function(situation))
        
    def test_evaluating_condition(self):
        box1 = BoxAgent(Style([50, 100], [30, 30]))
        box2 = BoxAgent(Style([60, 200], [30, 30]))
        box3 = BoxAgent(Style([120, 100], [30, 30]))

        layout = Layout([box1, box2, box3])
        situation = Situation(agent_set=layout, agent=box1)
        condition = Condition.make_condition(situation)

        self.assertTrue(condition.evaluate(situation))

    def test_having_overlapped_box(self):
        box1 = BoxAgent(Style([50, 50], [30, 30]))
        box2 = BoxAgent(Style([70, 70], [30, 30]))
        box3 = BoxAgent(Style([120, 120], [30, 30]))
        box4 = BoxAgent(Style([470, 470], [30, 30]))

        layout = Layout([box1, box2, box3, box4])
        situation = Situation(agent_set=layout, agent=box2)

        condfun = BoxCondFun.having_overlapped_box()
        self.assertTrue(condfun.function(situation))


    def test_having_box_in_given_distance(self):
        box1 = BoxAgent(Style([50, 50], [30, 30]))
        box2 = BoxAgent(Style([70, 70], [30, 30]))
        box3 = BoxAgent(Style([120, 120], [30, 30]))
        box4 = BoxAgent(Style([470, 470], [30, 30]))

        layout = Layout([box1, box2, box3, box4])
        situation = Situation(agent_set=layout, agent=box1)

        condfun = BoxCondFun.having_box_in_given_distance(30)
        self.assertTrue(condfun.function(situation))

if __name__ == "__main__":
    unittest.main()
