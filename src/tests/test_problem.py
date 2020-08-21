from unittest import TestCase

import problem


class TestSolutionDomination(TestCase):

    def setUp(self):
        self.problem = problem.Problem('test_config.json')

    def tearDown(self):
        self.problem = None

    def test_input(self): # TODO: Perhaps tests for when we use a different input method
        pass
