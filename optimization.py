#-*- coding: utf-8 -*-

class Optimization():

    def __init__(self, specification):
        self.specification = specification

    def optimize(self, layout):
        for box in layout.boxes:
            box.position[0] = box.position[0] + 100

        return layout

    def get_objective_value(self, layout):
        return self.specification.objective.function(layout)

class OCSOptimization(Optimization):
    max_iteration = 10
    max_cycle_of_learning = 10
    minimum_difference = 20

    def __init__(self, specification):
        Optimization.__init__(self, specification)
        self.organizational_rulesets = []

    # optimization はlayoutとかboxを使わない一般化をしたほうがいい
    def optimize(self, layout):

        best_objective_value = 0

        # use organizational rulesets for default rulesets
        layout.set_rulesets(self.organizational_rulesets)

        for i in range(OCSOptimization.max_iteration):
            step = 1

            #解が収束していない間回す
            while abs(old_objective_value - new_objective_value) < MAOptimization.minimum_difference : 

                old_objective_value = self.get_objective_value(layout)

                layout.generate_rules()
                Agent.exchage_rule_randomly(layout.boxes)

                new_objective_value = self.get_objective_value(layout)

            # learn and adjust a strength of each rule
            self.reinforcement_learning(layout)

            # in case this objective value exceeds the best value so far
            if self.get_objective_value(layout) > best_objective_value:

                # update the best objective value
                best_objective_value = self.get_objective_value(layout)

                # update organizational ruleset
                self.organizational_rulesets = layout.get_rulesets()

    def reinforcement_learning(self, layout):
        for box in layout.boxes:
            self.learn_strength_with_q_learning(box, layout)

    def learn_strength_with_q_learning(self, box, layout):

        for i in range(OCSOptimization.max_cycle_of_learning):
            
            episode = 0

            while true:
                selected_rule = box.rule_select()

                previous_value = self.get_objective_value(layout)
                box.execute_action(selected_rule.action)
                current_value = self.get_objective_value(layout)
                situation_after = Situation(layout.get_copy(), box)

                episode += 1

                if self.positive_reward_or_not(layout):
                    selected_rule.strength = selected_rule.strength + 0.1
                else:
                    selected_rule.strength = selected_rule.strength - 0.1

    def positive_reward_or_not(self, current_value, best_value, worst_value, previous_value):
        def _compare_with_before():
            return (previous_value < current_value)

        return _compare_with_before()

class SampleOptimization(Optimization):
    def __init__(self, specification):
        Optimization.__init__(self, specification)

