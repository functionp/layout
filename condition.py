#-*- coding: utf-8 -*-


class Situation():
    def __init__(self, **kwargs):
        self.agent_set = kwargs.get('agent_set', None)
        self.agent = kwargs.get('agent', None)

    def get_copy(self):
        return Situation(agent_set=self.agent_set.get_copy(), agent=self.agent.get_copy())


# return True if relation between given box and any box in given layout satisfies the given bool function
def bool_for_layout_and_box(agent_set, agent, bool_function):

    agents = agent_set.agents[:]

    #ignore exception
    try:
        agents.remove(agent)
    except:
        pass

    result = False
    for i in range(len(agents)):
        if bool_function(agent, agents[i]) == True:
            result = True
            break

    return result

class Condition():
    # we call function which reperesents one condition  as "condfun"
    def __init__(self, condfuns=[], and_or=1):
        self.condfuns = condfuns
        self.and_or = and_or

    # evaluate the condition with given situation and return True or False
    def evaluate(self, situation):

        if self.condfuns != []:
            results = [condfun.evaluate_function(situation) for condfun in self.condfuns]

            # case of "and"
            if self.and_or == 1:
                return reduce(lambda b1,b2: b1 and b2, results)
            else:
                return reduce(lambda b1,b2: b1 or b2, results)
        else:
            return True

    def get_copy(self):
        return Condition(self.condfuns[:], self.and_or)

    def get_size(self):
        return len(self.condfuns)

    def get_sum_of_constraint_objective(self, situation):
        objective_value_list = [condfun.get_objective_value(situation) for condfun in self.condfuns]
        return reduce((lambda x, y: x+y), objective_value_list)

    def add_condfun(self, condfun):
        self.condfuns.append(condfun)

    def remove_random_condfun(self):
        index = random.randint(0, len(self.condfuns) - 1)
        self.remove_condfun(index)

    def remove_condfun(self, index):
        del(self.condfuns[index])

    @classmethod
    # make Condition instance which represents given situation(layout and box)
    def make_condition(cls, situation):
        #in_the_edgeだけってケースが多いのでコンディション増やしたら変わってくるかも
        condfun_candidates = [BoxCondFun.in_the_edge(), 
                              BoxCondFun.having_box_in_given_distance(100), 
                              BoxCondFun.having_box_in_given_distance(200), 
                              BoxCondFun.having_box_in_given_distance(400), 
                              BoxCondFun.keeping_given_distance_from_box(300), 
                              BoxCondFun.having_overlapped_box()]

        # extract which matches given state(layout and box)
        matched_condfuns = [condfun for condfun in condfun_candidates if condfun.evaluate_function(situation) == True]

        and_or = 1 # represents "and"
        condition = Condition(matched_condfuns, and_or)

        # remove if condition has a lot of condfuns (loosening condition)
        if 3 < condition.get_size():
            condition.remove_random_condfun()

        return condition

        # # # CONDFUNS # # #

    @classmethod
    def minimum_member(cls, number):
        def _minimum_member(situation):
            agent_set = situation.agent_set

            if agent_set.get_number_of_boxes() >= number:
                return True
            else:
                return False

        return _minimum_member



class BoxCondition(Condition):
    pass

class CondFun():
    def __init__(self, function, objective=None):

        # to avoid import error, avoid to use initial value
        if objective == None: objective = Objective()

        self.set_function(function)
        self.set_objective(objective)

    def set_function(self, function):
        self.function = function

    def set_objective(self, objective):
        self.objective = objective

    def get_objective_value(self, situation):
        return self.objective.function(situation)

    def evaluate_function(self, situation):
        return self.function(situation)

