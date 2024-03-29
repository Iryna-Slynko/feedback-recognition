from recognition.repeated_decider import RepeatedDecider
import unittest

decision_times = 20


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

    def test_get_decided_if_multiple_times_gets_decided(self):
        decider = RepeatedDecider()
        decider.__decider_class__ = MockUpvoteDecider
        for _ in range(decision_times):
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

    def test_undecided_if_result_of_seven_latest_is_mixed(self):
        decider = RepeatedDecider()
        decider.__decider_class__ = MockUpvoteDecider
        for _ in range(decision_times // 3 + 1):
            decider.analyze([])
        decider.__decider_class__ = MockDownvoteDecider
        for _ in range(2 * decision_times // 3 - 1):
            decider.analyze([])
        self.assertFalse(decider.is_decided())

    def test_decided_if_result_of_more_than_some_amount_is_mixed_but_than_stable(
        self,
    ):
        decider = RepeatedDecider()
        decider.__decider_class__ = MockUpvoteDecider
        for _ in range(decision_times // 3):
            decider.analyze([])
        decider.__decider_class__ = MockDownvoteDecider
        for _ in range(2 * decision_times // 3 + 1):
            decider.analyze([])
        self.assertTrue(decider.is_decided())

    def test_decided_if_result_of_recent_latest_undecided(
        self,
    ):
        decider = RepeatedDecider()
        decider.__decider_class__ = MockUndecidedDecider
        for _ in range(decision_times):
            decider.analyze([])
        self.assertFalse(decider.is_decided())

    def test_refresh_resets_decision_and_skips_hundred_next_ones(self):
        decider = RepeatedDecider()
        decider.__decider_class__ = MockUpvoteDecider
        for _ in range(decision_times):
            decider.analyze([])
        self.assertTrue(decider.is_decided())
        decider.reset()
        for _ in range(100):
            decider.analyze([])
            self.assertFalse(decider.is_decided())
        for _ in range(decision_times):
            decider.analyze([])
        self.assertTrue(decider.is_decided())

    def test_refresh_resets_decision_skips_hundred_next_ones_and_shows_that_it_is_not_analyzing(
        self,
    ):
        decider = RepeatedDecider()
        decider.__decider_class__ = MockUpvoteDecider
        decider.reset()
        for _ in range(99):
            decider.analyze([])
            self.assertTrue(decider.is_reseting())
        decider.analyze([])
        self.assertFalse(decider.is_reseting())
