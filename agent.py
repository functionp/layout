#-*- coding: utf-8 -*-

import math

class Agent():

    max_rules = 5

    def __init__(self):
        self.ruleset = []

    # return sorted ruleset according to its strength
    def get_sorted_ruleset(self):
        pairs = [(rule.strength, rule) for rule in self.ruleset]
        pairs.sort()
        pairs.reverse()
        sorted_ruleset = [pair[1] for pair in pairs]

        return sorted_ruleset

    def get_number_of_rules(self):
        return len(self.ruleset)

    def add_rule(self, rule):
        if Agent.max_rules <= self.get_number_of_rules():
            self.replace_weakest_rule(rule)
        else:
            self.ruleset.append(rule)

    def add_rule_with_random_action(self, agent_set):
        pass

    def delete_weak_rules(self):
        border_strength = 0.01

        for rule in self.ruleset:
            if rule.strength < border_strength:
                self.delete_rule(rule)

    def delete_rule(self, rule):
        self.ruleset.remove(rule)

    def find_matching_rule_and_apply(self, agent_set):
        pass

    # let this agent take given action
    def execute_action(self, action):
        action(self)

    def get_index_of_weakest_rule(self):
        weakest_value = 1000

        for i,rule in enumerate(self.ruleset):
            if rule.strength < weakest_value:
                weakest_value = rule.strength
                index_weakest = i

        return index_weakest

    # change weakest rule of agent into given rule (DESTRUCTIVE)
    def replace_weakest_rule(self, rule):
        i = self.get_index_of_weakest_rule()
        self.ruleset[i] = rule

    def rule_select(self):
        def _greedy(agent):
            sorted_ruleset = agent.get_sorted_ruleset()
            return sorted_ruleset[0]

        return _greedy(self)

    @classmethod
    # exchange two rules of randomly chosen two agents (DESTRUCTIVE)
    def exchange_rule_randomly(cls, agents):
        BORDER = 3

        if len(agents) != 0:
            i1 = random.randint(0,len(agents)-1)
            i2 = random.randint(0,len(agents)-1)
        else: 
            i1 = 0
            i2 = 0

        sending_rule1 = agents[i1].get_sorted_ruleset()[0]
        sending_rule2 = agents[i2].get_sorted_ruleset()[0]

        agents[i1].replace_weakest_rule(sending_rule2)
        agents[i2].replace_weakest_rule(sending_rule1)

def length_of_vector(vector):
    return math.sqrt(vector[0] ** 2 + vector[1] ** 2)

