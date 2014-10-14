#-*- coding: utf-8 -*-

# imports - - - - - - -
from layout import *

class Optimization():

    def __init__(self, specification):
        self.specification = specification
        self.reset_record()

    def optimize(self):
        pass

    def reset_record(self):
        self.best_value = 0
        self.worst_value = 0

    def get_objective_value(self):
        return self.specification.objective.function(self.layout)

    def get_rulesets(self):
        return self.layout.get_rulesets()

    # update best objective value if gained new value is better(smaller) than the best value
    # if updated, return True
    def update_best_value(self, new_value):
        if new_value < self.best_value:
            self.best_value = new_value
            return True
        else: 
            return False

    # update worst objective value if gained new value is worse(bigger) than the worst value
    # if updated, return True
    def update_worst_value(self, new_value):
        
        #ブールとその時の処理を渡して同じ処理をする高階関数に治せる
        if self.worst_value < new_value:
            self.worst_value = new_value
            return True
        else: 
            return False

class OCSOptimization(Optimization):
    max_iteration = 10
    max_cycle_of_learning = 10
    minimum_difference = 20

    def __init__(self, specification, layout=Layout()):
        Optimization.__init__(self, specification)
        self.organizational_rulesets = []
        self.layout = layout.get_copy()

    # optimization はlayoutとかboxを使わない一般化をしたほうがいい
    def optimize(self):
        layout = self.layout

        # use organizational rulesets for default rulesets
        layout.set_rulesets(self.organizational_rulesets)

        for i in range(OCSOptimization.max_iteration):
            step = 1

            # repeat while ruleset is not converged(while new rule is generated)
            rule_generated_or_not = True
            while rule_generated_or_not == True : 
                rule_generated_or_not = layout.generate_rules()
                Agent.exchage_rule_randomly(layout.boxes)

            # learn and adjust a strength of each rule
            self.reinforcement_learning()

            current_objective_value = self.get_objective_value()
            self.update_worst_value(current_objective_value)
            self.update_organizational_rulesets(current_objective_value)
            

    def update_organizational_rulesets(self, new_value):

        if self.update_best_value(new_value):

            # update organizational ruleset
            self.organizational_rulesets = self.layout.get_rulesets()
            return True
        else:
            return False

    def reinforcement_learning(self):
        for box in self.layout.boxes:
            self.learn_strength_with_profit_sharing(box)

    def learn_strength_with_profit_sharing(self, box):

        layout = self.layout

        for i in range(OCSOptimization.max_cycle_of_learning):
            
            episode = 0

            #次にやること：bestとworstの表現→インスタンスに保持？layoutとboxを使わない一般化

            #とりあえず終了状態ベースでなく関数の収束ベースで終了条件考えてるけど状態で考えなくていいのだろうか？→脳内実行
            while abs(previous_value - current_value) > OCSOptimization.minimum_difference:
                selected_rule = box.rule_select()

                # apply selected rule, and record objective values before and after execution
                previous_value = self.get_objective_value()
                box.execute_action(selected_rule.action)
                current_value = self.get_objective_value()
                situation_after = Situation(layout.get_copy(), box)

                # rememebr applied rule with episode(time)
                pair_of_episode_and_rule = {'episode':episode, 'rule':selected_rule}
                applied_pairs.append(pair_of_episode_and_rule)

                episode += 1

                if self.positive_reward_or_not(current_value, previous_value):
                    positive_reward_function = (lambda x: 0.1)
                    self.give_rewards(applied_pairs, positive_reward_function)

                else:
                    negative_reward_function = (lambda x: -0.1)
                    self.give_rewards(applied_pairs, negative_reward_function)

    def positive_reward_or_not(self, current_value, previous_value):
        half_value = (self.worst_value + self.best_value) / 2

        def _compare_with_before():
            return (previous_value < current_value)

        def _compare_with_half():
            return (half_value < current_value)

        return _compare_with_half()

    # give rewards to serial rules at one time
    def give_rewards(self, pairs, reward_function):
        for pair in pairs:
            rule = pair['rule']
            episode = pair['episode']
            rule.reinforce(episode, reward_function)

class SampleOptimization(Optimization):
    def __init__(self, specification):
        Optimization.__init__(self, specification)


