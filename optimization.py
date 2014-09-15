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

    def __init__(self, specification):
        Optimization.__init__(self, specification)
        self.organizational_rulesets = []

    def optimize(self, layout):

        best_objective_value = 0

        for i in range(MAOptimization.max_iteration):
            step = 1

            #あとでネスト解除

            #解が収束していない間回す
            while true: 
                for box in layout.boxes:
                    box.ruleset = box.get_sorted_ruleset()
                    match_or_not = False 

                    #if present condition matches any rule of this box, apply(execute) that rule 
                    for rule in box.ruleset:
                        if rule.condition.evaluate(layout=layout, box=box):
                            box.execute_action(rule.action)
                            match_or_not = True
                            break

                    # if no rule is matched, make new rule
                    if match_or_not == False:
                        # make new rule with condition of present situation
                        new_rule = Rule.make_rule_with_random_action(Condition.make_condition(layout=layout, box=box))
                        box.add_rule(new_rule)

                Agent.exchage_rule_randomly(layout.boxes)

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

