#-*- coding: utf-8 -*-

import math

class Agent():

    max_rules = 20

    def __init__(self, condition, identifier=""):
        self.set_ruleset([])
        self.condition = condition
        self.set_identifier(identifier)

    def set_ruleset(self, ruleset):
        self.ruleset = ruleset

    def set_identifier(self, identifier):
        self.identifier = identifier

    def get_copy(self):
        agent = Agent(self.condition, self.identifier)
        agent.set_ruleset(self.get_copy_of_ruleset())
        return agent

    def get_copy_of_ruleset(self):
        return self.ruleset[:]

    def get_sorted_ruleset(self, border=-1):
        """ Return sorted ruleset according to its strength, and filter the rule whose strength is more than border."""

        pairs = [(rule.strength, rule) for rule in self.ruleset]
        pairs.sort()
        pairs.reverse()
        sorted_ruleset = [pair[1] for pair in pairs]

        return [rule for rule in sorted_ruleset if rule.strength > border]

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

    def replace_weakest_rule(self, rule):
        """Change weakest rule of agent into given rule. (DESTRUCTIVE)"""

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
    def exchange_rule_randomly(cls, agents):
        """Exchange two rules between agents having same condition. (DESTRUCTIVE)"""

        strength_border = 0.9 # do not exchange rule whose strength is less than this value

        i1 = random.randint(0,len(agents)-1)
        agent1 = agents[i1]

        # make array of agents which has same rule with agent1
        agents_with_same_condition = [agent for agent in agents if agent.condition == agent1.condition and agent != agent1]

        if len(agents_with_same_condition) != 0:

            i2 = random.randint(0,len(agents_with_same_condition)-1)
            agent2 = agents_with_same_condition[i2]

            filtered_ruleset1 = agent1.get_sorted_ruleset(strength_border)
            filtered_ruleset2 = agent2.get_sorted_ruleset(strength_border)

            if len(filtered_ruleset1) != 0:
                sending_rule1 = filtered_ruleset1[0].get_copy()
                #sending_rule1.set_strength(Rule.initial_strength)
                agent2.add_rule(sending_rule1)

            if len(filtered_ruleset2) != 0:
                sending_rule2 = filtered_ruleset2[0].get_copy()
                #sending_rule2.set_strength(Rule.initial_strength)
                agent1.add_rule(sending_rule2)

def length_of_vector(vector):
    return math.sqrt(vector[0] ** 2 + vector[1] ** 2)


class Style():
    def __init__(self, position=[0,0], size=[10,10], visibility=1):
        self.position = position
        self.size = size
        self.set_visibility(visibility)

    def set_visibility(self, visibility):
        self.visibility = visibility

    def get_copy(self):
        return Style(self.position[:], self.size[:], self.visibility)


