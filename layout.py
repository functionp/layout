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
        self.optimization = False

        for agent in agents:
            agent.set_parent_layout(self)

    def set_base_box(self, base_box):
        self.base_box = base_box
        base_box.set_inner_layout(self)

    def set_optimization_needed(self, value):
        self.optimization_needed = value

    def add_box(self, box):
        self.agents.append(box)
        box.set_parent_layout(self)

    def get_agent_with_identifier(self, identifier):

        result = None
        for agent in self.agents:

            if agent.identifier == identifier:
                result = agent
                break 

            if agent.inner_layout: 
                result = agent.inner_layout.get_agent_with_identifier(identifier)
                if result != None: break

        return result

    def get_copy(self):
        return Layout(self.agents[:], self.base_box)

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

    @classmethod
    def get_softplanner_layout(cls):

        MAIN_WIDTH = 750
        margin = 20

        # base_layout

        base_box = BoxAgent(Style([0,0], main.WINDOW_SIZE, 0), "base")
        max_width = main.WINDOW_SIZE[0]

        header_style = Style([0,0], [max_width, 80], 1)
        header_condition = Condition([BoxCondFun.width_constraint(max_width, max_width)], 1)
        header_box = BoxAgent(header_style, "header", header_condition)

        image_area_style = Style(header_box.get_bottom_position(3), [header_box.get_width(), 270], 1)
        image_area_condition = Condition()
        image_area_box = BoxAgent(image_area_style, "image_area", image_area_condition)

        main_style = Style(image_area_box.get_bottom_position(margin), [MAIN_WIDTH, 600], 1)
        main_condition = Condition([BoxCondFun.width_constraint(0, 800)] , 1)
        main_box = BoxAgent(main_style, "main", main_condition)

        footer_style = Style(main_box.get_bottom_position(margin), [max_width,100], 1)
        footer_condition = Condition([BoxCondFun.width_constraint(0, 800)] , 1)
        footer_box = BoxAgent(footer_style, "footer")

        #base_layout = Layout([header_box, image_area_box], base_box)
        base_layout = Layout([header_box, image_area_box, main_box], base_box)
        base_layout.set_optimization_needed(False)

        main_box.set_x(main_box.get_center_x())

        # header_layout

        header_inner_style = Style([0,0], [MAIN_WIDTH, header_box.get_height()], 1)
        header_inner_condition = Condition()
        header_inner_box = BoxAgent(header_inner_style, "header_inner_menu", header_inner_condition)

        header_layout = Layout([header_inner_box], header_box)
        header_layout.set_optimization_needed(False)

        header_inner_box.set_x(header_inner_box.get_center_x())

        header_inner_item_style = Style([200,10], [75,50], 1)
        logo_condition = Condition([BoxCondFun.width_constraint(120,150), BoxCondFun.y_constraint(2), BoxCondFun.x_constraint(0, 10) ] , 1)
        phone_condition = Condition([BoxCondFun.width_constraint(120,170), BoxCondFun.y_constraint(2), BoxCondFun.x_end_constraint(MAIN_WIDTH-10, MAIN_WIDTH)] , 1)

        header_inner_item_boxes = []
        #header_inner_item_boxes.append(BoxAgent(header_inner_item_style.get_copy(), "logo", logo_condition))
        #header_inner_item_boxes.append(BoxAgent(header_inner_item_style.get_copy(), "phone", phone_condition))

        header_inner_layout = Layout(header_inner_item_boxes, header_inner_box)
        header_inner_layout.set_optimization_needed(False)

        # image_area_layout

        image_area_inner_style = Style([0,0], [MAIN_WIDTH, image_area_box.get_height()], 1)
        image_area_inner_condition = Condition()
        image_area_inner_box = BoxAgent(image_area_inner_style, "image_area_inner", image_area_inner_condition)

        image_area_layout = Layout([image_area_inner_box], image_area_box)
        image_area_layout.set_optimization_needed(False)

        image_area_inner_box.set_x(image_area_inner_box.get_center_x())

        image_area_item_style = Style([200,10], [75,180], 1)
        dl_button_condition = Condition([BoxCondFun.width_constraint(210,230), BoxCondFun.height_constraint(40, 50)] , 1)
        pc_image_condition = Condition([BoxCondFun.width_constraint(340,360,1), BoxCondFun.height_constraint(190,210,1)] , 1)
        pr_text_condition = Condition([BoxCondFun.width_constraint(210, 230, 1), BoxCondFun.height_constraint(110,130, 0)] , 1) #height と widthどっちかならできるけどどっちもはむずい

        image_area_item_boxes = []
        #image_area_item_boxes.append(BoxAgent(image_area_item_style.get_copy(), "dl_button", dl_button_condition))
        image_area_item_boxes.append(BoxAgent(image_area_item_style.get_copy(), "pc_image", pc_image_condition))
        image_area_item_boxes.append(BoxAgent(image_area_item_style.get_copy(), "pr_text", pr_text_condition))

        image_area_inner_layout = Layout(image_area_item_boxes, image_area_inner_box)
        image_area_inner_layout.set_optimization_needed(True)

        # main_layout

        side_style = Style([10,10], [200,580], 1)
        side_condition = Condition([BoxCondFun.width_constraint(0, 210), BoxCondFun.y_constraint(2), BoxCondFun.x_constraint(2)] , 1)
        side_box = BoxAgent(side_style, "side", side_condition)

        content_style = Style(side_box.get_right_position(margin), [500,280], 1)
        content_box = BoxAgent(content_style, "content")

        main_layout = Layout([], main_box)
        main_layout.set_optimization_needed(False)
        #main_layout = Layout([side_box, content_box], main_box)

        #content_box.set_x(content_box.get_center_x())

        return base_layout

