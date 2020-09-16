import json


class Wizard:
    def __init__(self):
        """
        Wizard for setting up config file
        """
        # Gather user input
        self.objective = input('Enter path to objective file: ')
        objective_count = int(input('Enter number of objectives: '))
        self.optimization_type = []
        print("Enter optimization types (MAX or MIN)")
        for i in range(objective_count):
            self.optimization_type.append(input("Objective %s: " % (i + 1)))
        variable_count = int(input("Enter number of objective variables: "))
        self.max_ = []
        self.min_ = []
        print("Enter objective variable max and min values:")
        for i in range(variable_count):
            print("Variable %s" % (i + 1))
            self.max_.append(input("Max: "))
            self.min_.append(input("Min: "))
        self.swarm_distribution = input('Enter swarm distribution type (EVEN or RANDOM): ')
        self.c1 = input("Enter c1: ")
        self.c2 = input("Enter c2: ")
        self.max_w = input("Enter maximum weight: ")
        self.min_w = input("Enter minimum weight: ")
        self.max_iterations = input("Enter maximum iterations (stopping condition): ")
        self.min_avg_velocity = input("Enter minimum average velocity (stopping condition): ")
        self.particle_num = input("Enter number of particles: ")
        self.cube_count = input("Enter number of cubes to be used in the hypercube: ")
        self.solution_count = input("Enter maximum number of solutions to store: ")
        # Create the JSON file
        self.create_config()

    def create_config(self):
        """
        Convert the user input into a JSON config file
        """
        config = {
          "objective": self.objective,
          "c1": self.c1,
          "c2": self.c2,
          "min_w": self.min_w,
          "max_w": self.max_w,
          "particle_num": self.particle_num,
          "max_iterations": self.max_iterations,
          "min_avg_velocity": self.min_avg_velocity,
          "max": self.max_,
          "min": self.min_,
          "cube_count":  self.cube_count,
          "solution_count": self.solution_count,
          "optimization_type": self.optimization_type,
          "swarm_distribution": self.swarm_distribution,
        }
        # Create the JSON file
        with open('config.json', 'w') as out:
            json.dump(config, out, indent=1)


if __name__ == "__main__":
    Wizard()
