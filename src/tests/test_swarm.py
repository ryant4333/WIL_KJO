from unittest import TestCase

import swarm
import problem


class TestSolutionDomination(TestCase):

    def setUp(self):
        self.config = problem.Problem()
        self.swarm = swarm.Swarm(self.config.particle_num, True)

    def tearDown(self):
        self.config = None
        self.swarm = None

    def test_set_x(self):  # TODO: set x test
        pass
