# needs to run from test file
import unittest
import sys
from swarm import Swarm
import numpy as np
sys.path.insert(1, "../")  # to import running in the test path


class TestSwarm(unittest.TestCase):

    def test_num_particles_swarm(self):
        test_swarm = Swarm(num_particles=13, min_=[0, 1, 2], max_=[1, 2, 3])
        num_p = len(test_swarm.swarm) == 13
        self.assertEqual(num_p, True)

    def test_num_dims_particles(self):
        test_swarm = Swarm(num_particles=13, min_=[0, 1, 2], max_=[1, 2, 3])
        dims_p = all(len(x.x) == 3 for x in test_swarm.swarm)
        self.assertEqual(dims_p, True)


    def test_range_particle_dims(self):
        test_swarm = Swarm(num_particles=13, min_=[0, 1, 2], max_=[1, 2, 3])
        high = [1, 2, 3]
        low = [0, 1, 2]
        range_dims = all(high[y] >= x.x[y] >= low[y] for x, y in zip(test_swarm.swarm, range(len(test_swarm.swarm[0].x))))
        self.assertEqual(range_dims, True)

    def test_num_dims_velocity(self):
        test_swarm = Swarm(num_particles=13, min_=[0, 1, 2], max_=[1, 2, 3])
        vel_p = all(len(x.velocity) == 3 for x in test_swarm.swarm)
        self.assertEqual(vel_p, True)


if __name__ == "__main__":
    unittest.main()
