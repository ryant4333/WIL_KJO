import json
import zdt_test
import numpy as np


class Problem:
    """
    Problem config class
    """
    def __init__(self, config_file):
        # Read data from JSON file
        with open(config_file) as f:
            config = json.load(f)
        # Declaring variables
        self.objective = config['objective']
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

    def import_zdt(self, zdt_objective):
        """
        Sets the objective to the ZDT objective function
        """
        self.objective = zdt_objective

