import json


class Problem:
    """
    Saves config file in the problem class.
    """
    def __init__(self, config_file):
        """Initialises a problem class based on a config json file"""
        # Read data from JSON file
        with open(config_file) as f:
            config = json.load(f)
        # Declaring variables
        self.objective: str = config['objective']
        self.c1: float = config['c1']
        self.c2: float = config['c2']
        self.max_w: float = config['max_w']
        self.min_w: float = config['min_w']
        self.particle_num: int = config['particle_num']
        self.max_iterations: int = config['max_iterations']
        self.min_avg_velocity: float = config['min_avg_velocity']
        self.max: list[float] = config['max']
        self.min: list[float] = config['min']
        self.cube_count: int = config['cube_count']
        self.optimization_type: list[str] = config['optimization_type']
        self.solution_count: int = config['solution_count']
        # Convert objective to method
        self.convert_to_method(self.objective)
        # Validation
        self.validate_config()

    def validate_config(self):
        """
        Perform validation on the config file
        - Checking types
        - Checking values
        """
        self.validate_types()
        self.validate_values()

    def validate_types(self):
        """
        Validates the config file types
        """
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

    def validate_values(self):
        """
        Validates specific config file values
        """
        # Values are greater than 0 and non-negative
        if self.particle_num <= 0:
            raise ValueError("particle_num should be greater than 0")
        if self.max_iterations <= 0:
            raise ValueError("max_iterations should be greater than 0")
        if self.cube_count <= 0:
            raise ValueError("cube_count should be greater than 0")
        if self.solution_count <= 0:
            raise ValueError("solution_count should be greater than 0")
        # Is the optimization types either 'MIN' or 'MAX'
        for i in self.optimization_type:
            if i != "MAX" and i != "MIN":
                raise ValueError("optimization_type '%s' should be MAX or MIN" % i)
        # Is min & max the same array size?
        if len(self.max) != len(self.min):
            raise ValueError("size of max (%s) and min (%s) should be equal" % (len(self.max), len(self.min)))
        # Are the min inputs less than the max outputs
        for i in range(len(self.max)):
            if self.max[i] <= self.min[i]:
                raise ValueError("min values should be less than max values (%s not less than %s)"
                                 % (self.min[i], self.max[i]))

    def convert_to_method(self, objective):
        """
        Convert objective name to function reference
        """
        try:
            s = objective.split(".")
            module = __import__(s[0])
            self.objective = getattr(module, s[1])
        except NameError:
            raise NameError("Objective '%s' was not found" % objective)
        if not callable(self.objective):
            raise ValueError("Objective '%s' is not callable" % objective)
