#-*- coding: utf-8 -*-

# imports - - - - - - -
from condition import *

#アクションはagentをとる関数 Actionクラスはインスタンスを持たない：持ったほうがいいか？
class Action():
    
    @classmethod
    def stay(cls):
        def _stay(box):
            pass

        return _stay
    
    @classmethod
    def move_horizontally(cls, amount):
        def _move_horizontally(box):
            box.add_x(amount)

        return _move_horizontally

    @classmethod
    def move_vertically(cls, amount):
        def _move_horizontally(box):
            box.add_y(amount)

        return _move_horizontally
    
    @classmethod
    def change_width(cls, amount):
        def _change_width(box):
            box.add_width(amount)

        return _change_width
    
    @classmethod
    def change_height(cls, amount):
        def _change_height(box):
            box.add_height(amount)

        return _change_height
    
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


class Rule():
    initial_weight = 5

    def __init__(self, condition=Condition(), action=Action.stay(), weight=initial_weight):
        self.condition = condition
        self.action = action
        self.weight = weight

    def set_weight(self, weight):
        self.weight = weight

    def add_weight(self, amount):
        self.set_weight(self.weight +  amount)


    @classmethod
    # take layout as argument because some actions need layout for argument
    def generate_rule_with_random_action(cls, condition, layout):
        action = Action.stay()
        return Rule(condition, action)

class SampleRule():
    def __init__(self):
        self.condition = Condition([Condition.nearby_object(60)])
        self.action = Action.stay()
        self.weight = Rule.initial_weight


# imports - - - - - - -
