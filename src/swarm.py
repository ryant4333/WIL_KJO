import particle as particle
import numpy as np


class Swarm:

    def __init__(self, num_particles, min_, max_, s_dist):
        self.particles = [particle.Particle() for _ in range(num_particles)]
        self.eval_count = 0
        np_vel = np.random.uniform(0, 0, len(min_))

        # Random swarm distribution
        if s_dist == "RANDOM":
            np_pos = np.array([np.random.uniform(min_[x], max_[x], num_particles) for x in range(len(min_))])

            for j in range(num_particles):
                x_pos = np_pos[:, j]
                self.particles[j].x = x_pos
                self.particles[j].velocity = np.array(np_vel)

        # Even swarm distribution
        elif s_dist == "EVEN":

            arr_sorted = np.array([np.arange(min_[x], max_[x], (max_[x] - min_[x]) / num_particles) for x in range(len(max_))])
            np.random.shuffle((arr_sorted[0]))

            for j in range(num_particles):
                x_pos = arr_sorted[:, j]
                self.particles[j].x = x_pos
                self.particles[j].velocity = np.array(np_vel)

        else:
            raise ValueError(s_dist + " is not a valid distribution type")


if __name__ == "__main__":
    test_swarm = Swarm(13, [0, 1, 2, 0, 0], [1, 2, 3, 1, 1], "EVEN")

    for i in range(len(test_swarm.particles)):
        print(test_swarm.particles[i].x)
