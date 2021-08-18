from recognition.decider import Decider


class RepeatedDecider:
    def __init__(self):
        self.__decider_class__ = Decider
        self.__analyzed_count__ = 0
        self.__decisions__ = []

    def analyze(self, np_array):
        self.__analyzed_count__ += 1
        single_decider = self.__decider_class__(np_array)
        self.__decisions__.append(single_decider.is_upvote())

    def is_decided(self):
        if self.__analyzed_count__ < 4:
            return False

        positive = 0
        negative = 0
        for decision in self.__recent_decisions__():
            if decision:
                positive += 1
            else:
                negative += 1

        return abs(positive - negative) > 2

    def is_upvote(self):
        votes = 0
        for decision in self.__recent_decisions__():
            if decision:
                votes += 1
        return votes > 0 and (len(self.__decisions__) / votes) <= 2

    def decided_result(self):
        return True

    def __recent_decisions__(self):
        return self.__decisions__[-7:]
