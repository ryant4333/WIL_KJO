from unittest import TestCase

import swarm
import problem


class TestSolutionDomination(TestCase):

    def setUp(self):
        self.problem = problem.Problem('test_config.json')
        self.swarm = swarm.Swarm()

    def tearDown(self):
        self.swarm = None

    def test_fully_dominated(self):
        self.assertFalse(self.solution_1.fully_dominated(self.solution_2, ["MAX", "MAX"]))
