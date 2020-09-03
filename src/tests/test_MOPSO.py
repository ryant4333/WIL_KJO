import unittest
import test_particle
import test_problem
import test_solution
import test_swarm
import test_optimiser

suite_list = []
suite_list.append(unittest.TestLoader()
    .loadTestsFromTestCase(test_particle.TestParticle))
suite_list.append(unittest.TestLoader()
    .loadTestsFromTestCase(test_problem.TestProblem))
suite_list.append(unittest.TestLoader()
    .loadTestsFromTestCase(test_solution.TestSolution))
suite_list.append(unittest.TestLoader()
    .loadTestsFromTestCase(test_swarm.TestSwarm))
suite_list.append(unittest.TestLoader()
    .loadTestsFromTestCase(test_optimiser.TestOptimiser))

combo_suite = unittest.TestSuite(suite_list)
unittest.TextTestRunner(verbosity=0).run(combo_suite)
