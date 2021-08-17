from recognition.repeated_decider import RepeatedDecider
import unittest


class MockUpvoteDecider:
    def __init__(self, np_array):
        pass

    def is_decided(self):
        return True

    def is_upvote(self):
        return True


class MockDownvoteDecider:
    def __init__(self, np_array):
        pass

    def is_decided(self):
        return True

    def is_upvote(self):
        return False


class MockUndecidedDecider:
    def __init__(self, np_array):
        pass

    def is_decided(self):
        return False

    def is_upvote(self):
        return False


class TestRepeatedDecider(unittest.TestCase):
    def test_undecided_in_beginning(self):
        self.assertFalse(RepeatedDecider().is_decided())

    def test_get_decided_if_five_times_gets_decided(self):
        decider = RepeatedDecider()
        decider.__decider_class__ = MockUpvoteDecider
        for _ in range(5):
            decider.analyze([])
        self.assertTrue(decider.is_decided())

    def test_show_the_average_result_of_decider_downvote(self):
        decider = RepeatedDecider()
        decider.__decider_class__ = MockDownvoteDecider
        decider.analyze([])
        self.assertFalse(decider.is_upvote())

    def test_show_the_average_result_of_decider_upvote(self):
        decider = RepeatedDecider()
        decider.__decider_class__ = MockUpvoteDecider
        decider.analyze([])
        self.assertTrue(decider.is_upvote())

    def test_show_the_average_result_of_decider_mixed(self):
        decider = RepeatedDecider()
        decider.__decider_class__ = MockUpvoteDecider
        decider.analyze([])
        decider.analyze([])
        decider.__decider_class__ = MockDownvoteDecider
        decider.analyze([])
        self.assertTrue(decider.is_upvote())