class BoxAgent(Agent):
    def __init__(self, position=[0,0], size=[10,10]):
        Agent.__init__(self)
        self.position = position
        self.size = size

    def render(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY, pos=self.position, size=self.size, style=wx.SIMPLE_BORDER)
        panel.SetBackgroundColour("#ffffff")

    #add rule which has present condition and random action
    def add_rule_with_random_action(self, layout):
        situation = Situation(layout, self)
        condition = Condition.make_condition(situation)

        if condition.condfuns != []:
            new_rule = BoxRule.generate_rule_with_random_action(condition, layout)
            self.add_rule(new_rule)
            return True

        # if no condition can be represents current situation, add no rule
        else:
            return False

    # find (the strongest) rule which matches current condition(layout and box) and return it. return None if no rule is found.
    def get_matching_rule(self, layout):
        self.ruleset = self.get_sorted_ruleset()
        matching_rule = None
        current_situation = Situation(layout, self)

        for rule in self.ruleset:
            if rule.condition.evaluate(current_situation):
                matching_rule = rule
                break

        return matching_rule

    def get_right_position(self, margin):
        present_x, present_y = self.position
        return [present_x + self.size[0] + margin, present_y]

    def get_bottom_position(self, margin):
        present_x, present_y = self.position
        return [present_x, present_y + self.size[1] + margin]

    def add_x(self, amount):

        x_after_movement = (self.position[0] + amount)

        if x_after_movement <= 0:
            self.position[0] = 0
        elif WINDOW_SIZE[0] <x_after_movement + self.size[0]:
            self.position[0] = WINDOW_SIZE[0] - self.size[0]
        else:
            self.position[0] = x_after_movement

    def add_y(self, amount):

        y_after_movement = (self.position[1] + amount)

        if y_after_movement <= 0:
            self.position[1] = 0
        elif WINDOW_SIZE[1] < y_after_movement + self.size[1]:
            self.position[1] = WINDOW_SIZE[1] - self.size[1]
        else:
            self.position[1] = y_after_movement

    def add_vector(self, vector):
        self.add_x(vector[0])
        self.add_y(vector[1])

    def add_width(self, amount):
        self.size[0] = self.size[0] + amount

    def add_height(self, amount):
        self.size[1] = self.size[1] + amount

    def align_left(self, target_box):
        self.position[0] = target_box.position[0]

    def align_top(self, target_box):
        self.position[1] = target_box.position[1]

    def get_nearest_box(self, layout):

        pairs = [(get_distance_between_gravities(self, box), box)  for box in layout.agents]
        pairs.sort()

        # take 1st box as nearest box because 0th box is box itself
        nearest_box = pairs[1][1]

        return nearest_box

    # get difference(signed distance) of gravity
    def get_gravity_difference(self, target_box):
        self_gravity = self.get_gravity_position()
        target_gravity = target_box.get_gravity_position()

        gravity_difference_x = self_gravity[0] - target_gravity[0]
        gravity_difference_y = self_gravity[1] - target_gravity[1]

        return [gravity_difference_x, gravity_difference_y]

    # stay away from target, or approach to target
    def change_distance(self, target_box, amount):
        gravity_difference = self.get_gravity_difference(target_box)
        gravity_distance = length_of_vector(gravity_difference)

        if gravity_distance != 0:
            vector_to_move = [amount * (gravity_difference[0] / gravity_distance), amount * (gravity_difference[1] / gravity_distance)]
            self.add_vector(vector_to_move)

    def stay_away(self, target_box, amount=None):

        # set default amount
        if amount == None:
            gravity_difference = self.get_gravity_difference(target_box)
            gravity_distance = length_of_vector(gravity_difference)

            basic_distance_vector = BoxAgent.get_basic_distance_vector(self, target_box)
            basic_distance = length_of_vector(basic_distance_vector)

            if gravity_distance != 0:
                # the closer two boxes are, the further they move
                amount =  basic_distance ** 2 / gravity_distance
            else:
                amount = 0

        self.change_distance(target_box, amount)

    def approach(self, target_box, amount=None):
        gravity_difference = self.get_gravity_difference(target_box)
        gravity_distance = length_of_vector(gravity_difference)

        #set default amount
        if amount == None:
            amount = gravity_distance / 2

        # do not approach if boxes are already close enough
        if gravity_distance > amount:
            self.change_distance(target_box, -amount)

    # get the position of center of gravity
    def get_gravity_position(self):
        gravity_x = self.position[0] + self.size[0] / 2
        gravity_y = self.position[1] + self.size[1] / 2

        return [gravity_x, gravity_y]

    def off_the_edge_or_not(self):
        off_right_or_bottom = (self.position[0] + self.size[0]) > WINDOW_SIZE[0] or (self.position[1] + self.size[1]) > WINDOW_SIZE[1]
        off_left_or_top = self.position[0] < 0 or self.position[1] < 0

        if off_right_or_bottom or off_left_or_top:
            return True
        else:
            return False

    @classmethod
    def overlap_or_not(cls, box1, box2):
        difference_x = abs(box1.position[0] - box2.position[0])
        difference_y = abs(box1.position[1] - box2.position[1])
        if difference_x < box1.size[0] and difference_x < box2.size[0] and difference_y < box1.size[1] and difference_y < box2.size[1]:
            return True
        else:
            return False

    @classmethod
    def get_basic_distance_vector(cls, box1, box2):
        basic_distance_x = (box1.size[0] + box2.size[0]) /2
        basic_distance_y = (box1.size[1] + box2.size[1]) /2
        return [basic_distance_x, basic_distance_y]


# imports - - - - - - -
import wx
import random
from main import WINDOW_SIZE
from condition import *
from rule import *
