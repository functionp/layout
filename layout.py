#-*- coding: utf-8 -*-


class AgentSet():
    def __init__(self, agents=[]):
        self.agents = agents

    def get_copy(self):
        return AgentSet(self.agents[:])

    def add_agent(self, agent):
        self.agents.append(agent)

    def remove_agent(self, agent):
        self.agents.remove(agent)

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
        rule_not_found_or_not = False

        for agent in (self).agents:

            # if no rule is matched, make new rule
            if agent.get_matching_rule(self) == None:

                rule_not_found_or_not = True

                # generate new rule with condition of present situation
                if agent.add_rule_with_random_action(self):
                    rule_generated_or_not = True

        return [rule_not_found_or_not, rule_generated_or_not]

    def delete_weak_rules(self):
        rule_deleted_or_not = False

        for agent in (self).agents:
            if agent.delete_weak_rules():
                rule_deleted_or_not = True

        return rule_deleted_or_not


class Layout(AgentSet):
    def __init__(self, agents=[], base_box=None):

        # to avoid import error, avoid to use initial value
        if base_box == None: base_box = BoxAgent([0,0], main.WINDOW_SIZE)
        self.agents = agents
        self.set_base_box(base_box)

        for agent in agents:
            agent.set_parent_layout(self)

    def set_base_box(self, base_box):
        self.base_box = base_box
        base_box.set_inner_layout(self)

    def add_box(self, box):
        self.agents.append(box)
        box.set_parent_layout(self)

    def get_copy(self):
        return Layout(self.agents[:])

    def render(self, parent_panel):
        for agent in self.agents:
            agent.render(parent_panel)


class SampleLayout(Layout):
    def __init__(self):

        margin = 20

        base_box = BoxAgent([200,20], [950,900], 1)

        boxes = []

        header_condition = Condition()
        side_condition = Condition([BoxCondition.width_limit(100)] , 1)
        main_condition = Condition([BoxCondition.width_limit(800)] , 1)

        boxes.append(BoxAgent([10,10], [800,100], 1, "header", header_condition))
        boxes.append(BoxAgent(boxes[0].get_bottom_position(margin), [200,400], 1, "side", side_condition))
        boxes.append(BoxAgent(boxes[1].get_right_position(margin), [100,400], 1,  "main", main_condition))
        boxes.append(BoxAgent(boxes[1].get_bottom_position(margin), [800,100], 1))

        layout = Layout(boxes, base_box)

        Layout.__init__(self, [base_box])

# imports - - - - - - -
from condition import *
import main
from agent import *
