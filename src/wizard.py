import json
import zdt.zdt1

# TODO: Having an issue reading the objective functions without importing them.
#  e.g. 'zdt.zdt1.objectives.ZDT1' will not work without importing zdt.zdt1.
#  There also seems to be a problem where ZDT1 is not callable.


class Wizard:
    def __init__(self):
        """
        Wizard for setting up config file
        """
        # Objective
        while True:
            self.objective = input('Enter path to objective function: ')
            try:
                # Try to evaluate the objective
                s = self.objective.split(".")
                module = __import__(s[0])
                test_method = getattr(module, s[1])
            except:
                print("Objective '%s' not found. Please try again." % self.objective)
                continue
            if not callable(test_method):
                print("Objective '%s' is not callable. Please try again." % self.objective)
                continue
            else:
                break
        # Objective Count
        while True:
            try:
                objective_count = int(input('Enter number of objectives: '))
            except ValueError:
                print("Must be type int. Please try again")
                continue
            if objective_count <= 0:
                print("Value must be greater than 0.")
                continue
            else:
                break
        # Optimization Type
        self.optimization_type = []
        print("Enter optimization types (MAX or MIN)")
        for i in range(objective_count):
            while True:
                try:
                    optimization = str(input("Objective %s: " % (i + 1)))
                except ValueError:
                    print("Must be type string. Please try again")
                    continue
                if optimization != "MAX" and optimization != "MIN":
                    print("Optimization type must be either 'MAX' or 'MIN'. Please try again.")
                    continue
                else:
                    self.optimization_type.append(optimization)
                    break
        # Objective variables count
        while True:
            try:
                variable_count = int(input("Enter number of objective variables: "))
            except ValueError:
                print("Must be type int. Please try again")
                continue
            if variable_count <= 0:
                print("Value must be greater than 0.")
                continue
            else:
                break
        # Objective variables (max and min)
        self.max_ = []
        self.min_ = []
        for i in range(variable_count):
            while True:
                print("Variable %s" % (i + 1))
                try:
                    max_value = float(input("Max: "))
                except ValueError:
                    print("Must be type float. Please try again")
                    continue
                try:
                    min_value = float(input("Min: "))
                except ValueError:
                    print("Must be type float. Please try again")
                    continue
                if max_value <= min_value:
                    print("Maximum (%s) should be greater than minimum (%s). "
                          "Please try again." % (max_value, min_value))
                    continue
                else:
                    self.max_.append(max_value)
                    self.min_.append(min_value)
                    break
        # Swarm Distribution
        while True:
            try:
                self.swarm_distribution = str(input('Enter swarm distribution type (EVEN or RANDOM): '))
            except ValueError:
                print("Must be type string. Please try again")
                continue
            if self.swarm_distribution != "EVEN" and self.swarm_distribution != "RANDOM":
                print("Swarm distribution must be either 'EVEN' or 'RANDOM'. Please try again")
                continue
            else:
                break
        # C1
        while True:
            try:
                self.c1 = float(input("Enter c1: "))
            except ValueError:
                print("Must be type float. Please try again")
                continue
            else:
                break
        # C2
        while True:
            try:
                self.c2 = float(input("Enter c2: "))
            except ValueError:
                print("Must be type float. Please try again")
                continue
            else:
                break
        # Max W and MIN W
        while True:
            while True:
                try:
                    self.max_w = float(input("Enter maximum weight: "))
                except ValueError:
                    print("Must be type float. Please try again")
                    continue
                else:
                    break
            while True:
                try:
                    self.min_w = float(input("Enter minimum weight: "))
                except ValueError:
                    print("Must be type float. Please try again")
                    continue
                else:
                    break
            if self.max_w <= self.min_w:
                print("Maximum (%s) should be greater than minimum (%s). "
                      "Please try again." % (self.max_w, self.min_w))
                continue
            else:
                break
        # Max Iterations
        while True:
            try:
                self.max_iterations = int(input("Enter maximum iterations (stopping condition): "))
            except ValueError:
                print("Must be type int. Please try again")
                continue
            if self.max_iterations <= 0:
                print("Value must be greater than 0.")
                continue
            else:
                break
        # Min Avg Velocity
        while True:
            try:
                self.min_avg_velocity = float(input("Enter minimum average velocity (stopping condition): "))
            except ValueError:
                print("Must be type float. Please try again")
                continue
            else:
                break
        # Particle Number
        while True:
            try:
                self.particle_num = int(input("Enter number of particles: "))
            except ValueError:
                print("Must be type int. Please try again")
                continue
            if self.particle_num <= 0:
                print("Value must be greater than 0.")
                continue
            else:
                break
        # Cube Count
        while True:
            try:
                self.cube_count = int(input("Enter number of cubes to be used in the hypercube: "))
            except ValueError:
                print("Must be type int. Please try again")
                continue
            if self.cube_count <= 0:
                print("Value must be greater than 0.")
                continue
            else:
                break
        # Solution Count
        while True:
            try:
                self.solution_count = int(input("Enter maximum number of solutions to store: "))
            except ValueError:
                print("Must be type int. Please try again")
                continue
            if self.solution_count <= 0:
                print("Value must be greater than 0.")
                continue
            else:
                break
        # Create the JSON file
        self.create_config()
        print("\nSuccessfully created config file!")

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
