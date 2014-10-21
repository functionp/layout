#-*- coding: utf-8 -*-

# imports - - - - - - -
from condition import *
import random

#アクションはagentをとる関数 Actionクラスはインスタンスを持たない：持ったほうがいいか？
class Action():
    pass

class BoxAction(Action):
    @classmethod
    def stay(cls):
        def _stay(box):
            pass

        return _stay

    @classmethod
    def move_horizontally(cls, amount_to_move):
        def _move_horizontally(box):
            box.add_x(amount_to_move)

        return _move_horizontally

    @classmethod
    def move_horizontally_at_random(cls, max_amount):
        def _move_horizontally_at_random(box):
            amount_to_move = random.randint(-max_amount, max_amount)
            box.add_x(amount_to_move)

        return _move_horizontally_at_random

    @classmethod
    def move_vertically(cls, amount_to_move):
        def _move_vertically(box):
            box.add_y(amount_to_move)

        return _move_vertically

    @classmethod
    def move_vertically_at_random(cls, max_amount):
        def _move_vertically_at_random(box):
            amount_to_move = random.randint(-max_amount, max_amount)
            box.add_y(amount_to_move)

        return _move_vertically_at_random

    @classmethod
    def change_width(cls, amount):
        def _change_width(box):
            box.add_width(amount)

        return _change_width

    @classmethod
    def change_width_at_random(cls, max_amount):
        def _change_width_at_random(box):
            amount_to_change = random.randint(-max_amount, max_amount)
            box.add_width(amount_to_change)

        return _change_width_at_random

    @classmethod
    def change_height(cls, amount):
        def _change_height(box):
            box.add_height(amount)

        return _change_height

    @classmethod

    def change_height_at_random(cls, max_amount):
        def _change_height_at_random(box):
            amount_to_change = random.randint(-max_amount, max_amount)
            box.add_height(amount_to_change)

        return _change_height_at_random

    @classmethod
    def align_to_nearest_box(cls, layout):

        def _align_to_nearest_box(box):
            nearest_box = box.get_nearest_box(layout)

            difference_x = abs(box.position[0] - nearest_box.position[0])
            difference_y = abs(box.position[1] - nearest_box.position[1])

            if difference_x < difference_y:
                box.align_left(nearest_box)
            else:
                box.align_top(nearest_box)

        return _align_to_nearest_box

    @classmethod
    def align_top_to_nearest_box(cls, layout):

        def _align_top_to_nearest_box(box):
            nearest_box = box.get_nearest_box(layout)
            box.align_top(nearest_box)

        return _align_top_to_nearest_box

    @classmethod
    def align_left_to_nearest_box(cls, layout):

        def _align_left_to_nearest_box(box):
            nearest_box = box.get_nearest_box(layout)
            box.align_left(nearest_box)

        return _align_left_to_nearest_box
 

class Rule():
    initial_strength = 0.5

    def __init__(self, condition=Condition(), action=BoxAction.stay(), strength=initial_strength):
        self.condition = condition
        self.action = action
        self.strength = strength

    def set_strength(self, strength):
        self.strength = strength

    def add_strength(self, amount):
        self.set_strength(self.strength +  amount)

    # increase(decrease) strength
    def reinforce(self, episode, reward_function):
        self.strength = self.strength + reward_function(episode)

        if 1.0 <= self.strength:
            self.strength = 1.0
        elif self.strength <= 0:
            self.strength = 0


    @classmethod
    # take layout as argument because some actions need layout for argument
    def generate_rule_with_random_action(cls, condition, agent_set):
        pass

class BoxRule(Rule):
    @classmethod
    # take layout as argument because some actions need layout for argument
    def generate_rule_with_random_action(cls, condition, layout):
        action_candidates = [BoxAction.stay(), BoxAction.move_vertically_at_random(30), BoxAction.move_horizontally_at_random(30), BoxAction.change_width_at_random(30), BoxAction.change_height_at_random(30), BoxAction.align_to_nearest_box(layout), BoxAction.align_top_to_nearest_box(layout), BoxAction.align_left_to_nearest_box(layout)]
        action = random.choice(action_candidates)
        return Rule(condition, action)


class SampleRule():
    def __init__(self):
        self.condition = Condition([Condition.nearby_object(60)])
        self.action = BoxAction.stay()
        self.strength = Rule.initial_strength


# imports - - - - - - -
