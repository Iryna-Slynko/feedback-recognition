from recognition.decider import Decider


class Decision:
    def __init__(self, is_decided, is_upvote):
        self.is_decided = is_decided
        self.is_upvote = is_upvote


class RepeatedDecider:
    def __init__(self):
        self.__decider_class__ = Decider
        self.__analyzed_count__ = 0
        self.__decisions__ = []
        self.reset_count = 0

    def analyze(self, np_array):
        if self.reset_count > 0:
            self.reset_count -= 1
            return
        self.__analyzed_count__ += 1
        single_decider = self.__decider_class__(np_array)
        self.__decisions__.append(
            Decision(single_decider.is_decided(), single_decider.is_upvote())
        )

    def is_decided(self):
        decided = 0
        for decision in self.__recent_decisions__():
            if decision.is_decided:
                decided += 1

        if decided < 4:
            return False

        positive = 0
        negative = 0
        for decision in self.__recent_decisions__():
            if decision.is_upvote:
                positive += 1
            else:
                negative += 1

        return abs(positive - negative) > 2

    def is_upvote(self):
        votes = 0
        for decision in self.__recent_decisions__():
            if decision.is_upvote:
                votes += 1
        return votes > 0 and (len(self.__decisions__) / votes) <= 2

    def has_input(self):
        decided = 0
        for decision in self.__recent_decisions__():
            if decision.is_decided:
                decided += 1
        return decided > 0

    def __recent_decisions__(self):
        return self.__decisions__[-7:]

    def reset(self):
        self.reset_count = 100
        self.__decisions__ = []

    def is_reseting(self):
        return self.reset_count > 0
