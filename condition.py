#-*- coding: utf-8 -*-

class Situation():
    def __init__(self, agent_set, agent=None):
        self.agent_set = agent_set
        self.agent = agent

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
            results = [condfun(situation) for condfun in self.condfuns]

            # case of "and"
            if self.and_or == 1:
                return reduce(lambda b1,b2: b1 and b2, results)
            else:
                return reduce(lambda b1,b2: b1 or b2, results)
        else:
            return True

    def get_size(self):
        return len(self.condfuns)

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
        condfun_candidates = [BoxCondition.in_the_edge(), 
                              BoxCondition.having_box_in_given_distance(100), 
                              BoxCondition.having_box_in_given_distance(200), 
                              BoxCondition.having_box_in_given_distance(400), 
                              BoxCondition.keeping_given_distance_from_box(300), 
                              BoxCondition.having_overlapped_box()]

        # extract which matches given state(layout and box)
        matched_condfuns = [condfun for condfun in condfun_candidates if condfun(situation) == True]

        and_or = 1 # represents "and"
        condition = Condition(matched_condfuns, and_or)

        # remove if condition has a lot of condfuns (loosing condition)
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

    # # # CONDFUNS # # #

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

        return _in_the_edge

    @classmethod
    def no_overlap(cls):
        def _no_overlap(situation):
            layout = situation.agent_set

            boxes = layout.agents
            result = True
            for i in range(len(boxes)):
                for j in range(i+1, len(boxes)):
                    if BoxAgent.overlap_or_not(boxes[i], boxes[j]) == True:
                        result = False
                        break

            return result

        return _no_overlap

    @classmethod
    def having_box_in_given_distance(cls, distance):
        def _having_box_in_given_distance(situation):
            layout = situation.agent_set
            box = situation.agent

            bool_function = (lambda box1, box2: BoxAgent.get_gravity_distance(box1, box2) < distance)

            return bool_for_layout_and_box(layout, box, bool_function)

        return _having_box_in_given_distance

    @classmethod
    def keeping_given_distance_from_box(cls, distance):
        f = BoxCondition.having_box_in_given_distance(distance)
        return (lambda situation: not f(situation))

    @classmethod
    def having_overlapped_box(cls):
        def _having_overlapped_box(situation):
            layout = situation.agent_set
            box = situation.agent

            bool_function = BoxAgent.overlap_or_not

            return bool_for_layout_and_box(layout, box, bool_function)

        return _having_overlapped_box

# imports - - - - - - -
from layout import *
from rule import *
from agent import *
from specification import *
import random
