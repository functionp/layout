#-*- coding: utf-8 -*-

class AgentSet():
    def __init__(self, agents=[]):
        self.agents = agents
        
    def get_copy(self):
        return AgentSet(self.agents[:])

    def update(self, agents):
        self.agents = agents

    def get_number_of_agents(self):
        return len(self.agents)

    def set_rulesets(self, rulesets):
        if rulesets != []:
            for i, agent in enumerate(self.agents):
                agent.ruleset = rulesets[i]

    def get_rulesets(self):
        return [agent.ruleset for agent in self.agents]

    # generate new rules 
    def generate_rules(self):

        rule_generated_or_not = False

        for agent in (self).agents:

            # if no rule is matched, make new rule
            if agent.get_matching_rule(self) == None:

                # generate new rule with condition of present situation
                agent.add_rule_with_random_action(self)
                rule_generated_or_not = True

        return rule_generated_or_not


class Layout(AgentSet):
    def __init__(self, agents=[]):
        self.agents = agents

    def get_copy(self):
        return Layout(self.agents[:])

    def render(self, parent):
        for agent in self.agents:
            agent.render(parent)



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
