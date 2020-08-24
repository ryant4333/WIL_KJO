from unittest import TestCase

from problem import Problem


class TestSolutionDomination(TestCase):

    def setUp(self):
        self.config = Problem('test_config.json')

    def tearDown(self):
        self.config = None

    def test_read_as_methods_correct(self):
        # check if objective methods have been converted to functions properly
        for obj in self.config.objectives:
            self.assertTrue(callable(obj))

    def test_read_as_methods_false(self):
        # check if unconverted methods are detected
        # (?) maybe don't need this test, I'm not sure
        self.config.objectives = ["zdt_test.ZDT1", "zdt_test.ZDT2"]  # using unconverted objectives
        for obj in self.config.objectives:
            self.assertFalse(callable(obj))
