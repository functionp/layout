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

    def get_rulesets(self, layout):
        return layout.get_rulesets

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

            # repeat while ruleset is not converged(while new rule is generated)
            rule_generated_or_not = True
            while rule_generated_or_not == True : 
                rule_generated_or_not = layout.generate_rules()
                Agent.exchage_rule_randomly(layout.boxes)

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
            self.learn_strength_with_profit_sharing(box, layout)

    def learn_strength_with_profit_sharing(self, box, layout):

        for i in range(OCSOptimization.max_cycle_of_learning):
            
            episode = 0

            #次にやること：bestとworstの表現→インスタンスに保持？

            #とりあえず終了状態ベースでなく関数の収束ベースで終了条件考えてるけど状態で考えなくていいのだろうか？→脳内実行
            while abs(previous_value - current_value) > OCSOptimization.minimum_difference:
                selected_rule = box.rule_select()

                # apply selected rule, and record objective values before and after execution
                previous_value = self.get_objective_value(layout)
                box.execute_action(selected_rule.action)
                current_value = self.get_objective_value(layout)
                situation_after = Situation(layout.get_copy(), box)

                # rememebr applied rule with episode(time)
                pair_of_episode_and_rule = {'episode':episode, 'rule':selected_rule}
                applied_pairs.append(pair_of_episode_and_rule)

                episode += 1

                if self.positive_reward_or_not(current_value, previous_value, best_value, worst_value):
                    positive_reward_function = (lambda x: 0.1)
                    self.give_rewards(applied_pairs, positive_reward_function)

                else:
                    negative_reward_function = (lambda x: -0.1)
                    self.give_rewards(applied_pairs, negative_reward_function)

    def positive_reward_or_not(self, current_value, previous_value, best_value, worst_value):
        def _compare_with_before():
            return (previous_value < current_value)

        return _compare_with_before()

    # give rewards to serial rules at one time
    def give_rewards(self, pairs, reward_function):
        for pair in pairs:
            rule = pair['rule']
            episode = pair['episode']
            rule.reinforce(episode, reward_function)

class SampleOptimization(Optimization):
    def __init__(self, specification):
        Optimization.__init__(self, specification)

