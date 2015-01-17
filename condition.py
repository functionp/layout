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
    def evaluate(self, situation, latitude=0):

        if self.condfuns != []:
            results = [condfun.evaluate_function(situation) for condfun in self.condfuns]
            number_of_true = reduce(lambda a,b: a + b, results) # Bool value is calculatable (True = 1, False = 0)
            number_of_false = len(results) - number_of_true

            # case of "and"
            if self.and_or == 1:
                return number_of_false <= latitude
            else:
                return number_of_true >= 1
        else:
            return True

    def get_copy(self):
        return Condition(self.condfuns[:], self.and_or)

    def get_size(self):
        return len(self.condfuns)

    def get_sum_of_constraint_objective(self, situation):
        objective_value_list = [condfun.get_objective_value(situation) for condfun in self.condfuns]
        #print objective_value_list

        if len(objective_value_list) == 0:
            return 0
        elif len(objective_value_list) == 1:
            return objective_value_list[0]
        else:
            return reduce((lambda x, y: x+y), objective_value_list)

    def add_condfun(self, condfun):
        self.condfuns.append(condfun)

    def remove_condfun_by_name(self, name):
        for i, condfun in enumerate(self.condfuns):
            if condfun.function.__name__ == name:
                self.remove_condfun(i)
                break

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
                              BoxCondFun.width_constraint(0,25),
                              BoxCondFun.width_constraint(26,50),
                              BoxCondFun.width_constraint(51,75),
                              BoxCondFun.width_constraint(76,100),
                              BoxCondFun.width_constraint(101,125),
                              BoxCondFun.width_constraint(126,150),
                              BoxCondFun.width_constraint(151,175),
                              BoxCondFun.width_constraint(176,200),
                              BoxCondFun.width_constraint(201,225),
                              BoxCondFun.width_constraint(226,250),
                              BoxCondFun.width_constraint(251,275),
                              BoxCondFun.width_constraint(276,300),
                              BoxCondFun.height_constraint(0,25),
                              BoxCondFun.height_constraint(26,50),
                              BoxCondFun.height_constraint(51,75),
                              BoxCondFun.height_constraint(76,100),
                              BoxCondFun.height_constraint(101,125),
                              BoxCondFun.height_constraint(126,150),
                              BoxCondFun.height_constraint(151,175),
                              BoxCondFun.height_constraint(176,200),
                              BoxCondFun.height_constraint(201,225),
                              BoxCondFun.height_constraint(226,250),
                              BoxCondFun.height_constraint(251,275),
                              BoxCondFun.height_constraint(276,300),
                              BoxCondFun.having_box_in_given_distance(100), 
                              BoxCondFun.having_box_in_given_distance(200), 
                              BoxCondFun.having_box_in_given_distance(400), 
                              BoxCondFun.keeping_given_distance_from_box(300), 
                              BoxCondFun.having_overlapped_box()]

        # add agent condition to candidate
        if situation.agent:
            condfun_candidates.extend(situation.agent.condition.condfuns)

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
    def __init__(self, function, objective=None, soft_hard=1):

        # to avoid import error, avoid to use initial value
        if objective == None: objective = Objective()

        self.set_function(function)
        self.set_objective(objective)
        self.set_soft_hard(soft_hard)

    def set_function(self, function):
        self.function = function

    def set_objective(self, objective):
        self.objective = objective
        
    def set_soft_hard(self, soft_hard):
        self.soft_hard = soft_hard

    def get_objective_value(self, situation):
        return self.objective.function(situation)

    def evaluate_function(self, situation):
        if self.soft_hard == 1:
            return self.function(situation)
        else:
            return True

