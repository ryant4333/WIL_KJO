import unittest
import sys
import os
from wizard import Wizard

sys.path.insert(1, ".")  # to import running in the test path


class TestWizard(unittest.TestCase):

    def setUp(self):
        self.w = Wizard()
        self.w.objective = 'objectives.ZDT1'
        self.w.c1 = 1.1
        self.w.c2 = 2.2
        self.w.min_w = 0.4
        self.w.max_w = 0.7
        self.w.particle_num = 30
        self.w.max_iterations = 400
        self.w.min_avg_velocity = 0.1
        self.w.cube_count = 10
        self.w.solution_count = 1000
        self.w.variables = [
            {"name": "v1", "max": 1, "min": 0},
            {"name": "v2", "max": 1, "min": 0}
        ]
        self.w.optimization_type = ['MIN', 'MIN']
        self.w.path = '.'

    def tearDown(self):
        try:
            os.remove('config.json')
        except FileNotFoundError:
            pass

    def test_create_config(self):
        self.w.create_config()
        file_created = os.path.isfile('config.json')
        self.assertTrue(file_created)


if __name__ == "__main__":
    unittest.main()
