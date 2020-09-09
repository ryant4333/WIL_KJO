import unittest
import sys
import numpy as np

sys.path.insert(1, "../")  # to import running in the test path
from problem import Problem
import zdt_test


class TestProblem(unittest.TestCase):

    def setUp(self):
        self.problem = Problem('test_config.json')

    def tearDown(self):
        self.problem = None

    def test_import_zdt(self):
        test_input = np.array([0.1, 1])
        self.assertEqual(self.problem.objective(test_input), zdt_test.ZDT1(test_input))

    def test_validation_c1_type(self):
        self.problem.c1 = "1.1"
        with self.assertRaises(TypeError):
            self.problem.validate_config()

    def test_validation_c2_type(self):
        self.problem.c2 = [1]
        with self.assertRaises(TypeError):
            self.problem.validate_config()

    def test_validation_min_w_type(self):
        self.problem.min_w = "1.1"
        with self.assertRaises(TypeError):
            self.problem.validate_config()

    def test_validation_max_w_type(self):
        self.problem.max_w = "1.1"
        with self.assertRaises(TypeError):
            self.problem.validate_config()

    def test_validation_particle_num_type(self):
        self.problem.particle_num = 1.1
        with self.assertRaises(TypeError):
            self.problem.validate_config()

    def test_validation_min_avg_velocity_type(self):
        self.problem.min_avg_velocity = "1.1"
        with self.assertRaises(TypeError):
            self.problem.validate_config()

    def test_validation_max_type(self):
        self.problem.max = 1
        with self.assertRaises(TypeError):
            self.problem.validate_config()

    def test_validation_max_nested_type(self):
        self.problem.max = [1, "1", 1]
        with self.assertRaises(TypeError):
            self.problem.validate_config()

    def test_validation_min_type(self):
        self.problem.max = 1
        with self.assertRaises(TypeError):
            self.problem.validate_config()

    def test_validation_min_nested_type(self):
        self.problem.min = [1, "1", 1]
        with self.assertRaises(TypeError):
            self.problem.validate_config()

    def test_validation_optimization_type_type(self):
        self.problem.optimization_type = 1
        with self.assertRaises(TypeError):
            self.problem.validate_config()

    def test_validation_optimization_type_nested_type(self):
        self.problem.optimization_type = [1, 1]
        with self.assertRaises(TypeError):
            self.problem.validate_config()

    def test_validation_cube_count_type(self):
        self.problem.cube_count = 1.1
        with self.assertRaises(TypeError):
            self.problem.validate_config()

    def test_validation_solution_count_type(self):
        self.problem.solution_count = 1.1
        with self.assertRaises(TypeError):
            self.problem.validate_config()

    def test_validation_particle_num_value(self):
        self.problem.particle_num = 0
        with self.assertRaises(ValueError):
            self.problem.validate_config()

    def test_max_iterations_value(self):
        self.problem.max_iterations = 0
        with self.assertRaises(ValueError):
            self.problem.validate_config()

    def test_cube_count_value(self):
        self.problem.cube_count = 0
        with self.assertRaises(ValueError):
            self.problem.validate_config()

    def test_solution_count_value(self):
        self.problem.solution_count = 0
        with self.assertRaises(ValueError):
            self.problem.validate_config()

    def test_min_max_len_value(self):
        self.problem.max = [1, 1, 1]
        self.problem.min = [0, 0]
        with self.assertRaises(ValueError):
            self.problem.validate_config()

    def test_optimization_type_value(self):
        self.problem.optimization_type = ["MAN", "MIN"]
        with self.assertRaises(ValueError):
            self.problem.validate_config()

    def test_convert_to_method_not_found(self):
        with self.assertRaises(NameError):
            self.problem.convert_to_method('invalid_zdt_test.ZDT1')

    def test_convert_to_method_not_callable(self):
        with self.assertRaises(ValueError):
            self.problem.convert_to_method('zdt_test')
    
    def test_type_error_swarm_dist(self):
        self.problem.swarm_distribution = 1
        with self.assertRaises(TypeError):
            self.problem.validate_types()
    
    def test_value_error_swarm_dist(self):
        self.problem.swarm_distribution = "MEH"
        with self.assertRaises(ValueError):
            self.problem.validate_values()

if __name__ == "__main__":
    unittest.main()