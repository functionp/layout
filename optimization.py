#-*- coding: utf-8 -*-

# imports - - - - - - -
from layout import *
import random
import time

def update_something(bool_condition, process):
    """A high order function which updates given value and return True if updated."""

    if bool_condition:
        process()
        return True
    else:
        return False

class Optimization():

    def __init__(self, agent_set):
        self.agent_set = agent_set#agent_set.get_copy()
        self.reset_record()

    def optimize(self):
        pass

    def set_render_function(self, render_function):
        self.render_function = render_function

    def render(self):
        self.render_function()

    def reset_record(self):
        self.set_best_value(100000)
        self.set_worst_value(0)

    def get_whole_constraints_satisfied_or_not(self):
        constraints = self.agent_set.condition
        situation = Situation(agent_set=self.agent_set.get_copy()) 
        return constraints.evaluate(situation)

    def get_agent_constraints_satisfied_or_not(self):
        situation = Situation(agent_set=self.agent_set.get_copy()) 
        return situation.agent_set.evaluate_agent_constraint()

    def get_best_value_now_or_not(self):
        return abs(self.best_value - self.get_objective_value()) < OCSOptimization.minimum_difference

    def get_objective_function(self):
        return self.agent_set.condition.get_sum_of_constraint_objective

    def get_objective_value(self):
        objective_funtion = self.get_objective_function()
        situation = Situation(agent_set=self.agent_set)
        return objective_funtion(situation)

    def get_rulesets(self):
        return self.agent_set.get_rulesets()

    def set_best_value(self, value):
        self.best_value = value

    def set_worst_value(self, value):
        self.worst_value = value

    def update_best_value(self, new_value):
        """Update best objective value if gained new value is better(smaller) than the best value. If updated, return True. """
        update_something((new_value < self.best_value), (lambda : self.set_best_value(new_value)))

    def update_worst_value(self, new_value):
        """Update worst objective value if gained new value is worse(bigger) than the worst value. If updated, return True."""
        update_something((self.worst_value < new_value), (lambda : self.set_worst_value(new_value)))

    def clear_output_file(self, filename):
        file = open(filename, 'w')
        file.write("")
        file.close

    def output_obvective_values(self, filename):

        constraints = self.agent_set.condition
        situation = Situation(agent_set=self.agent_set.get_copy())

        output_line = ""
        output_line += str(constraints.get_sum_of_constraint_objective(situation)) + ","

        agents = self.agent_set.agents
        for i,agent in enumerate(agents):
            situation_with_agent = Situation(agent_set=self.agent_set.get_copy(), agent=agent.get_copy())
            output_line += str(agent.condition.get_sum_of_constraint_objective(situation_with_agent)) + ","

        output_line += "\n"
        
        file = open(filename, 'a')
        file.write(output_line)
        file.close()


class RandomOptimization(Optimization):

    max_trial = 1000

    def __init__(self, agent_set=AgentSet()):
        Optimization.__init__(self, agent_set)

    def optimize(self):
        
        base_box = self.agent_set.base_box
        grid_size = 10
        max_x_grid =  base_box.get_width() / grid_size
        max_y_grid =  base_box.get_height() / grid_size

        self.clear_output_file("output_data.csv")

        number_of_trial = 0
        total_cycle_duration = 0
        while True:
            start = time.time()
            constraints_satisfied = self.get_whole_constraints_satisfied_or_not() and self.get_agent_constraints_satisfied_or_not()
            reach_max_trial = self.max_trial < number_of_trial
            if constraints_satisfied or reach_max_trial: break

            self.render()

            for agent in self.agent_set.agents:
                agent.set_x(random.randint(0, max_x_grid) * grid_size)
                agent.set_y(random.randint(0, max_y_grid) * grid_size)

                max_width_grid =  (base_box.get_width() - agent.get_x()) / grid_size
                max_height_grid =  (base_box.get_height() - agent.get_y()) / grid_size
                agent.set_width(random.randint(0, max_width_grid) * grid_size)
                agent.set_height(random.randint(0, max_height_grid) * grid_size)

            self.output_obvective_values("output_data.csv")

            number_of_trial += 1
            total_cycle_duration += time.time() - start

        average_cycle_duration = total_cycle_duration / number_of_trial
        print average_cycle_duration

