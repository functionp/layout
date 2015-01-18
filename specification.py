#-*- coding: utf-8 -*-

import math

class Objective():
    def __init__(self, max_min=1, function=(lambda x: 0)):
        self.max_min = max_min
        self.function = function

    @staticmethod
    def sum_of_overlapped_area(situation):

        boxes = situation.agent_set.agents

        if len(boxes) > 1:
            overlapped_area_list = [[int(math.sqrt(BoxAgent.get_overlaped_area(boxes[i], boxes[j]))) for j in range(i, len(boxes)) if i != j] for i in range(len(boxes))]
        else:
            overlapped_area_list = [[0]]

        # return sum of distances
        return reduce((lambda x,y: x+y), reduce((lambda x,y: x+y), overlapped_area_list))

    @staticmethod
    def sum_of_alignment_distance(situation):

        boxes = situation.agent_set.agents

        if len(boxes) > 1:
            alignment_distance_list = [BoxAgent.get_alignment_distance(box, box.get_most_aligned_box(situation.agent_set)) for box in boxes]
        else:
            alignment_distance_list = [0]

        # return sum of distances
        return reduce(lambda x,y: x+y, alignment_distance_list)

    @staticmethod
    def sum_of_distance_between_gravities(situation):

        boxes = situation.agent_set.agents
        distance_list = [[BoxAgent.get_gravity_distance(boxes[i], boxes[j]) for j in range(i, len(boxes))] for i in range(len(boxes))]

        # return sum of distances
        return reduce((lambda x,y: x+y), reduce((lambda x,y: x+y), distance_list))

    @staticmethod
    def penalize_overlap(situation):
        boxes = situation.agent_set.agents
        penalty = 0

        for i, box1 in enumerate(boxes):
            for j in range(i+1,len(boxes) - 1):
                if BoxAgent.overlap_or_not(boxes[i], boxes[j]):
                    penalty += 1

        # return sum of distances
        return penalty * 1000

    @staticmethod
    def width_difference(situation):

        boxes = situation.agent_set.agents
        scale = 10

        distance_list = [[abs(boxes[i].get_width() - boxes[j].get_width()) * scale for j in range(i, len(boxes))] for i in range(len(boxes))]

        # return sum of distances
        return reduce((lambda x,y: x+y), reduce((lambda x,y: x+y), distance_list))

    @staticmethod
    def height_difference(situation):

        boxes = situation.agent_set.agents
        scale = 10

        distance_list = [[abs(boxes[i].get_height() - boxes[j].get_height()) * scale for j in range(i, len(boxes))] for i in range(len(boxes))]

        # return sum of distances
        return reduce((lambda x,y: x+y), reduce((lambda x,y: x+y), distance_list))




class OverlappedAreaObjective(Objective):
    def __init__(self):

        objective_function = (lambda situation: Objective.sum_of_overlapped_area(situation) )

        Objective.__init__(self, 1, objective_function)


class DistanceObjective(Objective):
    def __init__(self):

        objective_function = (lambda layout: Objective.sum_of_distance_between_gravities(layout) + Objective.penalize_overlap(layout))

        Objective.__init__(self, 1, objective_function)

# imports - - - - - - -
from layout import *
from agent import *
from rule import *
from condition import *
import math

from compiler.node import *
