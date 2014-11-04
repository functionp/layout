#-*- coding: utf-8 -*-

from condition import *

#制約条件も目的関数に取り込む方針で　カプセル化の意味でSpecificationは消さない
class Specification():
    def __init__(self, objective, constraints=Condition()):
        self.objective = objective
        self.constraints = constraints

    def get_default_layout(self):
        return SampleLayout()

    @staticmethod
    def load_specification(file_path):
        something = ''
        condition = Condition([BoxCondition.no_overlap()])
        #return Specification(constraint, objective)
        return Specification(SampleObjective(), condition)

class Objective():
    def __init__(self, max_min, function):
        self.max_min = max_min
        self.function = function

class SampleObjective(Objective):
    def __init__(self):

        def sum_of_distance_between_gravities(layout):

            boxes = layout.agents
            distance_list = [[BoxAgent.get_gravity_distance(boxes[i], boxes[j]) for j in range(i, len(boxes))] for i in range(len(boxes))]

            # return sum of distances
            return reduce((lambda x,y: x+y), reduce((lambda x,y: x+y), distance_list))

        #重なり数ではなく重なり面積とかにすれば改善されそう
        def penalize_overlap(layout):
            boxes = layout.agents
            penalty = 0

            for i, box1 in enumerate(boxes):
                for j in range(i+1,len(boxes) - 1):
                    if BoxAgent.overlap_or_not(boxes[i], boxes[j]):
                        penalty += 1

            # return sum of distances
            return penalty * 1000

        objective_function = (lambda layout: sum_of_distance_between_gravities(layout) + penalize_overlap(layout))

        Objective.__init__(self, 1, objective_function)


class DistanceObjective(Objective):
    def __init__(self):

        def sum_of_distance_between_gravities(layout):

            boxes = layout.agents
            distance_list = [[BoxAgent.get_gravity_distance(boxes[i], boxes[j]) for j in range(i, len(boxes))] for i in range(len(boxes))]

            # return sum of distances
            return reduce((lambda x,y: x+y), reduce((lambda x,y: x+y), distance_list))

        #重なり数ではなく重なり面積とかにすれば改善されそう
        def penalize_overlap(layout):
            boxes = layout.agents
            penalty = 0

            for i, box1 in enumerate(boxes):
                for j in range(i+1,len(boxes) - 1):
                    if BoxAgent.overlap_or_not(boxes[i], boxes[j]):
                        penalty += 1

            # return sum of distances
            return penalty * 1000

        objective_function = (lambda layout: sum_of_distance_between_gravities(layout) + penalize_overlap(layout))

        Objective.__init__(self, 1, objective_function)

# imports - - - - - - -
from layout import *
from agent import *
from rule import *
import math

from compiler.node import *
