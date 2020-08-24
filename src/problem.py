import json

"""
NOTE: With the current implementation of reading in objective functions
as methods, we require the actual python file that contains said methods.
(In this case it is the zdt_test file).
"""
import zdt_test


class Problem:
    """
    Problem config class
    """
    def __init__(self, config_file):
        # Read data from JSON file
        with open(config_file) as f:
            config = json.load(f)
        # Declaring variables
        self.objectives = read_as_methods(config['objectives'])
        self.c1 = config['c1']
        self.c2 = config['c2']
        self.start_w = config['start_w']
        self.end_w = config['end_w']
        self.particle_num = config['particle_num']
        self.max_iterations = config['max_iterations']
        self.min_avg_velocity = config['min_avg_velocity']
        self.dimensions = config['dimensions']
        self.max = config['max']
        self.min = config['min']


def read_as_methods(objectives):
    return [eval(obj) for obj in objectives]


"""
OLD read_as_methods code:

This function let's us read in and execute the objective function as string BUT..
I couldn't figure out how to extract the actual function from it and use it somewhere else
Input that worked: def add(a, b):\n    result = a + b\n    print(result)\n    return result\nadd(1, 2)"

(to run this put it back in the test_problem.py testfile)
"""
# print(self.config.objectives)
# code = compile(self.config.objectives[0], "<string>", "exec")
# exec(code)
