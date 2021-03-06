import particle as particle
import numpy as np


class Swarm:
    """
    Swarm is a class called by the optimiser.py to create an array of particles with randomised positions and velocities
    within the boundaries set by the user in the config file.
    """
    def __init__(self, num_particles: int, min_: list, max_: list):
        """Initialises swarm of n particles in random positions between the max 
        and min search domains."""
        self.particles = [particle.Particle() for _ in range(num_particles)]
        self.eval_count = 0
        np_vel = np.random.uniform(0, 0, len(min_))

        # Random swarm distribution
        np_pos = np.array([np.random.uniform(min_[x], max_[x], num_particles) for x in range(len(min_))])

        for j in range(num_particles):
            x_pos = np_pos[:, j]
            self.particles[j].x = x_pos
            self.particles[j].velocity = np.array(np_vel)


if __name__ == "__main__":
    test_swarm = Swarm(13, [0, 1, 2, 0, 0], [1, 2, 3, 1, 1])

    for i in range(len(test_swarm.particles)):
        print(test_swarm.particles[i].x)
