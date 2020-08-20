import particle as particle
import numpy as np
import main as main

config = main.Problem("config.json")
# min = (0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0)
# max = (1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1)
# num_particles = 3


class Swarm:

    def __init__(self, num_particles):
        self.swarm = [particle.Particle(p_values()) for _ in range(num_particles)]


def p_values():
    x = []
    for i in range(len(config.min)):
        x.append(np.random.uniform(config.min[i], config.max[i]))

    np_array = np.array(x)
    return np_array


if __name__ == "__main__":

    test_swarm = Swarm(config.particle_num)
    for i in test_swarm.swarm:
        print(i.x)
