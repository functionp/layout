#-*- coding: utf-8 -*-


class AgentSet():
    def __init__(self, agents=[], condition=None):
        self.agents = agents
        self.set_condition(condition)

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

    def set_condition(self, condition):
        self.condition = condition

    def set_rulesets(self, rulesets):
        if rulesets != []:
            for i, agent in enumerate(self.agents):
                agent.set_ruleset(rulesets[i])

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
    def __init__(self, agents=[], base_box=None, condition=None):

        # to avoid import error, avoid to use initial value
        if base_box == None: base_box = BoxAgent(Style([0,0], main.WINDOW_SIZE, 0))
        if condition == None: condition = Condition()

        AgentSet.__init__(self, agents, condition)

        self.set_base_box(base_box)
        self.optimization_needed = False

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

    def get_minimum_inclusion_size(self):
        """Get size of minimum rectangle which includes all box in layout"""

        x_list = [box.get_x() for box in self.agents]
        end_x_list = [box.get_x() + box.get_width() for box in self.agents]
        y_list = [box.get_y() for box in self.agents]
        end_y_list = [box.get_y() + box.get_height() for box in self.agents]
        
        inclusion_width = reduce(max, end_x_list) - reduce(min, x_list)
        inclusion_height = reduce(max, end_y_list) - reduce(min, y_list)

        return [inclusion_width, inclusion_height]


    def get_sum_of_all_constraint_objective(self):
        sum_of_all_constraint_objective = 0
        sum_of_all_constraint_objective += self.condition.get_sum_of_constraint_objective(Situation(agent_set=self))

        for agent in self.agents:
            situation = Situation(agent_set=self, agent=agent)
            sum_of_all_constraint_objective += agent.condition.get_sum_of_constraint_objective(situation)

        return sum_of_all_constraint_objective

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

    def get_copy_of_agents(self):
        return [agent.get_copy() for agent in self.agents]

    def get_copy(self):
        return Layout(self.get_copy_of_agents(), self.base_box, self.condition)

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
    def get_sample_layout(cls):

        MAIN_WIDTH = 750
        margin = 20
        MAX_WIDTH = main.WINDOW_SIZE[0]
        MAX_HEIGHT = main.WINDOW_SIZE[1]

        # base_layout

        base_box = BoxAgent(Style([0,0], main.WINDOW_SIZE, 0), "base")
        base_inner_box = BoxAgent(Style([0,0], [MAIN_WIDTH, MAX_HEIGHT], 1), "base_inner")
        base_inner_box.set_x(base_inner_box.get_center_x())

        base_layout = Layout([base_inner_box], base_box)

        # base_inner_layout

        header_style = Style([0,0], [MAIN_WIDTH, 80], 1)
        header_box = BoxAgent(header_style, "header")

        main_style = Style(header_box.get_bottom_position(margin), [MAIN_WIDTH, 600], 0)
        main_box = BoxAgent(main_style, "main")

        base_inner_layout_condition = Condition([BoxCondFun.no_overlap(), BoxCondFun.all_aligned(), BoxCondFun.width_unification(1)], 1)
        base_inner_layout = Layout([header_box, main_box], base_inner_box, base_inner_layout_condition)
        base_inner_layout.set_optimization_needed(False)

        # main_layout

        content_style = Style([400,2], [280, 280], 1)
        content_condition = Condition([BoxCondFun.width_constraint(550,590), BoxCondFun.height_constraint(500)] , 1)
        content_box = BoxAgent(content_style, "content", content_condition)

        side_style = Style([400,2], [280, 280], 1)
        side_condition = Condition([BoxCondFun.width_constraint(140,160), BoxCondFun.height_constraint(500)] , 1)
        side_box = BoxAgent(side_style, "side", side_condition)

        main_layout_condition = Condition([BoxCondFun.no_overlap(), BoxCondFun.all_aligned()], 1)
        main_layout = Layout([content_box, side_box], main_box, main_layout_condition)
        main_layout.set_optimization_needed(True)

        # side_layout

        side_item_style = Style([0,0], [30, 30], 1)
        side_item_condition = Condition([BoxCondFun.width_constraint(120,140), BoxCondFun.height_constraint(80, None, 0)] , 1)
        side_item_boxes = []
        side_item_boxes.append(BoxAgent(side_item_style.get_copy(), "side_item1", side_item_condition))
        side_item_boxes.append(BoxAgent(side_item_style.get_copy(), "side_item2", side_item_condition))

        side_layout_condition = Condition([BoxCondFun.no_overlap(), BoxCondFun.all_aligned(), BoxCondFun.width_unification(1)], 1)
        side_layout = Layout(side_item_boxes, side_box, side_layout_condition)
        #side_layout.set_optimization_needed(True)

        # content_layout

        content_item_style = Style([0,0], [240, 240], 1)
        content_item_condition = Condition([BoxCondFun.height_constraint(80, 110), BoxCondFun.width_constraint(300, 590), ] , 1)
        content_item_box1 = BoxAgent(content_item_style.get_copy(), "content_item1", content_item_condition)
        content_item_box2 = BoxAgent(content_item_style.get_copy(), "content_item2", content_item_condition)

        content_layout_condition = Condition([BoxCondFun.no_overlap(), BoxCondFun.all_aligned(), BoxCondFun.horizontal_margin_constraint(40)], 1)
        content_layout = Layout([content_item_box1, content_item_box2], content_box, content_layout_condition)
        content_layout.set_optimization_needed(True)

        # content_item_layout

        content_image_style = Style([0,0], [30, 30], 1)
        content_image_condition = Condition([BoxCondFun.height_constraint(60,90,1)] , 1)
        content_image_box = BoxAgent(content_image_style, "content_image", content_image_condition, "image")

        content_text_style = Style([0, 120],[30, 30], 1)
        content_text_condition = Condition([BoxCondFun.height_constraint(50, 80, 1)] , 1)
        content_text_box = BoxAgent(content_text_style, "side", content_text_condition, "text")

        content_item_layout_condition = Condition([BoxCondFun.no_overlap(), BoxCondFun.all_aligned(), BoxCondFun.horizontal_margin_constraint(40)], 1)
        content_item_layout1 = Layout([content_image_box.get_copy(), content_text_box.get_copy()], content_item_box1, content_item_layout_condition)
        content_item_layout2 = Layout([content_image_box.get_copy(), content_text_box.get_copy()], content_item_box2, content_item_layout_condition)
        #content_item_layout1.set_optimization_needed(True)
        #content_item_layout2.set_optimization_needed(True)


        return base_layout

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

        header_inner_item_style = Style([200,10], [185,55], 1)
        logo_condition = Condition([BoxCondFun.width_constraint(120,150), BoxCondFun.y_constraint(2), BoxCondFun.x_constraint(0, 10) ] , 1)
        phone_condition = Condition([BoxCondFun.width_constraint(120,170), BoxCondFun.y_constraint(2), BoxCondFun.x_end_constraint(MAIN_WIDTH-10, MAIN_WIDTH)] , 1)
        menu_condition = Condition([BoxCondFun.width_constraint(160,180), BoxCondFun.height_constraint(40, 60, 1), BoxCondFun.y_constraint(2), BoxCondFun.y_end_constraint(0,78, 0)] , 1)

        header_inner_item_boxes = []
        #header_inner_item_boxes.append(BoxAgent(header_inner_item_style.get_copy(), "logo", logo_condition))
        #header_inner_item_boxes.append(BoxAgent(header_inner_item_style.get_copy(), "phone", phone_condition))

        header_inner_item_boxes.append(BoxAgent(header_inner_item_style.get_copy(), "menu1", menu_condition, "menu1"))
        header_inner_item_boxes.append(BoxAgent(header_inner_item_style.get_copy(), "menu2", menu_condition, "menu2"))
        header_inner_item_boxes.append(BoxAgent(header_inner_item_style.get_copy(), "menu3", menu_condition, "menu3"))
        header_inner_item_boxes.append(BoxAgent(header_inner_item_style.get_copy(), "menu4", menu_condition, "menu4"))

        header_layout_constraint = Condition([BoxCondFun.no_overlap(), BoxCondFun.all_aligned(), BoxCondFun.height_unification(1)], 1)
        header_inner_layout = Layout(header_inner_item_boxes, header_inner_box, header_layout_constraint)
        header_inner_layout.set_optimization_needed(True)

        # image_area_layout

        image_area_inner_style = Style([0,0], [MAIN_WIDTH, image_area_box.get_height()], 1)
        image_area_inner_condition = Condition()
        image_area_inner_box = BoxAgent(image_area_inner_style, "image_area_inner", image_area_inner_condition)

        image_area_layout = Layout([image_area_inner_box], image_area_box)
        image_area_layout.set_optimization_needed(False)

        image_area_inner_box.set_x(image_area_inner_box.get_center_x())

        image_area_item_style1 = Style([200,10], [75,180], 1)
        image_area_item_style2 = Style([220,30], [75,180], 1)
        image_area_item_style3 = Style([240,50], [75,180], 1)
        pc_image_condition = Condition([BoxCondFun.width_constraint(340,360,1), BoxCondFun.height_constraint(230,265,1)] , 1)
        pr_text_condition = Condition([BoxCondFun.width_constraint(210, 230, 1), BoxCondFun.height_constraint(110,130, 0)] , 1) #height と widthどっちかならできるけどどっちもはむずい
        dl_button_condition = Condition([BoxCondFun.width_constraint(210,230), BoxCondFun.height_constraint(40, 50)] , 1)

        image_area_item_boxes = []
        #image_area_item_boxes.append(BoxAgent(image_area_item_style1.get_copy(), "dl_button", dl_button_condition, "button"))
        #image_area_item_boxes.append(BoxAgent(image_area_item_style2.get_copy(), "pc_image", pc_image_condition, "image"))
        #image_area_item_boxes.append(BoxAgent(image_area_item_style3.get_copy(), "pr_text", pr_text_condition, "text"))

        image_area_constraint = Condition([BoxCondFun.no_overlap(), BoxCondFun.all_aligned()], 1)
        image_area_inner_layout = Layout(image_area_item_boxes, image_area_inner_box, image_area_constraint)
        image_area_inner_layout.set_optimization_needed(False)

        # main_layout

        side_style = Style([10,10], [200,580], 1)
        side_condition = Condition([BoxCondFun.width_constraint(0, 210), BoxCondFun.y_constraint(2), BoxCondFun.x_constraint(2)] , 1)
        side_box = BoxAgent(side_style, "side", side_condition)

        content_style = Style(side_box.get_right_position(margin), [500,280], 1)
        content_box = BoxAgent(content_style, "content")

        main_layout = Layout([], main_box)
        #main_layout = Layout([side_box, content_box], main_box)
        main_layout.set_optimization_needed(False)

        #content_box.set_x(content_box.get_center_x())

        return base_layout

# imports - - - - - - -
from condition import *
from specification import *
import main
from agent import *