class OCSOptimization(Optimization):
    minimum_iteration = 1
    max_cycle_of_learning = 1
    minimum_difference = 20

    def __init__(self, agent_set=AgentSet()):
        Optimization.__init__(self, agent_set)
        self.organizational_rulesets = []

    def get_half_value(self):
        return (self.worst_value + self.best_value) / 2

    def set_organizational_rulesets(self, rulesets):
        self.organizational_rulesets = rulesets

    def optimize(self):
        # use organizational rulesets for default rulesets
        self.agent_set.set_rulesets(self.organizational_rulesets)
        print self.organizational_rulesets

        constraints = self.agent_set.condition
        situation = Situation(agent_set=self.agent_set.get_copy()) 

        self.clear_output_file("output_data.csv")

        # Termination condition for whole optimization: satisfaction of all hard constraints, best_value
        number_of_trial = 0
        total_cycle_duration = 0
        while True:
            start = time.time()
            constraints_satisfied = self.get_whole_constraints_satisfied_or_not() and self.get_agent_constraints_satisfied_or_not()
            best_value_now = True #self.get_best_value_now_or_not()
            iteration_finished = inumber_of_trial > OCSOptimization.minimum_iteration

            if constraints_satisfied and best_value_now and iteration_finished: break

            #self.display_break_condition()

            self.one_optimization_cycle()
            number_of_trial += 1
            total_cycle_duration += time.time() - start

        average_cycle_duration = total_cycle_duration / number_of_trial
        print average_cycle_duration

        self.output_obvective_values("output_data.csv")
        
    def one_optimization_cycle(self):

        # repeat while ruleset is not converged(while new rule is generated)
        rule_not_found_or_not = True
        while rule_not_found_or_not == True:
            rule_not_found_or_not, rule_generated_or_not = self.agent_set.generate_rules() 
            #Agent.exchange_rule_randomly(self.agent_set.agents) 

        #self.display_status()

        self.output_obvective_values("output_data.csv")

        # learn and adjust a strength of each rule
        self.reinforcement_learning()

        self.render()

        current_objective_value = self.get_objective_value()
        self.update_worst_value(current_objective_value)
        self.update_organizational_rulesets(current_objective_value)

        self.agent_set.delete_weak_rules()

        #self.display_status()

    def update_organizational_rulesets(self, new_value):
        """update objective value if it is the best, and record the rulesets"""

        new_rulesets = self.agent_set.get_rulesets()
        #update_something(self.update_best_value(new_value), (lambda : self.set_organizational_rulesets(new_rulesets))) #とにかく毎週記録してれば終了時のルールはゲットできる
        self.set_organizational_rulesets(new_rulesets)

    def reinforcement_learning(self):
        for agent in self.agent_set.agents:
            self.learn_strength_with_profit_sharing(agent)

    def learn_strength_with_profit_sharing(self, agent):

        agent_set = self.agent_set

        for i in range(OCSOptimization.max_cycle_of_learning):

            episode = 1
            applied_pairs = []

            current_value = self.get_objective_value()
            previous_value = 10000

            constraints = self.agent_set.condition
            situation = Situation(agent_set=agent_set.get_copy(), agent=agent) 

            while True:
                converged = abs(previous_value - current_value) < OCSOptimization.minimum_difference
                whole_constraints_satisfied = self.get_whole_constraints_satisfied_or_not() 
                best_value_now = self.get_best_value_now_or_not()

                if converged and whole_constraints_satisfied and best_value_now : break
                #if converged: break #ここの条件ゆるめただけで強度がガン上がり

                selected_rule = agent.rule_select()

                # skip too weak rule (to avoid infinite loop)
                if selected_rule.strength < 0.001: break

                # record objective value, constraint satisfaction before execution
                previous_situation = situation.get_copy()
                previous_value = self.get_objective_value()

                agent.execute_action(selected_rule.action)

                current_value = self.get_objective_value()
                situation = Situation(agent_set=agent_set.get_copy(), agent=agent.get_copy())

                # rememebr applied rule with episode(time)
                pair_of_episode_and_rule = {'episode':episode, 'rule':selected_rule}
                applied_pairs.append(pair_of_episode_and_rule)

                episode += 1
                #self.display_status()

                self.reward_process(situation, previous_situation, applied_pairs)

    def reward_process(self, present_situation, previous_situation, applied_pairs):

        fixed_value = (lambda x: 0.5)
        decreasing_function = (lambda x: (0.1)**x)

        if self.positive_reward_or_not(present_situation, previous_situation):
            reward_function = (lambda x: fixed_value(x))
        else:
            reward_function = (lambda x: -1 * fixed_value(x))

        self.give_rewards(applied_pairs, reward_function)

    def positive_reward_or_not(self, present_situation, previous_situation):
        """return True if positive reward is to be given, otherwise return False"""

        whole_constraints = self.agent_set.condition
        agent_constraints = previous_situation.agent.condition

        previous_value = self.get_objective_function()(previous_situation)
        previous_whole_constraints_objective = whole_constraints.get_sum_of_constraint_objective(previous_situation)
        previous_agent_constraints_objective = agent_constraints.get_sum_of_constraint_objective(previous_situation)

        current_value = self.get_objective_value()
        half_value = self.get_half_value()
        whole_constraints_objective = whole_constraints.get_sum_of_constraint_objective(present_situation)
        agent_constraints_objective = agent_constraints.get_sum_of_constraint_objective(present_situation)

        compare_with_half = (half_value > current_value)
        compare_with_before = (previous_value > current_value)

        difference_whole = previous_whole_constraints_objective - whole_constraints_objective 
        difference_agent = previous_agent_constraints_objective - agent_constraints_objective

        #best_now =  whole_constraints_objective == 0 and agent_constraints_objective == 0 #もう満たしている状態になってるのにあえて変えちゃうってことあるのでは？

        improve_total_objective = difference_whole + difference_agent > 0
        improve_either_one = difference_whole > 0 or difference_agent > 0 

        return improve_either_one

    def give_rewards(self, pairs, reward_function):
        """give rewards to serial rules at one time"""

        for pair in pairs:
            rule = pair['rule']
            episode = pair['episode']
            rule.reinforce(episode, reward_function)

    def display_break_condition(self):

        constraints = self.agent_set.condition
        situation = Situation(agent_set=self.agent_set.get_copy()) 

        print "---------------------------------------------"
        print "Whole Constraints: " + str(self.get_whole_constraints_satisfied_or_not())
        print "   Whole Objective:  " + str(constraints.get_sum_of_constraint_objective(situation))
        print "Agent Constraints: " + str(self.get_agent_constraints_satisfied_or_not())
        agents = self.agent_set.agents

        for i,agent in enumerate(agents):
            situation_with_agent = Situation(agent_set=self.agent_set.get_copy(), agent=agent.get_copy())
            print "   Agent Number " + str(i) + ": " + str(agent.condition.evaluate(situation_with_agent))
            print "       Objective:  " + str(agent.condition.get_sum_of_constraint_objective(situation_with_agent))

        print "Best Value now:" + str(self.get_best_value_now_or_not())
        print "Best Value: " + str(self.best_value)
        print "Current Value: " + str(self.get_objective_value())

    def display_status(self):

        print "============================================="
        print "Best Value so far: " + str(self.best_value)
        print "Worst Value so far: " + str(self.worst_value)
        print "Current Value: " + str(self.get_objective_value())
        print ""
        agents = self.agent_set.agents
        
        for i,agent in enumerate(agents):
            print "Agent Number " + str(i)
            ruleset = agent.get_sorted_ruleset()

            for rule_i, rule in enumerate(ruleset):
                print "  Rule Number " + str(rule_i) + ": " + str(rule.strength)
                print [condfun.function for condfun in rule.condition.condfuns]
                print rule.action

            print ""

# imports - - - - - - -
from condition import *
