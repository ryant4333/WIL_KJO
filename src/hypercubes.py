from solution import Solution
import numpy as np
import matplotlib.pyplot as plt
import random




class Hypercubes:
    """
    Hypercubes is a class to store non dominated solutions using pareto dominance.
    It works by dividing the solution space into sub-cubes based on the cube count.
    A high cube count means each sub-cube covers smaller space. Each sub-cube is 
    a list of solutions. These lists are stored in a dictionary with their 
    location in the solution space as the key. 

    For example a cube count of 10 in a 2d solution space, the bottom left sub
    - cube key will be 0 0, the top right will be 9 9.
    
    To decide what 
    sub-cube a solution belongs in, it's values are compared to the max and min
    values of the solution space.

    Each non dominated solution added to the hypercube updates the solution space
    dynamically, however when a solution is removed, that space is not adjusted.
    When solution space is adjusted, hypercube is remade.
    """
    def __init__(self,cube_count, max_solutions):
        """
        Solutions are kept in a dictionary and keys will be sub-cubes which 
        contain a list of solutions in that area in the hypercube.
        The hypercube object has a counter to keep track of the sum of solutions 
        inside each of the sub-cubes.
        Each sub-cube has a bin size which dictates the key it will have. 
        """
        self.cube_dict: dict = {}
        self.sol_count: int = 0
        self.max_sol_count: int = max_solutions
        self.bin_size: list = []
        self.max: list = []
        self.min: list = []
        self.cube_count: int = cube_count

    def get_bin_key(self, sol: Solution):
        """
        input is solution object
        returns a string of which bin each of its values fall into
        Used as key for dictionary to say which sub-cube the solution goes into.
        """
        key_list = []
        for i in range(len(sol.objectives)):
            key_val = int(sol.objectives[i] / self.bin_size[i])
            key_list.append(key_val)
        return str(key_list)

    def push_sol(self, new_solution, optimizaton_type: list, skipcheck: bool = False):
        """
        If new solution check == True
        add new solution to a cube
        """

        if skipcheck or self.new_sol_check(new_solution, optimizaton_type):
            if self.sol_count >= self.max_sol_count:
                self.delete_sol()

            key = self.get_bin_key(new_solution)
            if key in self.cube_dict:
                self.cube_dict[key].append(new_solution)
            else:
                self.cube_dict[key] = [new_solution]
            self.sol_count += 1
        
        return

    def new_sol_check(self, new_solution: Solution, optimizaton_type: list):
        """
        Checks new sol against all items
        return False if new solution dominated by any solution.
        If new sol dominates a sol in hypercube:
            sol in hypercube is stored in to_del list then deleted after for loop.
        return true if new solution is non-dom
        """
        
        empty_cubes = []
        for cube in self.cube_dict:
            to_del = []
            for i, sol in enumerate(self.cube_dict[cube]):
                dom_status = new_solution.dominated(sol, optimizaton_type)

                if dom_status == -1:
                    return False
                elif dom_status == 1:
                    to_del.append(i)
                elif dom_status == 0:
                    pass

            for i in sorted(to_del, reverse=True):
                del self.cube_dict[cube][i]
                self.sol_count -= 1

            if len(self.cube_dict[cube]) == 0:
                empty_cubes.append(cube)
                #Check if cube empty

        for cube in empty_cubes:
            del self.cube_dict[cube]

        return True

    def select_gbest(self):
        """Uses roulette wheel selection to randomly choose a hypercube, giving 
        hypercubes with LESS solutions more weight. A random solution in this 
        hypercube is then selected. This is returned as the gbest.This 
        promotes exploring hypercubes with less solutions."""
        cube = self.select_min_cube()

        chosen = random.randrange(len(self.cube_dict[cube]))
        return self.cube_dict[cube][chosen]

    def select_min_cube(self):
        """Uses roulette wheel selection to randomly choose a hypercube, giving 
        hypercubes with LESS solutions more weight. This hypercube is then 
        returned"""
        cube_fitness = {}
        keys = self.cube_dict.keys()
        for cube in keys:
            cube_len = len(self.cube_dict[cube])
            cube_fitness[cube] = cube_len
        
        relative_fitness = [(self.sol_count/f) for f in cube_fitness.values()]
        total_fit = sum(relative_fitness)
        relative_fitness = [(f/total_fit) for f in relative_fitness]
        #relative fitness adds to 1
        
        r = random.random()
        counter = 0
        for (i, key) in enumerate(keys):
            counter += relative_fitness[i]
            if r <= counter:
                return key
        return keys[-1]

    def select_cube(self):
        """Uses roulette wheel selection to randomly choose a hypercube, giving 
        hypercubes with MORE solutions more weight. This hypercube is then 
        returned"""
        cube_fitness = {}
        keys = self.cube_dict.keys()
        for cube in keys:
            cube_len = len(self.cube_dict[cube])
            cube_fitness[cube] = cube_len
        
        relative_fitness = [f/self.sol_count for f in cube_fitness.values()]
        #relative fitness adds to 1

        r = random.random()
        counter = 0
        for (i, key) in enumerate(keys):
            counter += relative_fitness[i]
            if r <= counter:
                return key
        return keys[-1]
            
    def delete_sol(self):
        """Uses roulette wheel selection to randomly choose a hypercube, giving 
        hypercubes with MORE solutions more weight. A random solution in this 
        hypercube is then selected. This solution is then deleted. This 
        promotes deleting solutions in dense hypercubes."""
        cube = self.select_cube()
        
        chosen = random.randrange(len(self.cube_dict[cube]))
        del self.cube_dict[cube][chosen]
        
        if len(self.cube_dict[cube]) == 0:
            del self.cube_dict[cube]

        self.sol_count -= 1

    def output_front(self):
        """
        Return list of non dominated solutions
        """
        front = []
        for cube in self.cube_dict:
            for sol in self.cube_dict[cube]:
                front.append(sol.objectives)
        return front
    
    def redo_dict(self, optimization_type: list):
        """Resizes the buckets of the hypercubes based on the max and min values
        of the objectives"""
        buckets = list(self.cube_dict.values())
        self.cube_dict = {}
        self.sol_count = 0
        self.bin_size = []
        key_dist = []

        for i in range(len(self.min)):
            key_dist.append(self.max[i] - self.min[i])
            self.bin_size.append(key_dist[i] / self.cube_count)
        
        for sols in buckets:
            for sol in sols:
                self.push_sol(sol, optimization_type, skipcheck=True)

    def update_bounds(self, sol: Solution):
        """Updates the bounds of the max and min values for the objectives"""
        updated = False

        if self.max == [] and self.min == []:
            updated = True
            self.max = np.array(sol.objectives)
            self.min = np.array(sol.objectives)

        for i in range(len(self.max)):
            if sol.objectives[i] > self.max[i]:
                updated = True
                self.max[i] = sol.objectives[i]
        
        for i in range(len(self.min)):
            if sol.objectives[i] < self.max[i]:
                updated = True
                self.min[i] = sol.objectives[i]
        
        return updated

if __name__ == "__main__":
    pass
