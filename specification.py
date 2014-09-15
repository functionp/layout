#-*- coding: utf-8 -*-

class Specification():
    def __init__(self, constraint, objective):
        self.constraint = constraint
        self.objective = objective

    def get_default_layout(self):
        return SampleLayout()

    @staticmethod
    def load_specification(file_path):
        something = ''
        #return Specification(constraint, objective)
        return Specification(SampleConstraint(), SampleObjective())

class Objective():
    def __init__(self, max_min, function):
        self.max_min = max_min
        self.function = function

class SampleObjective(Objective):
    def __init__(self):

        def sum_of_distance_between_gravities(layout):

            boxes = layout.boxes
            distance_list = [[get_distance_between_gravities(boxes[i], boxes[j]) for j in range(i, len(boxes))] for i in range(len(boxes))]

            # return sum of distances
            return reduce((lambda x,y: x+y), reduce((lambda x,y: x+y), distance_list))

        Objective.__init__(self, 1, sum_of_distance_between_gravities)

def get_distance_between_gravities(box1, box2):
    return math.sqrt((box1.get_gravity_position()[0] - box2.get_gravity_position()[0]) ** 2 + (box1.get_gravity_position()[1] - box2.get_gravity_position()[1]) ** 2)

# imports - - - - - - -
from layout import *
from agent import *
from condition import *
import math
