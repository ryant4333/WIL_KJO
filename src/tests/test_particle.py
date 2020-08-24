# needs to run from test file
import unittest
import sys
import random
sys.path.insert(1, "../") # to import py classes
from solution import Solution
from particle import Particle


class TestParticle(unittest.TestCase):

    # tests that particle returns a solution with the correct fields and doesnt 
    # update pbest
    def test_particle_evaluate_no_pbest_update(self):
        particle = Particle()
        particle.x = [1, 1]
        particle.p_best = Solution([4,4], [5, 5])
        sol = particle.evaluate(basicObjective, ["MAX", "MAX"])
        self.assertEqual(sol.objectives[0], 2)
        self.assertEqual(sol.objectives[1], 2)
        self.assertEqual(sol.x[0], 1)
        self.assertEqual(sol.x[1], 1)
        self.assertEqual(particle.p_best.objectives[0], 5)
        self.assertEqual(particle.p_best.objectives[1], 5)
    
    # tests that the pbest is updated with fully dominated solution is found
    def test_particle_evaluate_with_pbest_update(self):
        particle = Particle()
        particle.x = [5, 5]
        particle.p_best = Solution([4,4], [5, 5])
        sol = particle.evaluate(basicObjective, ["MAX", "MAX"])
        self.assertEqual(sol.objectives[0], 6)
        self.assertEqual(sol.objectives[1], 6)
        self.assertEqual(particle.p_best.objectives[0], 6)
        self.assertEqual(particle.p_best.objectives[1], 6)
    
    # tests that the max or the min param in move is incorrect
    def test_particle_move_type_error(self):
        particle = Particle()
        particle.p_best = Solution([1, 1], [1, 1])
        particle.s_best = Solution([1, 1], [5, 5])
        particle.x = [0, 0]
        particle.velocity = [0.5, 0.5]
        with self.assertRaises(TypeError):
            particle.move(1,1,1, [100,100], [-100])
        with self.assertRaises(TypeError):
            particle.move(1,1,1, [100], [-100,-100])
    
    # tests that the particle moves in a random way, 
    # seeded so it prodcues the same result each time
    def test_particle_move(self):
        particle = Particle()
        particle.p_best = Solution([1, 1], [1, 1])
        particle.s_best = Solution([1, 1], [5, 5])
        particle.x = [0, 0]
        particle.velocity = [0.5, 0.5]
        random.seed(13)
        particle.move(1,1,1, [100,100], [-100, -100])
        self.assertAlmostEqual(particle.x[0], 2.38853297)
        self.assertAlmostEqual(particle.x[1], 2.38853297)
        

def basicObjective(x):
    new_x = []
    for i in range(len(x)):
        new_x.append(x[i] + 1)
    return new_x

if __name__ == "__main__":
    unittest.main()
