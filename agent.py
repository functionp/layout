#-*- coding: utf-8 -*-

import math

class Agent():

    max_rules = 5

    def __init__(self, condition, identifier=""):
        self.set_ruleset([])
        self.condition = condition
        self.identifier = identifier

    def set_ruleset(self, ruleset):
        self.ruleset = ruleset

    def get_copy_of_ruleset(self):
        return self.ruleset[:]

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

        index_weakest = None
        for i,rule in enumerate(self.ruleset):
            if rule.strength < weakest_value:
                weakest_value = rule.strength
                index_weakest = i

        return index_weakest

    # change weakest rule of agent into given rule (DESTRUCTIVE)
    def replace_weakest_rule(self, rule):
        i = self.get_index_of_weakest_rule()
        new_rule = rule.get_copy()
        #new_rule.set_strength(Rule.initial_strength)

        if i != None:
            self.ruleset[i] = new_rule

        # if this agent has no rule, newly add the rule
        else:
            self.add_rule(new_rule)

    def rule_select(self):
        def _greedy(agent):
            sorted_ruleset = agent.get_sorted_ruleset()
            return sorted_ruleset[0]

        return _greedy(self)

    @classmethod
    # exchange two rules of randomly chosen two agents (DESTRUCTIVE)
    def exchange_rule_randomly(cls, agents):
        BORDER = 3

        i1 = random.randint(0,len(agents)-1)
        i2 = random.randint(0,len(agents)-1)

        if agents[i1].get_number_of_rules() != 0:
            sending_rule1 = agents[i1].get_sorted_ruleset()[0]
            agents[i2].replace_weakest_rule(sending_rule1)

        if agents[i2].get_number_of_rules() != 0:
            sending_rule2 = agents[i2].get_sorted_ruleset()[0]
            agents[i1].replace_weakest_rule(sending_rule2)

def length_of_vector(vector):
    return math.sqrt(vector[0] ** 2 + vector[1] ** 2)

