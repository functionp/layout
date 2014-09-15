#-*- coding: utf-8 -*-

class Condition():
    # we call function which reperesents one condition  as "condfun"
    def __init__(self, condfuns=[], and_or=1):
        self.condfuns = condfuns
        self.and_or = and_or

    # evaluate the condition and return True or False
    def evaluate(self, **kwargs):
        results = [condfun(**kwargs) for condfun in self.condfuns]

        # case of "and"
        if self.and_or == 1:
            return reduce(lambda b1,b2: b1 and b2, results)
        else:
            return reduce(lambda b1,b2: b1 or b2, results)

    def add_condfun(self, condfun):
        self.condfuns.append(condfun)

    @classmethod
    def minimum_member(cls, number):
        def _minimum_member(**kwargs):
            layout = kwargs['layout']

            if layout.get_number_of_boxes() >= number:
                return True
            else:
                return False

        return _minimum_member

    @classmethod
    def in_the_edge(cls):
        def _in_the_edge(**kwargs):
            layout = kwargs['layout']

            result = True
            for box in layout.boxes:
                if box.off_the_edge_or_not() == True:
                    result = False
                    break

            return result

        return _in_the_edge

    @classmethod
    def no_overlap(cls):
        def _no_overlap(**kwargs):
            layout = kwargs['layout']

            boxes = layout.boxes
            result = True
            for i in range(len(boxes)):
                for j in range(i+1, len(boxes)):
                    if BoxAgent.overlap_or_not(boxes[i], boxes[j]) == True:
                        result = False
                        break

            return result

        return _no_overlap

    @classmethod
    def nearby_object(cls, distance):
        def _no_overlap(**kwargs):
            layout = kwargs['layout']
            box = kwargs['box']

            boxes = layout.boxes
            result = True
            for i in range(len(boxes)):
                for j in range(i+1, len(boxes)):
                    if BoxAgent.overlap_or_not(boxes[i], boxes[j]) == True:
                        result = False
                        break

            return result

        return _no_overlap

#必要なければ制約ConstraintはConditionだけにしてもいいかも
class Constraint():
    def __init__(self, condition):
        self.condition = condition

class SampleConstraint(Constraint):
    def __init__(self):
        condition = Condition()
        condition.add_condfun(Condition.minimum_member(2))
        condition.add_condfun(Condition.in_the_edge())
        condition.add_condfun(Condition.no_overlap())

        Constraint.__init__(self, condition)


class Rule():
    initial_weight = 5
    def __init__(self, conditions, action, weight):
        self.condition = Condition()
        self.action = ''
        self.weight = Rule.initial_weight

    @classmethod
    def make_rule_with_random_action(cls, condition):
        action = ''
        weight = Rule.initial_weight
        return Rule(condition, action, weight)

class SampleRule():
    def __init__(self):
        self.condition = Condition([Condition.nearby_object(60)])
        self.action = Action.stay()
        self.weight = Rule.initial_weight

#アクションはagentをとる関数
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

# imports - - - - - - -
from layout import *
from agent import *
from specification import *