class BoxAgent(Agent):
    def __init__(self, style, identifier="", condition=None, text=""):

        # to avoid import error, avoid to use initial value
        if condition == None: condition = Condition()
        
        Agent.__init__(self, condition, identifier)
        self.set_style(style)
        self.set_parent_layout(None)
        self.set_text(text)
        self.set_inner_layout(None)
        self.set_fixedness(False)

    def get_copy(self):
        box = BoxAgent(self.style.get_copy(), self.identifier, self.condition.get_copy(), self.text)
        box.set_ruleset(self.get_copy_of_ruleset())
        box.set_parent_layout(self.parent_layout)
        box.set_inner_layout(self.inner_layout)
        return box

    def get_position(self):
        return self.style.position

    def get_x(self):
        return self.get_position()[0]

    def get_y(self):
        return self.get_position()[1]

    def get_size(self):
        return self.style.size

    def get_width(self):
        return self.get_size()[0]

    def get_height(self):
        return self.get_size()[1]

    def get_visibility(self):
        return self.style.visibility

    def get_inner_layout(self):
        return self.inner_layout

    def get_limit_position(self):
        if self.parent_layout:
            base_box = self.parent_layout.base_box
            return base_box.get_size()
        else:
            return WINDOW_SIZE

    def set_x(self, value):
        left_limit = 0
        right_limit = self.get_limit_position()[0]

        if value < left_limit:
            x_after_movement = left_limit + 2
        elif right_limit < value + self.get_width():
            x_after_movement = right_limit - self.get_width() - 2
        else:
            x_after_movement = value

        self.style.position[0] = x_after_movement

    def set_y(self, value):
        top_limit = 0
        bottom_limit = self.get_limit_position()[1]

        if value < top_limit:
            y_after_movement = top_limit + 2
        elif bottom_limit < value + self.get_height():
            y_after_movement = bottom_limit - self.get_height() - 2
        else:
            y_after_movement = value

        self.style.position[1] = y_after_movement

    def set_width(self, value):
        right_limit = self.get_limit_position()[0]

        if value < 0: value = 0

        # in case of overflow
        if self.get_x() + value > right_limit:

            if value < right_limit:
                self.set_x(right_limit - value)
            else:
                self.set_x(0)
                value = right_limit

        self.style.size[0] = value


    def set_height(self, value):
        bottom_limit = self.get_limit_position()[1]

        if value < 0: value = 0

        # in case of overflow
        if self.get_y() + value > bottom_limit:

            if value < bottom_limit:
                self.set_y(bottom_limit - value)
            else:
                self.set_y(0)
                value = bottom_limit

        self.style.size[1] = value


    def set_parent_layout(self, parent_layout):
        self.parent_layout = parent_layout

    def set_inner_layout(self, inner_layout):
        self.inner_layout = inner_layout

    def set_style(self, style):
        self.style = style

    def set_text(self, text):
        self.text = text

    def set_fixedness(self, fixedness):
        self.fixedness = fixedness

    def make_visible(self):
        self.style.set_visibility(1)

    def make_invisible(self):
        self.style.set_visibility(0)

    def render(self, parent_panel):

        if self.get_visibility() == 1:
            border = wx.SIMPLE_BORDER
        else:
            border = wx.NO_BORDER

        panel = wx.Panel(parent_panel, wx.ID_ANY, pos=self.get_position(), size=self.get_size(), style=border)
        panel.SetBackgroundColour("#ffffff")

        if self.text:
            text = wx.StaticText(panel, wx.ID_ANY, self.text, (0,0), size=self.get_size())
            text.SetBackgroundColour('#ffffff')

        # if this box has boxes(layout) in itself, render them
        if self.inner_layout:
            self.inner_layout.render(panel)

    def add_rule_with_random_action(self, layout):
        """Add rule which has present condition and random action."""

        situation = Situation(agent_set=layout, agent=self)
        condition = Condition.make_condition(situation)

        if condition.condfuns != []:
            new_rule = BoxRule.generate_rule_with_random_action(condition, layout)
            self.add_rule(new_rule)
            return True

        # if no condition can be represents current situation, add no rule
        else:
            return False

    def get_matching_rule(self, layout):
        """Find (the strongest) rule which matches current condition(layout and box) and return it. return None if no rule is found."""

        self.ruleset = self.get_sorted_ruleset()
        matching_rule = None
        current_situation = Situation(agent_set=layout, agent=self)

        for rule in self.ruleset:
            if rule.condition.evaluate(current_situation, 1):
                matching_rule = rule
                break

        return matching_rule

    def get_right_position(self, margin):
        present_x, present_y = self.get_position()
        return [present_x + self.get_width() + margin, present_y]

    def get_bottom_position(self, margin):
        present_x, present_y = self.get_position()
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
        self.set_x(target_box.get_x())

    def align_top(self, target_box):
        self.set_y(target_box.get_y())

    def unify_width_and_align(self, target_box):
        self.align_left(target_box)
        self.set_width(target_box.get_width())

    def unify_height_and_align(self, target_box):
        self.align_top(target_box)
        self.set_height(target_box.get_height())

    def make_vertical_space(self, box, amount):
        """Place itself next to given box making given amount of vertical space."""

        if box.get_y() < self.get_y():
            self.set_y(box.get_y() + box.get_height() + amount)
        else:
            self.set_y(box.get_y() - self.get_height() - amount)

    def make_horizontal_space(self, box, amount):
        """Place itself next to given box making given amount of horizontal space."""

        if box.get_x() < self.get_x():
            self.set_x(box.get_x() + box.get_width() + amount)
        else:
            self.set_x(box.get_x() - self.get_width()- amount)

    def get_the_best_box_from_pairs(self, pairs):
        """Return the box which has the highest pair value in the list of pairs."""

        pairs.sort()

        if len(pairs) == 1 :
            best_box = pairs[0][1]
        else: 
            # take 1st box as nearest box because 0th box is box itself
            best_box = pairs[1][1]

        return best_box

    def get_nearest_box(self, layout):
        pairs = [(BoxAgent.get_gravity_distance(self, box), box)  for box in layout.agents]

        return self.get_the_best_box_from_pairs(pairs)

    def get_most_aligned_box(self, layout):

        pairs = []
        for box in layout.agents:
            alignemnt_distance = self.get_alignment_distance(self, box)

            # in case smaller_difference is same, add gravity distance to make difference
            scaled_gravity_distance = BoxAgent.get_gravity_distance(self, box) / 200
            pairs.append((alignemnt_distance + scaled_gravity_distance, box))

        return self.get_the_best_box_from_pairs(pairs)

    def get_position_difference(self,box,i):
        return abs(self.get_position()[i] - box.get_position()[i])

    def get_gravity_difference(self, target_box):
        """Get difference(signed distance) of gravity."""

        self_gravity = self.get_gravity_position()
        target_gravity = target_box.get_gravity_position()

        gravity_difference_x = self_gravity[0] - target_gravity[0]
        gravity_difference_y = self_gravity[1] - target_gravity[1]

        return [gravity_difference_x, gravity_difference_y]

    def change_distance(self, target_box, amount):
        """Stay away from target, or approach to target."""

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

    def get_gravity_position(self):
        """Get the position of center of gravity."""
        gravity_x = self.get_x() + self.get_width() / 2
        gravity_y = self.get_y() + self.get_height() / 2

        return [gravity_x, gravity_y]

    def off_the_edge_or_not(self):
        off_right_or_bottom = (self.get_x() + self.get_width()) > WINDOW_SIZE[0] or (self.get_y() + self.get_height()) > WINDOW_SIZE[1]
        off_left_or_top = self.get_x() < 0 or self.get_y() < 0

        return off_right_or_bottom or off_left_or_top

    @classmethod
    def overlap_or_not(cls, box1, box2):
        return cls.get_overlaped_area(box1, box2) > 0

    @classmethod
    def aligned_or_not(cls, box1, box2):
        return box1.get_x() == box2.get_x() or box1.get_y() == box2.get_y()

    @classmethod
    def get_basic_distance_vector(cls, box1, box2):
        basic_distance_x = (box1.get_width() + box2.get_width()) /2
        basic_distance_y = (box1.get_height() + box2.get_height()) /2
        return [basic_distance_x, basic_distance_y]
        
    @classmethod
    def get_alignment_distance(cls, box1, box2):
        return min(box1.get_position_difference(box2,0), box1.get_position_difference(box2,1))
        
    @classmethod
    def get_gravity_distance(cls, box1, box2):
        return length_of_vector(box1.get_gravity_difference(box2))

    @classmethod
    def get_overlaped_area(cls, box1, box2):
        overlaped_width = min(box1.get_x() + box1.get_width(), box2.get_x() + box2.get_width()) + 2 - (max(box1.get_x(), box2.get_x()))
        overlaped_height = min(box1.get_y() + box1.get_height(), box2.get_y() + box2.get_height()) + 2 - (max(box1.get_y(), box2.get_y()))

        if overlaped_width > 0 and overlaped_height > 0:
            return overlaped_width * overlaped_height
        else:
            return 0


# imports - - - - - - -
import wx
import random
from main import WINDOW_SIZE
from rule import *
from condition import *
