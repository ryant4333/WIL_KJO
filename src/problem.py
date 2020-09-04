import json
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
        self.objective: str = config['objective']
        self.c1: float = config['c1']
        self.c2: float = config['c2']
        self.max_w: float = config['max_w']
        self.min_w: float = config['max_w']
        self.particle_num: int = config['particle_num']
        self.max_iterations: int = config['max_iterations']
        self.min_avg_velocity: float = config['min_avg_velocity']
        self.max: list[float] = config['max']
        self.min: list[float] = config['min']
        self.cube_count: int = config['cube_count']
        self.optimization_type: list[str] = config['optimization_type']
        self.solution_count: int = config['solution_count']

    #     # validate ...
    #     self.type_check(self.objective, self.c1, self.c2, self.max_w, self.min_w, self.particle_num,
    #                     self.max_iterations, self.min_avg_velocity, self.max, self.min, self.cube_count,
    #                     self.optimization_type, self.solution_count)
    #
    #     # convert to a method
    #     self.objective = convert_to_method(self.objective)
    #
    # def type_check(self, objective: str, c1: float, c2: float, max_w: float, min_w: float, particle_num: int,
    #                max_iterations: int, min_avg_velocity: float, maximum: list[float], minimum: list[float],
    #                cube_count: int, optimization_type: list[str], solution_count: int):
    #     pass

    def validate_input(self):
        # Check types

        # Is the objective valid?

        # Is min & max the same array size?

        # Are the mins less than the maxs

        # Is the optimization types either 'MIN' or 'MAX'

        # Are the correct values +/ve

        # Are the certain values not 0
        pass

    def validate_types(self):
        """
        Validates the config file types
        """
        if type(self.objective) != str:
            raise TypeError("objective should be type: <string>")
        if type(self.c1) != float and type(self.c1) != int:
            raise TypeError("c1 should be type: <float>")
        if type(self.c2) != float and type(self.c2) != int:
            raise TypeError("c2 should be type: <float>")
        if type(self.min_w) != float and type(self.min_w) != int:
            raise TypeError("min_w should be type: <float>")
        if type(self.max_w) != float and type(self.max_w) != int:
            raise TypeError("max_w should be type: <float>")
        if type(self.particle_num) != int:
            raise TypeError("particle_num should be type: <int>")
        if type(self.max_iterations) != int:
            raise TypeError("particle_num should be type: <int>")
        if type(self.min_avg_velocity) != float and type(self.min_avg_velocity) != int:
            raise TypeError("min_avg_velocity should be type: <float>")
        if type(self.max) != list:
            raise TypeError("max should be type: <list of floats>")
        if type(self.min) != list:
            raise TypeError("min should be type: <list of floats>")
        if type(self.cube_count) != int:
            raise TypeError("cube_count should be type: <int>")
        if type(self.solution_count) != int:
            raise TypeError("solution_count should be type: <int>")
        if type(self.optimization_type) != list:
            raise TypeError("optimization_type should be type: <list of strings>")
        # Checking list nested types
        for i in self.max:
            if type(i) != float and type(i) != int:
                raise TypeError("max should be type: <list of floats>")
        for i in self.min:
            if type(i) != float and type(i) != int:
                raise TypeError("min should be type: <list of floats>")
        for i in self.optimization_type:
            if type(i) != str:
                raise TypeError("optimization_type should be type: <list of strings>")


def convert_to_method(objective):
    """
    Convert objective name to function reference
    """
    # Check if a valid objective name was given
    try:
        method = eval(objective)
    except NameError:
        raise NameError("Objective '%s' was not found" % objective)
    if not callable(method):
        raise ValueError("Objective '%s' is not callable" % objective)
    return method
