#-*- coding: utf-8 -*-

# imports - - - - - - -
from condition import *
import random

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
    def unify_width_to_nearest_box(cls, layout):

        def _unify_width_to_nearest_box(box):
            nearest_box = box.get_nearest_box(layout)
            box.set_width(nearest_box.get_width())

        return _unify_width_to_nearest_box

    @classmethod
    def unify_height_to_nearest_box(cls, layout):

        def _unify_height_to_nearest_box(box):
            nearest_box = box.get_nearest_box(layout)
            box.set_height(nearest_box.get_height())

        return _unify_height_to_nearest_box

    @classmethod
    def unify_size_to_most_aligned_box(cls, layout):

        def _unify_size_to_most_aligned_box(box):
            most_aligned_box = box.get_most_aligned_box(layout)
            x_difference = box.get_position_difference(most_aligned_box, 0)
            y_difference = box.get_position_difference(most_aligned_box, 1)
 
            if x_difference < y_difference:
                box.unify_width_and_align(most_aligned_box)
            else:
                box.unify_height_and_align(most_aligned_box)

        return _unify_size_to_most_aligned_box

    @classmethod
    def align_to_nearest_box(cls, layout, compare=(lambda x1, x2: x1 < x2)):

        def _align_to_nearest_box(box):
            nearest_box = box.get_nearest_box(layout)

            difference_x = abs(box.get_x() - nearest_box.get_x())
            difference_y = abs(box.get_y() - nearest_box.get_y())

            if compare(difference_x , difference_y):
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

    @classmethod
    def stay_away_to_nearest_box(cls, layout):

        def _stay_away_to_nearest_box(box):
            nearest_box = box.get_nearest_box(layout)
            box.stay_away(nearest_box)

        return _stay_away_to_nearest_box

    @classmethod
    def approach_to_nearest_box(cls, layout):

        def _approach_to_nearest_box(box):
            nearest_box = box.get_nearest_box(layout)
            box.approach(nearest_box)

        return _approach_to_nearest_box

    @classmethod
    def space_nearest_box(cls, amount, layout,compare=(lambda x1, x2: x1 < x2)):
        """Set space with the nearest box designated value"""

        def _space_nearest_box(box):
            nearest_box = box.get_nearest_box(layout)
            x_difference = box.get_position_difference(nearest_box, 0)
            y_difference = box.get_position_difference(nearest_box, 1)
 
            if compare(x_difference, y_difference):
                box.make_vertical_space(nearest_box, amount)
            else:
                box.make_horizontal_space(nearest_box, amount)

        return _space_nearest_box

    @classmethod
    def space_most_aligned_box(cls, amount, layout, compare=(lambda x1, x2: x1 < x2)):
        """Set space with the most aligned box designated value"""

        def _space_most_aligned_box(box):
            most_aligned_box = box.get_most_aligned_box(layout)
            x_difference = box.get_position_difference(most_aligned_box, 0)
            y_difference = box.get_position_difference(most_aligned_box, 1)
 
            if compare(x_difference,  y_difference):
                box.make_vertical_space(most_aligned_box, amount)
            else:
                box.make_horizontal_space(most_aligned_box, amount)

        return _space_most_aligned_box

class Rule():
    initial_strength = 0.5

    def __init__(self, condition=Condition(), action=BoxAction.stay(), strength=initial_strength):
        self.condition = condition
        self.action = action
        self.strength = strength

    def set_strength(self, strength):

        if 1.0 <= strength:
            strength = 1.0
        elif strength <= 0:
            strength = 0

        self.strength = strength

    def add_strength(self, amount):
        self.set_strength(self.strength +  amount)

    def get_copy(self):
        return Rule(self.condition.get_copy(), self.action, self.strength)

    def reinforce(self, episode, reward_function):
        """Increase(decrease) strength."""

        self.set_strength(self.strength + reward_function(episode))

    @classmethod
    #take layout as argument because some actions need layout for argument
    def generate_rule_with_random_action(cls, condition, agent_set):
        pass

class BoxRule(Rule):
    @classmethod
    # take elayout as argument because some actions need layout for argument
    def generate_rule_with_random_action(cls, condition, layout):
        action_candidates = [BoxAction.stay(),
                             BoxAction.move_horizontally(10),
                             BoxAction.move_vertically(10),
                             BoxAction.move_horizontally(-10),
                             BoxAction.move_vertically(-10),
                             BoxAction.change_width(10),
                             BoxAction.change_width(-10),
                             BoxAction.change_height(10),
                             BoxAction.change_height(-10),
                             BoxAction.align_to_nearest_box(layout, (lambda x1, x2: x1 < x2)),
                             BoxAction.align_to_nearest_box(layout, (lambda x1, x2: x1 > x2)),
                             BoxAction.space_nearest_box(20, layout, (lambda x1, x2: x1 < x2)),
                             BoxAction.space_nearest_box(20, layout, (lambda x1, x2: x1 < x2)),
                             BoxAction.space_nearest_box(20, layout, (lambda x1, x2: x1 > x2)),
                             BoxAction.space_most_aligned_box(20, layout, (lambda x1, x2: x1 < x2)),
                             BoxAction.space_most_aligned_box(20, layout, (lambda x1, x2: x1 < x2)),
                             BoxAction.space_most_aligned_box(20, layout, (lambda x1, x2: x1 > x2)),
                             BoxAction.unify_size_to_most_aligned_box(layout)]

        action = random.choice(action_candidates)
        return Rule(condition, action)


class SampleRule():
    def __init__(self):
        self.condition = Condition([Condition.nearby_object(60)])
        self.action = BoxAction.stay()
        self.strength = Rule.initial_strength


# imports - - - - - - -
