from recognition.decider import Decider


class RepeatedDecider:
    def __init__(self):
        self.__decider_class__ = Decider
        self.__analyzed_count__ = 0

    def analyze(self, np_array):
        self.__analyzed_count__ += 1
        pass

    def is_decided(self):
        if self.__analyzed_count__ >= 4:
            return True
        return False

    def is_upvote(self):
        return True