class BoxCondFun(CondFun):
    def __init__(self, function, objective=(lambda x: 0)):
        CondFun.__init__(self, function, objective)

    # # # CONDFUNS # # #

    @classmethod
    def width_constraint(cls, lower_limit, upper_limit=10000):
        def _width_constraint(situation):
            box = situation.agent
            return lower_limit <= box.get_width() and box.get_width() <= upper_limit

        def _width_constraint_objective(situation):
            box = situation.agent
            if box.get_width() < lower_limit:
                return abs(lower_limit - box.get_width())
            elif upper_limit < box.get_width():
                return abs(box.get_width() - upper_limit)
            else:
                return 0

        return CondFun(_width_constraint, Objective(1, _width_constraint_objective))

    @classmethod
    def height_constraint(cls, lower_limit, upper_limit=10000):
        def _height_constraint(situation):
            box = situation.agent
            return lower_limit <= box.get_height() and box.get_height() <= upper_limit

        def _height_constraint_objective(situation):
            box = situation.agent
            if box.get_height() < lower_limit:
                return abs(lower_limit - box.get_height())
            elif upper_limit < box.get_height():
                return abs(box.get_height() - upper_limit)
            else:
                return 0

        return CondFun(_height_constraint, Objective(1, _height_constraint_objective))

    @classmethod
    def x_constraint(cls, lower_limit, upper_limit=10000):
        def _x_constraint(situation):
            box = situation.agent
            return lower_limit <= box.get_x() and box.get_x() <= upper_limit

        def _x_constraint_objective(situation):
            box = situation.agent
            if box.get_x() < lower_limit:
                return abs(lower_limit - box.get_x())
            elif upper_limit < box.get_x():
                return abs(box.get_x() - upper_limit)
            else:
                return 0

        return CondFun(_x_constraint, Objective(1, _x_constraint_objective))

    @classmethod
    def y_constraint(cls, lower_limit, upper_limit=10000):
        def _y_constraint(situation):
            box = situation.agent
            return lower_limit <= box.get_y() and box.get_y() <= upper_limit

        def _y_constraint_objective(situation):
            box = situation.agent
            if box.get_y() < lower_limit:
                return abs(lower_limit - box.get_y())
            elif upper_limit < box.get_y():
                return abs(box.get_y() - upper_limit)
            else:
                return 0

        return CondFun(_y_constraint, Objective(1, _y_constraint_objective))

    @classmethod
    def in_the_edge(cls):
        def _in_the_edge(situation):
            layout = situation.agent_set
            boxes = layout.agents

            result = True
            for box in boxes:
                if box.off_the_edge_or_not() == True:
                    result = False
                    break

            return result

        return CondFun(_in_the_edge)

    @classmethod
    def no_overlap(cls):
        def _no_overlap(situation):
            layout = situation.agent_set

            boxes = layout.agents
            result = True
            for i in range(len(boxes) - 1):
                for j in range(i+1, len(boxes)):
                    if BoxAgent.overlap_or_not(boxes[i], boxes[j]) == True:
                        result = False
                        break

            return result

        return CondFun(_no_overlap, Objective(1, Objective.sum_of_overlapped_area))

    @classmethod
    def all_aligned(cls):
        # return False if box which does not align to any box exists, otherwise True
        def _all_aligned(situation):
            layout = situation.agent_set
            boxes = layout.agents

            list_of_number_of_aligned_box = []
            for i in range(len(boxes)):

                number_of_aligned_box = 0
                for j in range(len(boxes)):
                    if BoxAgent.aligned_or_not(boxes[i], boxes[j]) == True:
                        number_of_aligned_box += 1

                # minus 1 because every box aligned to the box itself
                list_of_number_of_aligned_box.append(number_of_aligned_box - 1)

            list_of_having_aligned_box_or_not = map((lambda x: x >= 1), list_of_number_of_aligned_box)

            # return True only if all the element is True
            return reduce((lambda b1,b2: b1 and b2), list_of_having_aligned_box_or_not)

        return CondFun(_all_aligned)

    @classmethod
    def having_box_in_given_distance(cls, distance):
        def _having_box_in_given_distance(situation):
            layout = situation.agent_set
            box = situation.agent

            bool_function = (lambda box1, box2: BoxAgent.get_gravity_distance(box1, box2) < distance)

            return bool_for_layout_and_box(layout, box, bool_function)

        return CondFun(_having_box_in_given_distance)

    @classmethod
    def keeping_given_distance_from_box(cls, distance):
        condfun = BoxCondFun.having_box_in_given_distance(distance)
        return CondFun((lambda situation: not condfun.evaluate_function(situation)))

    @classmethod
    def having_overlapped_box(cls):
        def _having_overlapped_box(situation):
            layout = situation.agent_set
            box = situation.agent

            bool_function = BoxAgent.overlap_or_not

            return bool_for_layout_and_box(layout, box, bool_function)

        return CondFun(_having_overlapped_box)

# imports - - - - - - -
from layout import *
from rule import *
from agent import *
from specification import *
import random
