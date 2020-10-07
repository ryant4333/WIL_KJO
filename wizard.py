import json
import os


class Wizard:
    """
    The Wizard is a CLI (Command Line Interface) used for building
    a config file. It is an independent program separate from
    the optimiser.

    Inputs the Wizard requests from the user:
        - Path to the objective function
        - Number of objectives
        - Optimisation types (for given number of objectives)
        - Number of variables
        - Name, maximum, and minimum for each variable
        - C1 value
        - C2 value
        - Maximum weight value
        - Minimum weight value
        - Max iterations
        - Minimum Average Velocity value
        - Particle count
        - Cube count
        - Solution count
        - Directory where the config.json should be saved

    Once these inputs are given, the Wizard will create a JSON file
    in the specified directory. It will be named 'config.json'.
    """
    def __init__(self):
        self.objective = None
        self.c1 = None
        self.c2 = None
        self.min_w = None
        self.max_w = None
        self.particle_num = None
        self.max_iterations = None
        self.min_avg_velocity = None
        self.cube_count = None
        self.solution_count = None
        self.variables = None
        self.optimization_type = None
        self.path = None

    def start(self):
        """
        Start the wizard.
        """
        # Objective (ignoring checks for this)
        self.objective = input('Enter path to objective function: ')
        clear()
        # Objective Count
        while True:
            try:
                objective_count = int(input('Enter number of objectives: '))
            except ValueError:
                clear()
                print("Must be type int. Please try again.")
                continue

            if objective_count <= 0:
                clear()
                print("Value must be greater than 0. Please try again.")
                continue
                clear()
            else:
                clear()
                break
        # Optimization Type
        self.optimization_type = []
        print("Enter optimization types (MAX or MIN)")
        for i in range(objective_count):
            while True:
                try:
                    optimization = str(input("Objective %s: " % (i + 1)))
                except ValueError:
                    clear()
                    print("Enter optimization types (MAX or MIN)")
                    print("Must be type string. Please try again")
                    continue
                if optimization != "MAX" and optimization != "MIN":
                    clear()
                    print("Enter optimization types (MAX or MIN)")
                    print("Optimization type must be either 'MAX' or 'MIN'. Please try again.")
                    continue
                else:
                    self.optimization_type.append(optimization)
                    clear()
                    print("Enter optimization types (MAX or MIN)")
                    break
        clear()
        # Objective variables count
        while True:
            try:
                variable_count = int(input("Enter number of objective variables: "))
            except ValueError:
                clear()
                print("Must be type int. Please try again.")
                continue
            if variable_count <= 0:
                clear()
                print("Value must be greater than 0. Please try again.")
                continue
            else:
                clear()
                break
        # Objective variables
        self.variables = []
        print("Enter variable values (For infinite values use 'inf' or '-inf').")
        for i in range(variable_count):
            while True:
                print("Variable #%s" % (i + 1))
                try:
                    name = input("Name: ")
                except ValueError:
                    print("Enter variable values (For infinite values use 'inf' or '-inf').")
                    print("Invalid input. Please try again.")
                    clear()
                    continue
                try:
                    max_value = input("Max: ")
                    if max_value != 'inf' and max_value != '-inf':
                        max_value = float(max_value)
                except ValueError:
                    clear()
                    print("Enter variable values (For infinite values use 'inf' or '-inf').")
                    print("Invalid input. Please try again.")
                    continue
                try:
                    min_value = input("Min: ")
                    if min_value != 'inf' and min_value != '-inf':
                        min_value = float(min_value)
                except ValueError:
                    clear()
                    print("Enter variable values (For infinite values use 'inf' or '-inf').")
                    print("Invalid input. Please try again.")
                    continue
                else:
                    variable = {
                        "name": name,
                        "max": max_value,
                        "min": min_value
                    }
                    self.variables.append(variable)
                    clear()
                    print("Enter variable values (For infinite values use 'inf' or '-inf').")
                    break
        clear()
        # C1
        while True:
            try:
                self.c1 = float(input("Enter c1: "))
            except ValueError:
                clear()
                print("Must be type float. Please try again.")
                continue
            else:
                clear()
                break
        # C2
        while True:
            try:
                self.c2 = float(input("Enter c2: "))
            except ValueError:
                clear()
                print("Must be type float. Please try again.")
                continue
            else:
                clear()
                break
        # Max W and MIN W
        while True:
            while True:
                try:
                    self.max_w = float(input("Enter maximum weight: "))
                except ValueError:
                    clear()
                    print("Must be type float. Please try again.")
                    continue
                else:
                    clear()
                    break
            while True:
                try:
                    self.min_w = float(input("Enter minimum weight: "))
                except ValueError:
                    clear()
                    print("Must be type float. Please try again.")
                    continue
                else:
                    clear()
                    break
            if self.max_w <= self.min_w:
                clear()
                print("Maximum (%s) should be greater than minimum (%s). "
                      "Please try again." % (self.max_w, self.min_w))
                continue
            else:
                clear()
                break
        # Max Iterations
        while True:
            try:
                self.max_iterations = int(input("Enter maximum iterations (stopping condition): "))
            except ValueError:
                clear()
                print("Must be type int. Please try again.")
                continue
            if self.max_iterations <= 0:
                clear()
                print("Value must be greater than 0. Please try again.")
                continue
            else:
                clear()
                break
        # Min Avg Velocity
        while True:
            try:
                self.min_avg_velocity = float(input("Enter minimum average velocity (stopping condition): "))
            except ValueError:
                clear()
                print("Must be type float. Please try again.")
                continue
            else:
                clear()
                break
        # Particle Number
        while True:
            try:
                self.particle_num = int(input("Enter number of particles: "))
            except ValueError:
                clear()
                print("Must be type int. Please try again.")
                continue
            if self.particle_num <= 0:
                clear()
                print("Value must be greater than 0. Please try again.")
                continue
            else:
                clear()
                break
        # Cube Count
        while True:
            try:
                self.cube_count = int(input("Enter number of cubes to be used in the hypercube: "))
            except ValueError:
                clear()
                print("Must be type int. Please try again.")
                continue
            if self.cube_count <= 0:
                clear()
                print("Value must be greater than 0. Please try again.")
                continue
            else:
                clear()
                break
        # Solution Count
        while True:
            try:
                self.solution_count = int(input("Enter maximum number of solutions to store: "))
            except ValueError:
                clear()
                print("Must be type int. Please try again.")
                continue
            if self.solution_count <= 0:
                clear()
                print("Value must be greater than 0. Please try again.")
                continue
            else:
                clear()
                break
        # File path to save the config.json
        while True:
            self.path = input("Enter file path to save config ( '.' for current dir): ")
            exists = os.path.exists(self.path)
            is_directory = os.path.isdir(self.path)
            if not exists and not is_directory:
                clear()
                print("'%s' is an invalid directory. Please try again." % self.path)
            else:
                clear()
                break
        # Create the JSON file
        self.create_config()
        print("Successfully created config file!")

    def create_config(self):
        """
        Converts the user input into a config.json file.
        This file will be saved in the specified directory path.
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
        # Path to save file
        file = os.path.join(self.path, 'config.json')
        # Create the JSON file
        with open(file, 'w') as out:
            json.dump(config, out, indent=1)


def clear():
    """
    Clears the CLI. Used to make the Wizard experience more user-friendly.
    This should work in both a Windows or Unix environment.
    """
    os.system('cls' or 'clear')


if __name__ == "__main__":
    w = Wizard()
    w.start()