class BoxCondFun(CondFun):
    def __init__(self, function, objective=(lambda x: 0)):
        CondFun.__init__(self, function, objective)

    # # # CONDFUNS # # #

    @classmethod
    def width_constraint(cls, lower_limit=None, upper_limit=None, soft_hard=1):

        if lower_limit == None: lower_limit = 0
        if upper_limit == None: upper_limit = 9999

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

        _width_constraint.func_dict['lower'] = lower_limit
        _width_constraint.func_dict['upper'] = upper_limit
        _width_constraint.func_dict['soft_hard'] = soft_hard

        return CondFun(_width_constraint, Objective(1, _width_constraint_objective), soft_hard)

    @classmethod
    def height_constraint(cls, lower_limit=None, upper_limit=None, soft_hard=1):

        if lower_limit == None: lower_limit = 0
        if upper_limit == None: upper_limit = 9999

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

        _height_constraint.func_dict['lower'] = lower_limit
        _height_constraint.func_dict['upper'] = upper_limit
        _height_constraint.func_dict['soft_hard'] = soft_hard

        return CondFun(_height_constraint, Objective(1, _height_constraint_objective), soft_hard)

    @classmethod
    def x_constraint(cls, lower_limit=None, upper_limit=None, soft_hard=1):

        if lower_limit == None: lower_limit = 0
        if upper_limit == None: upper_limit = 9999

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

        _x_constraint.func_dict['lower'] = lower_limit
        _x_constraint.func_dict['upper'] = upper_limit
        _x_constraint.func_dict['soft_hard'] = soft_hard

        return CondFun(_x_constraint, Objective(1, _x_constraint_objective), soft_hard)

    @classmethod
    def y_constraint(cls, lower_limit=None, upper_limit=None, soft_hard=1):

        if lower_limit == None: lower_limit = 0
        if upper_limit == None: upper_limit = 9999

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

        _y_constraint.func_dict['lower'] = lower_limit
        _y_constraint.func_dict['upper'] = upper_limit
        _y_constraint.func_dict['soft_hard'] = soft_hard

        return CondFun(_y_constraint, Objective(1, _y_constraint_objective), soft_hard)

    @classmethod
    def x_end_constraint(cls, lower_limit, upper_limit=9999, soft_hard=1):
        def _x_end_constraint(situation):
            box = situation.agent
            return lower_limit <= box.get_x() + box.get_width() and box.get_x() + box.get_width() <= upper_limit

        def _x_end_constraint_objective(situation):
            box = situation.agent
            if box.get_x() + box.get_width() < lower_limit:
                return abs(lower_limit - (box.get_x() + box.get_width()))
            elif upper_limit < box.get_x() + box.get_width():
                return abs((box.get_x() + box.get_width()) - upper_limit)
            else:
                return 0

        return CondFun(_x_end_constraint, Objective(1, _x_end_constraint_objective), soft_hard)

    @classmethod
    def y_end_constraint(cls, lower_limit, upper_limit=9999, soft_hard=1):
        def _y_end_constraint(situation):
            box = situation.agent
            return lower_limit <= box.get_y() + box.get_height() and box.get_y() + box.get_height() <= upper_limit

        def _y_end_constraint_objective(situation):
            box = situation.agent
            if box.get_y() + box.get_height() < lower_limit:
                return abs(lower_limit - (box.get_y() + box.get_height()))
            elif upper_limit < box.get_y():
                return abs((box.get_y() + box.get_height()) - upper_limit)
            else:
                return 0

        return CondFun(_y_end_constraint, Objective(1, _y_end_constraint_objective), soft_hard)

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

            if len(boxes) != 1:
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
            else:
                return True

        return CondFun(_all_aligned)

    @classmethod
    def width_unification(cls, soft_hard=1):
        def _width_unification(situation):
            layout = situation.agent_set
            boxes = layout.agents

            if len(boxes) == 1:
                return True
            else:
                width_equalities = [box.get_width() == boxes[0].get_width() for box in boxes]
                return reduce((lambda b1,b2: b1 and b2), width_equalities)

        return CondFun(_width_unification, Objective(1, Objective.width_difference), soft_hard)

    @classmethod
    def height_unification(cls, soft_hard=1):
        def _height_unification(situation):
            layout = situation.agent_set
            boxes = layout.agents

            if len(boxes) == 1:
                return True
            else:
                height_equalities = [box.get_height() == boxes[0].get_height() for box in boxes]
                return reduce((lambda b1,b2: b1 and b2), height_equalities)

        return CondFun(_height_unification, Objective(1, Objective.height_difference), soft_hard)

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
