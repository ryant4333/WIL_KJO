import particle as particle
import numpy as np


min_ = (0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0)
max_ = (1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1)
p_num = 2
# ----------------------------------------------------------------#


class Swarm:

    def __init__(self, num_particles):
        self.swarm = [particle.Particle(p_values()) for _ in range(num_particles)]


def p_values():
    x = []
    for i in min_:
        x.append(np.random.uniform(min_[i], max_[i]))

    np_array = np.array(x)
    return np_array

#---------------------------------------------------------------#


test_swarm = Swarm(p_num)


if __name__ == "__main__":

    for i in test_swarm.swarm:
        print(i.x)
