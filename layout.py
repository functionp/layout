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
        if base_box == None: base_box = BoxAgent(Style([0,0], main.WINDOW_SIZE, 0))
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

    def get_agent_with_identifier(self, identifier):
        for agent in self.agents:

            if agent.identifier == identifier:
                return agent
                break
            
            if agent.inner_layout: return agent.inner_layout.get_agent_with_identifier(identifier)


    def get_copy(self):
        return Layout(self.agents[:])

    def render(self, parent_panel):
        for agent in self.agents:
            agent.render(parent_panel)

    def evaluate_agent_constraint(self):
        bool_list = []
        for agent in self.agents:
            situation = Situation(agent=agent)
            bool_list.append(agent.condition.evaluate(situation))

        if len(bool_list) == 0:
            return True
        else:
            return reduce((lambda b1, b2: b1 and b2), bool_list)

class SampleLayout(Layout):
    def __init__(self):

        margin = 20

        # base_layout

        base_box = BoxAgent(Style([0,0], main.WINDOW_SIZE, 0), "base")
        max_width = main.WINDOW_SIZE[0]

        header_style = Style([0,0], [max_width, 100], 1)
        header_condition = Condition([BoxCondition.width_constraint(max_width, max_width)], 1)
        header_box = BoxAgent(header_style, "header", header_condition)

        main_style = Style(header_box.get_bottom_position(margin), [780,600], 0)
        main_condition = Condition([BoxCondition.width_constraint(0, 800)] , 1)
        main_box = BoxAgent(main_style,  "main", main_condition)

        footer_style = Style(main_box.get_bottom_position(margin), [max_width,100], 1)
        footer_box = BoxAgent(footer_style, "header")

        base_layout = Layout([header_box, main_box, footer_box], base_box)

        main_box.set_x(main_box.get_center_x())

        # main_layout

        side_style = Style([0,0], [400,580], 1)
        side_condition = Condition([BoxCondition.width_constraint(0, 210), BoxCondition.y_constraint(2), BoxCondition.x_constraint(2)] , 1)
        side_box = BoxAgent(side_style, "side", side_condition, "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatext!!")

        content_style = Style(side_box.get_right_position(margin), [500,280], 1)
        content_box = BoxAgent(content_style, "content")

        main_layout = Layout([side_box, content_box], main_box)

        #content_box.set_x(content_box.get_center_x())

        Layout.__init__(self, [base_box])

# imports - - - - - - -
from condition import *
import main
from agent import *
