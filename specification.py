#-*- coding: utf-8 -*-

from condition import *

#制約条件も目的関数に取り込む方針で　カプセル化の意味でSpecificationは消さない
class Specification():
    def __init__(self, default_layout, objective, constraints=Condition()):
        self.default_layout = default_layout
        self.objective = objective
        self.constraints = constraints

    @staticmethod
    def load_specification(file_path):
        pass
        #something = ''
        #return Specification(constraint, objective)
        #return SoftplannerSpecification()

class SoftplannerSpecification(Specification):
    def __init__(self):
        default_layout = SoftplannerLayout()
        objective = OverlappedAreaObjective()
        constraint = Condition([BoxCondition.no_overlap(), BoxCondition.all_aligned()], 1)

        Specification.__init__(self, default_layout, objective, constraint)

class SampleSpecification(Specification):
    def __init__(self):
        default_layout = SampleLayout()
        objective = OverlappedAreaObjective()
        constraint = Condition([BoxCondition.no_overlap(), BoxCondition.all_aligned()], 1)

        Specification.__init__(self, default_layout, objective, constraint)

class Objective():
    def __init__(self, max_min, function):
        self.max_min = max_min
        self.function = function

    @staticmethod
    def sum_of_overlapped_area(layout):

        boxes = layout.agents

        if len(boxes) > 1:
            overlapped_area_list = [[BoxAgent.get_overlaped_area(boxes[i], boxes[j]) for j in range(i, len(boxes)) if i != j] for i in range(len(boxes))]
        else:
            overlapped_area_list = [[0]]

        # return sum of distances
        return reduce((lambda x,y: x+y), reduce((lambda x,y: x+y), overlapped_area_list))

    @staticmethod
    def sum_of_distance_between_gravities(layout):

        boxes = layout.agents
        distance_list = [[BoxAgent.get_gravity_distance(boxes[i], boxes[j]) for j in range(i, len(boxes))] for i in range(len(boxes))]

        # return sum of distances
        return reduce((lambda x,y: x+y), reduce((lambda x,y: x+y), distance_list))

    @staticmethod
    def penalize_overlap(layout):
        boxes = layout.agents
        penalty = 0

        for i, box1 in enumerate(boxes):
            for j in range(i+1,len(boxes) - 1):
                if BoxAgent.overlap_or_not(boxes[i], boxes[j]):
                    penalty += 1

        # return sum of distances
        return penalty * 1000


class OverlappedAreaObjective(Objective):
    def __init__(self):

        #汎用性が低いのでクラスメソッドにはしない
        def width_difference(layout):

            boxes = layout.agents
            side_box = layout.get_agent_with_identifier("side")
            content_box = layout.get_agent_with_identifier("content")

            # return sum of distances
            return abs(side_box.get_width() - content_box.get_width()) * 10

        objective_function = (lambda layout: Objective.sum_of_overlapped_area(layout) + width_difference(layout))

        Objective.__init__(self, 1, objective_function)


class DistanceObjective(Objective):
    def __init__(self):

        objective_function = (lambda layout: Objective.sum_of_distance_between_gravities(layout) + Objective.penalize_overlap(layout))

        Objective.__init__(self, 1, objective_function)

# imports - - - - - - -
from layout import *
from agent import *
from rule import *
import math

from compiler.node import *
