#-*- coding: utf-8 -*-

# imports - - - - - - -
from layout import *

# a high order function which updates given value and return True if updated.
def update_something(bool_condition, process):
    if bool_condition:
        process()
        return True
    else:
        return False


class Optimization():

    def __init__(self, specification, agent_set):
        self.specification = specification
        self.agent_set = agent_set.get_copy()
        self.reset_record()

    def optimize(self):
        pass

    def reset_record(self):
        self.set_best_value(100000)
        self.set_worst_value(0)

    def get_objective_value(self):
        return self.specification.objective.function(self.agent_set)

    def get_rulesets(self):
        return self.agent_set.get_rulesets()

    def set_best_value(self, value):
        self.best_value = value

    def set_worst_value(self, value):
        self.worst_value = value

    # update best objective value if gained new value is better(smaller) than the best value
    # if updated, return True
    def update_best_value(self, new_value):
        update_something((new_value < self.best_value), (lambda : self.set_best_value(new_value)))

    # update worst objective value if gained new value is worse(bigger) than the worst value
    # if updated, return True
    def update_worst_value(self, new_value):
        update_something((self.worst_value < new_value), (lambda : self.set_worst_value(new_value)))

class OCSOptimization(Optimization):
    max_iteration = 10
    max_cycle_of_learning = 5
    minimum_difference = 20

    def __init__(self, specification, agent_set=AgentSet()):
        Optimization.__init__(self, specification, agent_set)
        self.organizational_rulesets = []

    def set_organizational_rulesets(self, rulesets):
        self.organizational_rulesets = rulesets

    def optimize(self):
        agent_set = self.agent_set

        # use organizational rulesets for default rulesets
        agent_set.set_rulesets(self.organizational_rulesets)

        for i in range(OCSOptimization.max_iteration):
            step = 1

            # repeat while ruleset is not converged(while new rule is generated)
            rule_generated_or_not = True
            while rule_generated_or_not == True : 
                rule_generated_or_not = agent_set.generate_rules()
                Agent.exchange_rule_randomly(agent_set.agents)

            # learn and adjust a strength of each rule
            self.reinforcement_learning()

            current_objective_value = self.get_objective_value()
            self.update_worst_value(current_objective_value)
            self.update_organizational_rulesets(current_objective_value)

            self.display_status()


    #update objective value if it is the best, and record the rulesets
    def update_organizational_rulesets(self, new_value):
        new_rulesets = self.agent_set.get_rulesets()
        update_something(self.update_best_value(new_value), (lambda : self.set_organizational_rulesets(new_rulesets)))

    def reinforcement_learning(self):
        for agent in self.agent_set.agents:
            self.learn_strength_with_profit_sharing(agent)

    def learn_strength_with_profit_sharing(self, agent):

        agent_set = self.agent_set

        #てか収束してんだから繰り返しても意味ないのでは？
        for i in range(OCSOptimization.max_cycle_of_learning):
            
            episode = 1
            applied_pairs = []

            current_value = self.get_objective_value()
            previous_value = 10000

            #とりあえず終了状態ベースでなく関数の収束ベースで終了条件考えてるけど状態で考えなくていいのだろうか？→脳内実行
            while abs(previous_value - current_value) > OCSOptimization.minimum_difference :
                selected_rule = agent.rule_select()

                # apply selected rule, and record objective values before and after execution
                previous_value = self.get_objective_value()

                # do not execute too weak rule
                if selected_rule.strength > 0.001:
                    agent.execute_action(selected_rule.action)

                current_value = self.get_objective_value()
                situation_after = Situation(agent_set.get_copy(), agent)


                # rememebr applied rule with episode(time)
                pair_of_episode_and_rule = {'episode':episode, 'rule':selected_rule}
                applied_pairs.append(pair_of_episode_and_rule)

                episode += 1

                self.reward_process(current_value, previous_value, applied_pairs)

    def reward_process(self, current_value, previous_value, applied_pairs):
        if self.positive_reward_or_not(current_value, previous_value):
            positive_reward_function = (lambda x: 0.05)
            #positive_reward_function = (lambda x: (0.1)**x)
            self.give_rewards(applied_pairs, positive_reward_function)

        else:
            negative_reward_function = (lambda x: -0.05)
            #negative_reward_function = (lambda x: -(0.1)**x)
            self.give_rewards(applied_pairs, negative_reward_function)

    # return True if positive reward is given, otherwise return False
    def positive_reward_or_not(self, current_value, previous_value):
        half_value = (self.worst_value + self.best_value) / 2

        def compare_with_before():
            return (previous_value > current_value)

        def compare_with_half():
            return (half_value > current_value)

        return compare_with_before()

    # give rewards to serial rules at one time
    def give_rewards(self, pairs, reward_function):
        for pair in pairs:
            rule = pair['rule']
            episode = pair['episode']
            rule.reinforce(episode, reward_function)

    def display_status(self):

        print "============================================="
        print "Best Value so far: " + str(self.best_value)
        print "Worst Value so far: " + str(self.worst_value)
        print "Current Value so far: " + str(self.get_objective_value())
        agents = self.agent_set.agents
        
        for i,agent in enumerate(agents):
            print "Agent Number " + str(i)
            ruleset = agent.get_sorted_ruleset()

            for rule_i, rule in enumerate(ruleset):
                print "  Rule Number " + str(rule_i) + ": " + str(rule.strength)
                #print rule.condition.condfuns

            print ""

class SampleOptimization(Optimization):
    def __init__(self, specification):
        Optimization.__init__(self, specification)


# imports - - - - - - -
from condition import *
