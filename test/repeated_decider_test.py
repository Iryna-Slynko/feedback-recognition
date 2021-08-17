from recognition.repeated_decider import RepeatedDecider
import unittest


class MockUpvoteDecider:
    def __init__(self, np_array):
        pass

    def is_decided():
        return True

    def is_upvote():
        return True


class TestRepeatedDecider(unittest.TestCase):
    def test_undecided_in_beginning(self):
        self.assertFalse(RepeatedDecider().is_decided())

    def test_get_decided_if_five_times_gets_upvote(self):
        decider = RepeatedDecider()
        decider.__decider_class__ = MockUpvoteDecider
        for _ in range(5):
            decider.analyze([])
        self.assertTrue(decider.is_decided())
