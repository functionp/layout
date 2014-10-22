#-*- coding: utf-8 -*-

#制約条件も目的関数に取り込む方針で　カプセル化の意味でSpecificationは消さない
class Specification():
    def __init__(self, objective):
        self.objective = objective

    def get_default_layout(self):
        return SampleLayout()

    @staticmethod
    def load_specification(file_path):
        something = ''
        #return Specification(constraint, objective)
        return Specification(SampleObjective())

class Objective():
    def __init__(self, max_min, function):
        self.max_min = max_min
        self.function = function

class SampleObjective(Objective):
    def __init__(self):

        def sum_of_distance_between_gravities(layout):

            boxes = layout.agents
            distance_list = [[get_distance_between_gravities(boxes[i], boxes[j]) for j in range(i, len(boxes))] for i in range(len(boxes))]

            # return sum of distances
            return reduce((lambda x,y: x+y), reduce((lambda x,y: x+y), distance_list))

        def penalize_overlap(layout):
            boxes = layout.agents
            penalty = 0

            for i, box1 in enumerate(boxes):
                for j in range(i+1,len(boxes) - 1):
                    if BoxAgent.overlap_or_not(boxes[i], boxes[j]):
                        penalty += 1

            # return sum of distances
            return penalty * 0

        objective_function = (lambda layout: sum_of_distance_between_gravities(layout) + penalize_overlap(layout))

        Objective.__init__(self, 1, objective_function)

def get_distance_between_gravities(box1, box2):
    return math.sqrt((box1.get_gravity_position()[0] - box2.get_gravity_position()[0]) ** 2 + (box1.get_gravity_position()[1] - box2.get_gravity_position()[1]) ** 2)

# imports - - - - - - -
from layout import *
from agent import *
from condition import *
from rule import *
import math
