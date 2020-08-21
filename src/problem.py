import json

#I really like the config.json easy for researchers to tinker with

class Problem:
    """
    Read in from text file
    Initialise and pass config variables to Optimiser
    """
    def __init__(self, config_file):
        # Read data from JSON file
        with open(config_file) as f:
            config = json.load(f)
        # Declaring variables
        # TODO: Add variable for objectives
        # self.objectives = config['objectives']
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



if __name__ == '__main__':
    config = Problem("config.json")
    
    print(config.c1)