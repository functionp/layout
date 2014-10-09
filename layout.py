#-*- coding: utf-8 -*-

class Layout():
    def __init__(self, boxes):
        self.boxes = boxes
        
    def get_copy(self):
        return Layout(self.boxes[:])

    def update(self, boxes):
        self.boxes = boxes

    def get_number_of_boxes(self):
        return len(self.boxes)

    def render(self, parent):
        for box in self.boxes:
            box.render(parent)

    def set_rulesets(self, rulesets):
        for i, box in enumerate(self.boxes):
            box.ruleset = rulesets[i]

    def get_rulesets(self):
        return [box.ruleset for box in self.boxes]

    # generate new rules 
    def generate_rules(self):

        for box in (self).boxes:

            # if no rule is matched, make new rule
            if box.get_matching_rule(self) == None:

                # generate new rule with condition of present situation
                box.add_rule_with_random_action(self)



class SampleLayout(Layout):
    def __init__(self):

        boxes = []
        margin = 20
        boxes.append(BoxAgent([50,50], [200,200]))
        boxes.append(BoxAgent(boxes[0].get_right_position(margin), [100,200]))
        boxes.append(BoxAgent(boxes[1].get_right_position(margin), [100,200]))
        boxes.append(BoxAgent(boxes[0].get_bottom_position(margin), [100,200]))
        boxes.append(BoxAgent(boxes[3].get_right_position(margin), [350,200]))
        boxes.append(BoxAgent(boxes[4].get_right_position(margin), [100,200]))

        Layout.__init__(self, boxes)

# imports - - - - - - -
from agent import *
import main
