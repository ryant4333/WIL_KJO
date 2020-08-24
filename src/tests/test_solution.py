from unittest import TestCase

import solution


class TestSolutionDomination(TestCase):

    def setUp(self):
        self.solution_1 = solution.Solution([], [1, 3])
        self.solution_2 = solution.Solution([], [1, 2])

    def tearDown(self):
        self.solution_1 = None
        self.solution_2 = None

    def test_fully_dominated(self):
        self.assertFalse(self.solution_1.fully_dominated(self.solution_2, ["MAX", "MAX"]))
