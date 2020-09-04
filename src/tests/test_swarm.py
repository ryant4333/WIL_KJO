# needs to run from test file
import unittest
import sys
sys.path.insert(1, "../")  # to import running in the test path
from swarm import Swarm

class TestSwarm(unittest.TestCase):

    def test_num_particles_swarm(self):
        min_ = [0, 1, 2]
        max_ = [1, 2, 3]
        p_num = 13
        test_swarm = Swarm(p_num, min_, max_,"EVEN")
        num_p_a = len(test_swarm.particles) == p_num
        num_p_b = len(test_swarm.particles) != p_num
        self.assertEqual(num_p_a, True)
        self.assertEqual(num_p_b, False)

    def test_num_dims_particles(self):
        min_ = [0, 1, 2]
        max_ = [1, 2, 3]
        p_num = 13
        test_swarm = Swarm(p_num, min_, max_,"EVEN")
        dims_p_a = all(len(x.x) == len(min_) for x in test_swarm.particles)
        dims_p_b = all(len(x.x) == len(max_) for x in test_swarm.particles)
        self.assertEqual(dims_p_a, True)
        self.assertEqual(dims_p_b, True)

    def test_range_particle_dims(self):
        min_ = [0, 1, 2]
        max_ = [1, 2, 3]
        p_num = 13
        test_swarm = Swarm(p_num, min_, max_,"EVEN")
        range_dims_a = all(max_[y] >= x.x[y] >= min_[y] for x, y in zip(test_swarm.particles, range(len(test_swarm.particles[0].x))))
        range_dims_b = any(max_[y] <= x.x[y] <= min_[y] for x, y in zip(test_swarm.particles, range(len(test_swarm.particles[0].x))))
        self.assertEqual(range_dims_a, True)
        self.assertEqual(range_dims_b, False)

    def test_num_dims_velocity(self):
        min_ = [0, 1, 2]
        max_ = [1, 2, 3]
        p_num = 13
        test_swarm = Swarm(p_num, min_, max_,"EVEN")
        vel_p_a = all(len(x.velocity) == len(min_) for x in test_swarm.particles)
        vel_p_b = all(len(x.velocity) == len(max_) for x in test_swarm.particles)
        self.assertEqual(vel_p_a, True)
        self.assertEqual(vel_p_b, True)

    def test_dist_input_value_error(self):
        min_ = [0, 1, 2]
        max_ = [1, 2, 3]
        p_num = 13
        with self.assertRaises(ValueError):
            test_swarm = Swarm(p_num, min_, max_, "BANANA")



if __name__ == "__main__":
    unittest.main()
