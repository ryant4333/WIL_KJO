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
        self.objective = convert_to_method(config['objective'])
        self.c1 = config['c1']
        self.c2 = config['c2']
        self.max_w = config['max_w']
        self.min_w = config['max_w']
        self.particle_num = config['particle_num']
        self.max_iterations = config['max_iterations']
        self.min_avg_velocity = config['min_avg_velocity']
        self.max = config['max']
        self.min = config['min']
        self.cube_count = config['cube_count']
        self.optimization_type = config['optimization_type']
        self.solution_count = config['solution_count']
        self.swarm_distribution = config['swarm_distribution']


def convert_to_method(objective):
    """
    Convert objective name to function reference
    """
    return eval(objective)