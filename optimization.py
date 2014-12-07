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
        self.agent_set = agent_set#agent_set.get_copy()
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
    max_iteration = 30
    max_cycle_of_learning = 1
    minimum_difference = 20

    def __init__(self, specification, agent_set=AgentSet()):
        Optimization.__init__(self, specification, agent_set)
        self.organizational_rulesets = []

    def get_half_value(self):
        return (self.worst_value + self.best_value) / 2

    def set_organizational_rulesets(self, rulesets):
        self.organizational_rulesets = rulesets

    def optimize(self):
        # use organizational rulesets for default rulesets
        self.agent_set.set_rulesets(self.organizational_rulesets)

        constraints = self.specification.constraints
        situation = Situation(agent_set=self.agent_set.get_copy()) 

        #for i in range(OCSOptimization.max_iteration):

        #最適化全体の終了条件：所定の回数繰り返す　かつ　全体制約充足　かつ　全エージェントの個別制約充足
        i = 0
        constraints_not_satisfied = constraints.evaluate(situation) == False or situation.agent_set.evaluate_agent_constraint() == False
        while i < OCSOptimization.max_iteration or constraints_not_satisfied or abs(self.best_value - self.get_objective_value()) > OCSOptimization.minimum_difference:

            constraints_not_satisfied = constraints.evaluate(situation) == False or situation.agent_set.evaluate_agent_constraint() == False

            print "itera" + str(i < OCSOptimization.max_iteration)
            print "whole const" + str(constraints.evaluate(situation) == False)
            print "agent const" + str(situation.agent_set.evaluate_agent_constraint() == False)
            print self.best_value
            print self.get_objective_value()
            print "best" + str(abs(self.best_value - self.get_objective_value()) > OCSOptimization.minimum_difference)
            self.one_optimization_cycle()
            i += 1

    def one_optimization_cycle(self):
        # repeat while ruleset is not converged(while new rule is generated)
        rule_not_found_or_not = True
        while rule_not_found_or_not == True:
            rule_not_found_or_not, rule_generated_or_not = self.agent_set.generate_rules() 
            Agent.exchange_rule_randomly(self.agent_set.agents)
            
        self.display_status()

        # learn and adjust a strength of each rule
        self.reinforcement_learning()

        print "reinforce owatta"

        self.agent_set.delete_weak_rules()

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

            constraints = self.specification.constraints
            situation = Situation(agent_set=agent_set.get_copy(), agent=agent) 

            # repeat until objective converged and constraints are satisfied
            not_converged = abs(previous_value - current_value) > OCSOptimization.minimum_difference or abs(self.best_value - current_value) > OCSOptimization.minimum_difference
            while not_converged or constraints.evaluate(situation) == False:
                print "=-=-="
                print self.best_value
                print current_value
                selected_rule = agent.rule_select()

                # skip too weak rule (to avoid infinite loop)
                if selected_rule.strength < 0.001:
                    print "hoge"
                    break

                # apply selected rule, and record objective values before and after execution
                previous_value = self.get_objective_value()

                agent.execute_action(selected_rule.action)

                current_value = self.get_objective_value()
                situation = Situation(agent_set=agent_set.get_copy(), agent=agent)

                # rememebr applied rule with episode(time)
                pair_of_episode_and_rule = {'episode':episode, 'rule':selected_rule}
                applied_pairs.append(pair_of_episode_and_rule)

                #おそらく無限ループの原因はどんなアクションによっても体系が変化しない組み方になるから　制約がいつまでも解消されない→報酬減→削除→生成→無理
                print "episode" + str(episode)
                episode += 1

                self.reward_process(current_value, previous_value, applied_pairs)

    def reward_process(self, current_value, previous_value, applied_pairs):

        fixed_value = (lambda x: 0.05)
        decreasing_function = (lambda x: (0.1)**x)

        #報酬関数を減少関数にするとあっという間に強度が収束してデッドロックに陥る
        if self.positive_reward_or_not(current_value, previous_value):
            reward_function = (lambda x: fixed_value(x))
        else:
            reward_function = (lambda x: -1 * fixed_value(x))

        self.give_rewards(applied_pairs, reward_function)

    # return True if positive reward is to be given, otherwise return False
    def positive_reward_or_not(self, current_value, previous_value):
        half_value = self.get_half_value()

        def compare_with_before():
            return (previous_value > current_value)

        def compare_with_half():
            return (half_value > current_value)

        # do not give reward to the rule which does not satisfy the constraint
        def compare_with_before_and_satisfy():
            constraints = self.specification.constraints
            situation = Situation(agent_set=self.agent_set.get_copy()) 
            constraints_satisfied = constraints.evaluate(situation) == True and situation.agent_set.evaluate_agent_constraint()
            return constraints_satisfied and previous_value > current_value

        return compare_with_before_and_satisfy()

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
        print "Current Value: " + str(self.get_objective_value())
        agents = self.agent_set.agents
        
        for i,agent in enumerate(agents):
            print "Agent Number " + str(i)
            ruleset = agent.get_sorted_ruleset()

            for rule_i, rule in enumerate(ruleset):
                print "  Rule Number " + str(rule_i) + ": " + str(rule.strength)
                print rule.condition.condfuns
                print rule.action

            print ""

class SampleOptimization(Optimization):
    def __init__(self, specification):
        Optimization.__init__(self, specification)


# imports - - - - - - -
from condition import *
