import particle as particle
import numpy as np


class Swarm:

    def __init__(self, num_particles, min_, max_, even):
        self.particles = [particle.Particle() for _ in range(num_particles)]
        self.eval_count = 0
        np_vel = np.random.uniform(0, 0, len(min_))

        # Even dist particles
        arr_list = []
        for i in range(len(max_)):
            dist = (max_[i] - min_[i]) / num_particles
            arr_list.append(np.arange(min_[i], max_[i], dist))
        arr_sorted = np.array(arr_list)
        np.random.shuffle((arr_sorted[0]))

        # Random dist particles
        np_pos = np.array([np.random.uniform(min_[x], max_[x], num_particles) for x in range(len(min_))])

        # Assign a position and velocity to each particle in swarm
        for j in range(num_particles):
            if even:
                x_pos = arr_sorted[:, j]
            else:
                x_pos = np_pos[:, j]
            self.particles[j].x = x_pos
            self.particles[j].velocity = np.array(np_vel)


if __name__ == "__main__":
    test_swarm = Swarm(13, [0, 1, 2, 0, 0], [1, 2, 3, 1, 1])

    for i in range(len(test_swarm.particles)):
        print(test_swarm.particles[i].x)