class BoxAgent(Agent):
    def __init__(self, position=[0,0], size=[10,10], visibility=1, identifier="", condition=None, parent_layout=None):

        # to avoid import error, avoid to use initial value
        if condition == None: condition = Condition()

        Agent.__init__(self, condition, identifier)
        self.position = position
        self.size = size
        self.visibility = visibility
        self.set_parent_layout(parent_layout)
        self.set_inner_layout(None)

    def get_x(self):
        return self.position[0]

    def get_y(self):
        return self.position[1]

    def get_width(self):
        return self.size[0]

    def get_height(self):
        return self.size[1]

    def set_x(self, value):
        x_before_movement = self.get_x()
        base_box = self.parent_layout.base_box
        left_limit = 0
        right_limit = base_box.get_width()

        if value < left_limit:
            x_after_movement = left_limit + 1
        elif right_limit < value + self.get_width():
            x_after_movement = right_limit - self.get_width() - 1
        else:
            x_after_movement = value

        amount_to_move = x_after_movement - x_before_movement
        self.position[0] = x_after_movement

    def set_y(self, value):
        base_box = self.parent_layout.base_box
        top_limit = 0
        bottom_limit = base_box.get_height()

        if value < top_limit:
            y_after_movement = top_limit + 1
        elif bottom_limit < value + self.get_height():
            y_after_movement = bottom_limit - self.get_height() -1
        else:
            y_after_movement = value

        amount_to_move = y_after_movement - value
        self.position[1] = y_after_movement

    def set_width(self, value):
        base_box = self.parent_layout.base_box
        right_limit = base_box.get_x()+ base_box.get_width()

        if value < 0: value = 0

        if self.get_x() + value < right_limit:
            self.size[0] = value
        else:
            self.size[0] = right_limit - self.get_x()

    def set_height(self, value):
        base_box = self.parent_layout.base_box
        bottom_limit = base_box.get_y()+ base_box.get_height()

        if value < 0: value = 0

        if self.get_y() + value < bottom_limit:
            self.size[1] = value
        else:
            self.size[1] = bottom_limit - self.get_y()

    def set_parent_layout(self, parent_layout):
        self.parent_layout = parent_layout

    def set_inner_layout(self, inner_layout):
        self.inner_layout = inner_layout

    def make_visible(self):
        self.visibility = 1

    def make_invisible(self):
        self.visibility = 0

    def render(self, parent_panel):

        if self.visibility == 1:
            border = wx.SIMPLE_BORDER
        else:
            border = wx.NO_BORDER

        panel = wx.Panel(parent_panel, wx.ID_ANY, pos=self.position, size=self.size, style=border)
        panel.SetBackgroundColour("#ffffff")

        # if this box has boxes(layout) in itself, render them
        if self.inner_layout:
            self.inner_layout.render(panel)

    #add rule which has present condition and random action
    def add_rule_with_random_action(self, layout):
        situation = Situation(agent_set=layout, agent=self)
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
        current_situation = Situation(agent_set=layout, agent=self)

        for rule in self.ruleset:
            if rule.condition.evaluate(current_situation):
                matching_rule = rule
                break

        return matching_rule

    def get_right_position(self, margin):
        present_x, present_y = self.position
        return [present_x + self.get_width() + margin, present_y]

    def get_bottom_position(self, margin):
        present_x, present_y = self.position
        return [present_x, present_y + self.get_height() + margin]

    def get_center_x(self):
        parent_box = self.parent_layout.base_box
        return (parent_box.get_width() - self.get_width()) / 2

    def get_center_y(self):
        parent_box = self.parent_layout.base_box
        return (parent_box.get_width() - self.get_height()) / 2

    def add_x(self, amount):
        x_after_movement = (self.get_x() + amount)
        self.set_x(x_after_movement)

    def add_y(self, amount):
        y_after_movement = (self.get_y() + amount)
        self.set_y(y_after_movement)

    def add_vector(self, vector):
        self.add_x(vector[0])
        self.add_y(vector[1])

    def add_width(self, amount):
        self.set_width(self.get_width() + amount)

    def add_height(self, amount):
        self.set_height(self.get_height() + amount)

    def align_left(self, target_box):
        self.set_x( target_box.get_x())

    def align_top(self, target_box):
        self.set_y(target_box.get_y())

    def unify_width_and_align(self, target_box):
        self.align_left(target_box)
        self.set_width(target_box.get_width())

    def unify_height_and_align(self, target_box):
        self.align_top(target_box)
        self.set_height(target_box.get_height())

    # place itself next to given box making given amount of vertical space
    def make_vertical_space(self, box, amount):
        if box.get_y() < self.get_y():
            self.set_y(box.get_y() + box.get_height() + amount)
        else:
            self.set_y(box.get_y() - self.get_height() - amount)

    # place itself next to given box making given amount of horizontal space
    def make_horizontal_space(self, box, amount):
        if box.get_x() < self.get_x():
            self.set_x(box.get_x() + box.get_width() + amount)
        else:
            self.set_x(box.get_x() - self.get_width()- amount)

    def get_nearest_box(self, layout):

        pairs = [(BoxAgent.get_gravity_distance(self, box), box)  for box in layout.agents]
        pairs.sort()

        # take 1st box as nearest box because 0th box is box itself
        nearest_box = pairs[1][1]

        return nearest_box

    def get_position_difference(self,box,i):
        return abs(self.position[i] - box.position[i])

    def get_most_aligned_box(self, layout):

        pairs = []
        for box in layout.agents:
            smaller_difference = min(self.get_position_difference(box,0), self.get_position_difference(box,1))

            # in case smaller_difference is same, add gravity distance to make difference
            scaled_gravity_distance = BoxAgent.get_gravity_distance(self, box) / 200
            pairs.append((smaller_difference + scaled_gravity_distance, box))

        pairs.sort()

        # take 1st box as most_aligned box because 0th box is box itself
        most_aligned_box = pairs[1][1]

        return most_aligned_box

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
        gravity_x = self.get_x() + self.get_width() / 2
        gravity_y = self.get_y() + self.get_height() / 2

        return [gravity_x, gravity_y]

    def off_the_edge_or_not(self):
        off_right_or_bottom = (self.get_x() + self.get_width()) > WINDOW_SIZE[0] or (self.get_y() + self.get_height()) > WINDOW_SIZE[1]
        off_left_or_top = self.get_x() < 0 or self.get_y() < 0

        return off_right_or_bottom or off_left_or_top


    def get_vertically_splited_boxes(self, margin):
        original_rule = self.get_copy_of_ruleset()

        splited_width = (self.get_width() - margin) / 2
        splited_size = [splited_width , self.get_height()]
        box1 = BoxAgent(self.position, splited_size)
        box1.set_ruleset(original_rule)

        box2_position = [self.get_x() + (self.get_width() + margin) / 2, self.get_y()]
        box2 = BoxAgent(box2_position, splited_size)
        box2.set_ruleset(original_rule)

        return box1, box2

    @classmethod
    def overlap_or_not(cls, box1, box2):
        difference_x = abs(box1.get_x() - box2.get_x())
        difference_y = abs(box1.get_y() - box2.get_y())

        if box1.get_x() < box2.get_x():
            box_on_left = box1
        else:
            box_on_left = box2

        if box1.get_y() < box2.get_y():
            box_on_top = box1
        else:
            box_on_top = box2

        return difference_x < box_on_left.get_width() and difference_y < box_on_top.get_height() 

    @classmethod
    def aligned_or_not(cls, box1, box2):
        return box1.get_x() == box2.get_x() or box1.get_y() == box2.get_y()

    @classmethod
    def get_basic_distance_vector(cls, box1, box2):
        basic_distance_x = (box1.get_width() + box2.get_width()) /2
        basic_distance_y = (box1.get_height() + box2.get_height()) /2
        return [basic_distance_x, basic_distance_y]

    @classmethod
    def get_gravity_distance(cls, box1, box2):
        return length_of_vector(box1.get_gravity_difference(box2))

    @classmethod
    #
    def get_overlaped_area(cls, box1, box2):
        if cls.overlap_or_not(box1, box2):
            overlaped_width = min(box1.get_x() + box1.get_width(), box2.get_x() + box2.get_width()) - max(box1.get_x(), box2.get_x())
            overlaped_height = min(box1.get_y() + box1.get_height(), box2.get_y() + box2.get_height()) - max(box1.get_y(), box2.get_y())

            return overlaped_width * overlaped_height
        else:
            return 0


# imports - - - - - - -
import wx
import random
from main import WINDOW_SIZE
from rule import *
from condition import *
