import unittest
import sys
sys.path.insert(1, "./tests/")
sys.path.insert(1, "./benchmarks/zdt/zdt1") 
import test_particle
import test_problem
import test_solution
import test_swarm
import test_optimiser
import test_plotgraph

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
    .loadTestsFromTestCase(test_plotgraph.TestPlotgraph))
suite_list.append(unittest.TestLoader()
    .loadTestsFromTestCase(test_optimiser.TestOptimiser))

combo_suite = unittest.TestSuite(suite_list)
unittest.TextTestRunner(verbosity=0).run(combo_suite)
