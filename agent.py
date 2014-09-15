#-*- coding: utf-8 -*-

class Agent():

    def __init__(self):
        self.ruleset = []

    # return sorted ruleset according to its weight
    def get_sorted_ruleset(self):
        pairs = []
        for rule in self.ruleset:
            # make pair of weight value and rule
            pairs.append((rule.weight, rule)) # ruleがidenticalなオブジェクトかも→ならコピー

        pairs.sort()
        pairs.reverse()
        return [pair[1] for pair in pairs]

    def add_rule(self, rule):
        self.ruleset.append(rule)

    # let this agent take given action
    def execute_action(self, action):
        action(self)

    def get_index_of_lightest_rule(self, rule):
        lightest_value = 1000

        for i,rule in enumelate(self.ruleset):
            if rule.weight < lightest_value:
                lightest_value = rule.weight
                index_lightest = i

        return index_lightest

    # change lightest rule of agent into given rule (DESTRUCTIVE)
    def replace_lightest_rule(self, rule):
        i = self.get_index_of_lightest_rule()
        self.ruleset[i] = rule

    @classmethod
    # exchange two rules of randomly chosen two agents (DESTRUCTIVE)
    def exchange_rule_randomly(cls, agents):
        BORDER = 3
        i1 = random.randint(0,len(agents))
        i2 = random.randint(0,len(agents))

        sending_rule1 = agents[i1].get_sorted_ruleset()[0]
        sending_rule2 = agents[i2].get_sorted_ruleset()[0]

        agents[i1].replace_lightest_rule(sending_rule2)
        agents[i2].replace_lightest_rule(sending_rule1)

class BoxAgent(Agent):
    def __init__(self, position, size):
        Agent.__init__(self)
        self.position = position
        self.size = size

    def render(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY, pos=self.position, size=self.size, style=wx.SIMPLE_BORDER)
        panel.SetBackgroundColour("#ffffff")

    def get_right_position(self, margin):
        present_x, present_y = self.position
        return [present_x + self.size[0] + margin, present_y]

    def get_bottom_position(self, margin):
        present_x, present_y = self.position
        return [present_x, present_y + self.size[1] + margin]

    def add_x(self, amount):
        self.position[0] = self.position[0] + amount

    def add_y(self, amount):
        self.position[1] = self.position[1] + amount

    def add_width(self, amount):
        self.size[0] = self.size[0] + amount

    def add_height(self, amount):
        self.size[1] = self.size[1] + amount

    def align_left(self, target_box):
        self.position[0] = target_box.position[0]

    def align_top(self, target_box):
        self.position[1] = target_box.position[1]

    def get_nearest_box(self, layout):

        pairs = [(get_distance_between_gravities(self, box), box)  for box in layout.boxes]
        pairs.sort()

        # take 1st box as nearest box because 0th box is box itself
        nearest_box = pairs[1][1]

        return nearest_box 

    # get the position of center of gravity
    def get_gravity_position(self):
        gravity_x = self.position[0] + self.size[0] / 2
        gravity_y = self.position[1] + self.size[1] / 2

        return [gravity_x, gravity_y]

    def off_the_edge_or_not(self):
        off_right_or_bottom = self.position[0] + self.size[0] > WINDOW_SIZE[0] or self.position[1] + self.size[1] > WINDOW_SIZE[1]
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


# imports - - - - - - -
import wx
import random
from main import WINDOW_SIZE
from condition import *
