import unittest
import sys
import zdt_test
import numpy as np

sys.path.insert(1, "../")  # to import running in the test path
from problem import Problem


class TestProblem(unittest.TestCase):

    def test_import_zdt(self):
        self.problem = Problem('test_config.json')
        test_input = np.array([0.1, 1])
        self.assertEqual(self.problem.objective(test_input), zdt_test.ZDT1(test_input))

    def test_val(self):
        self.problem = Problem('test_config.json')
        # with self.assertRaises(TypeError):
