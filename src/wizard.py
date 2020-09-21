import json


class Wizard:
    """
    Wizard for setting up config file
    """
    def __init__(self):
        # Objective (ignoring checks for this)
        self.objective = input('Enter path to objective function: ')
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
        # Objective variables
        self.variables = []
        for i in range(variable_count):
            while True:
                print("Variable #%s" % (i + 1))
                try:
                    name = str(input("Variable name: "))
                except ValueError:
                    print("Must be type string. Please try again")
                    continue
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
                else:
                    variable = {
                        "name": name,
                        "max": max_value,
                        "min": min_value
                    }
                    self.variables.append(variable)
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
            "cube_count": self.cube_count,
            "solution_count": self.solution_count,
            "variables": self.variables,
            "optimization_type": self.optimization_type,
        }
        # Create the JSON file
        with open('config.json', 'w') as out:
            json.dump(config, out, indent=1)


if __name__ == "__main__":
    Wizard()
