# needs to run from test file
import unittest
import sys
from swarm import Swarm
sys.path.insert(1, "../")  # to import running in the test path


class TestSwarm(unittest.TestCase):

    def test_num_particles_swarm(self):
        min_ = [0, 1, 2]
        max_ = [1, 2, 3]
        p_num = 13
        test_swarm = Swarm(p_num, min_, max_)
        num_p_a = len(test_swarm.swarm) == p_num
        num_p_b = len(test_swarm.swarm) != p_num
        self.assertEqual(num_p_a, True)
        self.assertEqual(num_p_b, False)

    def test_num_dims_particles(self):
        min_ = [0, 1, 2]
        max_ = [1, 2, 3]
        p_num = 13
        test_swarm = Swarm(p_num, min_, max_)
        dims_p_a = all(len(x.x) == len(min_) for x in test_swarm.swarm)
        dims_p_b = all(len(x.x) == len(max_) for x in test_swarm.swarm)
        self.assertEqual(dims_p_a, True)
        self.assertEqual(dims_p_b, True)

    def test_range_particle_dims(self):
        min_ = [0, 1, 2]
        max_ = [1, 2, 3]
        p_num = 13
        test_swarm = Swarm(p_num, min_, max_)
        range_dims_a = all(max_[y] >= x.x[y] >= min_[y] for x, y in zip(test_swarm.swarm, range(len(test_swarm.swarm[0].x))))
        range_dims_b = any(max_[y] <= x.x[y] <= min_[y] for x, y in zip(test_swarm.swarm, range(len(test_swarm.swarm[0].x))))
        self.assertEqual(range_dims_a, True)
        self.assertEqual(range_dims_b, False)

    def test_num_dims_velocity(self):
        min_ = [0, 1, 2]
        max_ = [1, 2, 3]
        p_num = 13
        test_swarm = Swarm(p_num, min_, max_)
        vel_p_a = all(len(x.velocity) == len(min_) for x in test_swarm.swarm)
        vel_p_b = all(len(x.velocity) == len(max_) for x in test_swarm.swarm)
        self.assertEqual(vel_p_a, True)
        self.assertEqual(vel_p_b, True)


if __name__ == "__main__":
    unittest.main()
