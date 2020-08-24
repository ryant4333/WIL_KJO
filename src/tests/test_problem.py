from unittest import TestCase

import problem


class TestSolutionDomination(TestCase):

    def setUp(self):
        self.config = problem.Problem('test_config.json')

    def tearDown(self):
        self.config = None

    def test_input(self):
        """
        This function let's us read in and execute the objective function as string BUT..
        I couldn't figure out how to extract the actual function from it and use it somewhere else

        Input that worked: def add(a, b):\n    result = a + b\n    print(result)\n    return result\nadd(1, 2)"
        """
        # print(self.config.objectives)
        # code = compile(self.config.objectives[0], "<string>", "exec")
        # exec(code)