class SampleLayout(Layout):
    def __init__(self):

        MAIN_WIDTH = 750
        margin = 20

        # base_layout

        base_box = BoxAgent(Style([0,0], main.WINDOW_SIZE, 0), "base")
        max_width = main.WINDOW_SIZE[0]

        header_style = Style([0,0], [max_width, 80], 1)
        header_condition = Condition([BoxCondFun.width_constraint(max_width, max_width)], 1)
        header_box = BoxAgent(header_style, "header", header_condition)

        global_menu_style = Style(header_box.get_bottom_position(3), [header_box.get_width(), 80], 1)
        global_menu_condition = Condition()
        global_menu_box = BoxAgent(global_menu_style, "global_menu", global_menu_condition)

        main_style = Style(global_menu_box.get_bottom_position(margin), [MAIN_WIDTH, 600], 1)
        main_condition = Condition([BoxCondFun.width_constraint(0, 800)] , 1)
        main_box = BoxAgent(main_style, "main", main_condition)

        footer_style = Style(main_box.get_bottom_position(margin), [max_width,100], 1)
        footer_condition = Condition([BoxCondFun.width_constraint(0, 800)] , 1)
        footer_box = BoxAgent(footer_style, "footer")

        base_layout = Layout([header_box, global_menu_box, main_box, footer_box], base_box)

        main_box.set_x(main_box.get_center_x())

        # header_layout

        header_inner_style = Style([0,0], [MAIN_WIDTH, header_box.get_height()], 1)
        header_inner_condition = Condition()
        header_inner_box = BoxAgent(header_inner_style, "header_inner_menu", header_inner_condition)

        header_inner_layout = Layout([header_inner_box], header_box)
        header_inner_box.set_x(header_inner_box.get_center_x())

        header_inner_item_style = Style([200,10], [75,50], 1)
        header_inner_item_condition = Condition([BoxCondFun.width_constraint(70), BoxCondFun.y_constraint(2), ] , 1)

        header_inner_item_boxes = []
        header_inner_item_boxes.append(BoxAgent(header_inner_item_style.get_copy(), "logo", header_inner_item_condition))
        header_inner_item_boxes.append(BoxAgent(header_inner_item_style.get_copy(), "pohone", header_inner_item_condition))

        header_inner_layout = Layout(header_inner_item_boxes, header_inner_box)

        # global_menu_layout

        global_inner_menu_style = Style([0,0], [MAIN_WIDTH, global_menu_box.get_height()], 1)
        global_inner_menu_condition = Condition()
        global_inner_menu_box = BoxAgent(global_inner_menu_style, "global_inner_menu", global_inner_menu_condition)

        global_inner_menu_layout = Layout([global_inner_menu_box], global_menu_box)
        global_inner_menu_box.set_x(global_inner_menu_box.get_center_x())

        global_menu_item_style = Style([200,10], [75,50], 1)
        global_menu_item_condition = Condition([BoxCondFun.width_constraint(70), BoxCondFun.y_constraint(2), ] , 1)

        global_menu_item_boxes = []
        global_menu_item_boxes.append(BoxAgent(global_menu_item_style.get_copy(), "", global_menu_item_condition))
        global_menu_item_boxes.append(BoxAgent(global_menu_item_style.get_copy(), "", global_menu_item_condition))
        global_menu_item_boxes.append(BoxAgent(global_menu_item_style.get_copy(), "", global_menu_item_condition))

        global_menu_layout = Layout(global_menu_item_boxes, global_inner_menu_box)

        # main_layout

        side_style = Style([10,10], [200,580], 1)
        side_condition = Condition([BoxCondFun.width_constraint(0, 210), BoxCondFun.y_constraint(2), BoxCondFun.x_constraint(2)] , 1)
        side_box = BoxAgent(side_style, "side", side_condition)

        content_style = Style(side_box.get_right_position(margin), [500,280], 1)
        content_box = BoxAgent(content_style, "content")

        main_layout = Layout([side_box, content_box], main_box)

        #content_box.set_x(content_box.get_center_x())

        Layout.__init__(self, [base_box])

# imports - - - - - - -
from condition import *
from specification import *
import main
from agent import *
