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

class MAOptimization(Optimization):
    max_iteration = 10
    minimum_difference = 20

    def __init__(self, specification):
        Optimization.__init__(self, specification)
        self.organizational_rulesets = []

    def optimize(self, layout):

        best_objective_value = 0

        # use organizational rulesets for default rulesets
        layout.set_rulesets(self.organizational_rulesets)

        for i in range(MAOptimization.max_iteration):
            step = 1

            #解が収束していない間回す
            while abs(old_objective_value - new_objective_value) < MAOptimization.minimum_difference : 

                old_objective_value = self.get_objective_value(layout)

                layout.generate_and_apply_rules()
                Agent.exchage_rule_randomly(layout.boxes)

                new_objective_value = self.get_objective_value(layout)

            #ルール改変

            # in case this objective value exceeds the best value so far
            if self.get_objective_value(layout) > best_objective_value:

                # update the best objective value
                best_objective_value = self.get_objective_value(layout)

                # update organizational ruleset
                self.organizational_rulesets = layout.get_rulesets()



class SampleOptimization(Optimization):
    def __init__(self, specification):
        Optimization.__init__(self, specification)

