#-*- coding: utf-8 -*-

class Situation():
    def __init__(self, layout, box):
        self.layout = layout
        self.box = box

# return True if relation between given box and any box in given layout satisfies the given bool function
def bool_for_layout_and_box(layout, box, bool_function):

    boxes = layout.boxes[:]

    #ignore exception
    try:
        boxes.remove(box)
    except:
        pass

    result = False
    for i in range(len(boxes)):
        if bool_function(box, boxes[i]) == True:
            result = True
            break

    return result

class Condition():
    # we call function which reperesents one condition  as "condfun"
    def __init__(self, condfuns=[], and_or=1):
        self.condfuns = condfuns
        self.and_or = and_or

    # evaluate the condition with given situation and return True or False
    def evaluate(self, situation):
        results = [condfun(situation) for condfun in self.condfuns]

        # case of "and"
        if self.and_or == 1:
            return reduce(lambda b1,b2: b1 and b2, results)
        else:
            return reduce(lambda b1,b2: b1 or b2, results)

    def get_size(self):
        return len(self.condfuns)

    def add_condfun(self, condfun):
        self.condfuns.append(condfun)

    def remove_random_condfun(self):
        index = random.randint(0, len(self.condfuns) - 1)
        remove_condfun(index)

    def remove_condfun(self, index):
        del(self.condfuns[index])


    @classmethod
    # make Condition instance which represents given situation(layout and box)
    def make_condition(cls, situation):
        condfun_candidates = [Condition.in_the_edge() , Condition.having_box_in_given_distance(100), Condition.having_overlapped_box()]

        # extract which matches given state(layout and box)
        matched_condfuns = [condfun for condfun in condfun_candidates if condfun(situation) == True]

        and_or = 1 # represents "and"
        condition = Condition(matched_condfuns, and_or)

        # remove if condition has a lot of condfuns (loosing condition)
        if 3 < condition.get_size():
            condition.remove_random_condfun()

        return condition

    # # # CONDFUNS # # #

    @classmethod
    def minimum_member(cls, number):
        def _minimum_member(situation):
            layout = situation.layout

            if layout.get_number_of_boxes() >= number:
                return True
            else:
                return False

        return _minimum_member

    @classmethod
    def in_the_edge(cls):
        def _in_the_edge(situation):
            layout = situation.layout

            result = True
            for box in layout.boxes:
                if box.off_the_edge_or_not() == True:
                    result = False
                    break

            return result

        return _in_the_edge

    @classmethod
    def no_overlap(cls):
        def _no_overlap(situation):
            layout = situation.layout

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
    def having_box_in_given_distance(cls, distance):
        def _having_box_in_given_distance(situation):
            layout = situation.layout
            box = situation.box

            bool_function = (lambda box1, box2: get_distance_between_gravities(box1, box2) < distance)

            return bool_for_layout_and_box(layout, box, bool_function)

        return _having_box_in_given_distance

    @classmethod
    def having_overlapped_box(cls):
        def _having_overlapped_box(situation):
            layout = situation.layout
            box = situation.box

            bool_function = BoxAgent.overlap_or_not

            return bool_for_layout_and_box(layout, box, bool_function)

        return _having_overlapped_box

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

# imports - - - - - - -
from layout import *
from rule import *
from agent import *
from specification import *
import random
