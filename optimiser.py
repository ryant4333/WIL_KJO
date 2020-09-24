import sys
import random
import numpy as np
import math
import time
import multiprocessing
from functools import partial

sys.path.insert(1, "./src/")

import problem
import swarm
import hypercubes
import particle
import solution
import plot_graph

class Optimiser:
    def __init__(self, config):
        self.problem = problem.Problem(config)
        """Keeps instance of problem class which is responsible for holding 
        config file data."""
        self.swarm = swarm.Swarm(self.problem.particle_num,
            self.problem.min,
            self.problem.max)
        """Keeps instance of swarm class which is responsible for an array of 
        particles."""
        self.hypercubes = hypercubes.Hypercubes(
            self.problem.cube_count,
            self.problem.solution_count)
        """Keeps instance of hypercubes which is responsible for storing the 
        pareto front."""
        self.iteration = 0
        """Saves iteration step of the optimiser, increases at each iteration in
        run function.
        """
        self.weight = self.problem.max_w
        """Weight of inertia for all particles."""

    def weight_regression(self):
        """Changes the value for the weight variable, current implementation 
        is linear decreasing"""
        nt = self.problem.max_iterations
        t = self.iteration
        w0 = self.problem.max_w
        wnt = self.problem.min_w
        wt = ((w0 - wnt) * ((nt - t)/nt)) + wnt
        self.weight = wt
    
    def stop(self):
        """Checks to see if iteration is greater or equal to the max iterations
        in config file. If true, function returns true. If false, function
        checks if average velocity is less than min average velocity in the 
        config file and if true swarm will restart and return false."""
        if self.iteration >= self.problem.max_iterations:
            return True

        v = _get_avg_velocity(self.swarm.particles)

        if v < self.problem.min_avg_velocity:
            self.swarm = swarm.Swarm(self.problem.particle_num,
                self.problem.min,
                self.problem.max)

        return False

    def run(self, verbose=False):
        """Runs MOPSO optimisation. If verbose is true, terminal will output 
        details."""
        start = time.perf_counter()

        #initalise process pool and functions
        cores = multiprocessing.cpu_count()
        if verbose:
            print("NUMBER OF CORES: ", cores)
            print("CREATING PROCESSES ... ", end = '')

        pool = multiprocessing.Pool(cores)
        if verbose:
            print("DONE")
            
        eval_func = partial(
            _eval_process, 
            self.problem.objective
        )

        manager = multiprocessing.Manager()
        d = manager.dict()

        move_func = partial(
            _move_process, 
            self.problem.c1,
            self.problem.c2,
            d
        )

        while True:
            self.iteration+=1
            if verbose:
                print(
                "ITERATION: ", self.iteration,
                " SOLS: ", self.hypercubes.sol_count,
                " AVG V: ", _get_avg_velocity(self.swarm.particles)
                )

            # evaluate particle positions
            new_sols = pool.map(eval_func, self.swarm.particles)

            # update pbest with new sols
            for i in range(len(self.swarm.particles)):
                self.swarm.particles[i].update_pbest(
                    new_sols[i], 
                    self.problem.optimization_type
                )
            
            updated = False
            for sol in new_sols:
                updated = self.hypercubes.update_bounds(sol)
            
            if updated:
                self.hypercubes.redo_dict(self.problem.optimization_type)
            
            for sol in new_sols:
                self.hypercubes.push_sol(sol, self.problem.optimization_type)
            
            #select each particles gbest
            for particle in self.swarm.particles:
                gbest = self.hypercubes.select_gbest()
                particle.s_best = gbest
            
            #calc particles veloctiy with new weight regression
            self.weight_regression()
            # vs = []
            # for particle in self.swarm.particles:
            #     vs.append(particle.calc_velocity(
            #         self.problem.c1,
            #         self.problem.c2, 
            #         self.weight
            #     ))
            
            # vs = pool.map(move_func, self.swarm.particles)
            pool.map(move_func, [(self.swarm.particles[i], i, self.weight) for i in range(len(self.swarm.particles))])

            #move particles 
            for i in range(len(self.swarm.particles)):
                self.swarm.particles[i].move(
                    d[i], 
                    self.problem.max, 
                    self.problem.min
                )

            if self.stop():
                end = time.perf_counter()
                if verbose:
                    print("RUNNING TIME: ", end - start, " seconds")
                break

def _eval_process(objective, particle):
    """
    A global function which is used for wrapping the particle.evaluate function
    to be used by an instance of Pool from the multiprocess library.
    """
    return particle.evaluate(objective)

def _move_process(c1, c2, manager, args):
    """A global function which is used for wrapping the calc_velcoity function 
    to be used by an instance of Pool from the mulitprocessing library"""
    v = args[0].calc_velocity(c1, c2, args[2])
    manager[args[1]] = v

def _get_avg_velocity(particles):
    """Calculates the average velocity of the particles."""
    v_sum = np.random.uniform(0, 0, len(particles[0].velocity))
    for particle in particles:
        v_sum = v_sum + particle.velocity

    v_average = v_sum / len(particles)
    v2 = sum(map(lambda x: x * x, v_average))
    v = math.sqrt(v2)
    return v

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise AttributeError("Missing directory to problem folder")
    d = sys.argv[1]
    if not d[-1] in ('/', '\\'):
        d+='/'

    sys.path.insert(1, d)
    config = d+"config.json"
    optimiser = Optimiser(config)
    optimiser.run(verbose=True)
    plot_graph.plot(optimiser.problem.objective.__name__, optimiser, d)
