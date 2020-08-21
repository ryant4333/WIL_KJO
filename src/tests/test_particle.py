# needs to run from test file
import unittest
import sys
sys.path.insert(1, "../") # to import py classes
from solution import Solution
from particle import Particle


class TestParticle(unittest.TestCase):

    def test_particle_evaluate_no_pbest_update(self):
        particle = Particle()
        particle.x = [1, 1]
        particle.p_best = Solution([4,4], [5, 5])
        sol = particle.evaluate(basicObjective, ["MAX", "MAX"])
        self.assertEqual(sol.objectives[0], 2)
        self.assertEqual(sol.objectives[1], 2)
        self.assertEqual(particle.p_best.objectives[0], 5)
        self.assertEqual(particle.p_best.objectives[1], 5)
    
    def test_particle_evaluate_with_pbest_update(self):
        particle = Particle()
        particle.x = [5, 5]
        particle.p_best = Solution([4,4], [5, 5])
        sol = particle.evaluate(basicObjective, ["MAX", "MAX"])
        self.assertEqual(sol.objectives[0], 6)
        self.assertEqual(sol.objectives[1], 6)
        self.assertEqual(particle.p_best.objectives[0], 6)
        self.assertEqual(particle.p_best.objectives[1], 6)

def basicObjective(x):
    new_x = []
    for i in range(len(x)):
        new_x.append(x[i] + 1)
    return new_x

if __name__ == "__main__":
    unittest.main()
