# needs to run from test file
import unittest
import io
import sys
import random
import numpy as np
sys.path.insert(1, "./src/") # to import py classes
import optimiser

class TestOptimiser(unittest.TestCase):
    def test_weight_regression(self):
        o = optimiser.Optimiser("test_config.json")
        o.weight_regression()
        boolean = 0 <= o.weight <= 1
        self.assertEqual(boolean, True)
    
    def test_avg_velocity_calculator_init(self):
        o = optimiser.Optimiser("test_config.json")
        v = optimiser._get_avg_velocity(o.swarm.particles)
        self.assertEqual(v, 0)
    
    def test_avg_velocity_calculator(self):
        o = optimiser.Optimiser("test_config.json")
        for particle in o.swarm.particles:
            particle.velocity = np.random.uniform(1, 1, len(o.problem.min))
        v = optimiser._get_avg_velocity(o.swarm.particles)
        self.assertAlmostEqual(v, 5.477225575051661)
    
    def test_stop_on_iter(self):
        o = optimiser.Optimiser("test_config.json")
        for particle in o.swarm.particles:
            particle.velocity = np.random.uniform(1, 1, len(o.problem.min))
        o.iteration = o.problem.max_iterations+1
        boolean = o.stop()
        self.assertEqual(boolean, True)
    
    def test_not_stop(self):
        o = optimiser.Optimiser("test_config.json")
        for particle in o.swarm.particles:
            particle.velocity = np.random.uniform(1, 1, len(o.problem.min))
        boolean = o.stop() # assuming false if min_avg_v is lesser than 5.477225 
        self.assertEqual(boolean, False)
    
    def test_problem_folder(self):
        args = ["optimiser.py", "./benchmarks/zdt/zdt1"]
        args2 = ["optimiser.py", "./benchmarks/zdt/zdt1/"]
        path = optimiser.get_problem(args)
        path2 = optimiser.get_problem(args2)
        self.assertEqual(path, "./benchmarks/zdt/zdt1/")
        self.assertEqual(path2, "./benchmarks/zdt/zdt1/")
    
    def test_no_problem_folder(self):
        args = ["optimiser.py"]
        with self.assertRaises(AttributeError):
            path = optimiser.get_problem(args)

if __name__ == "__main__":
    unittest.main()