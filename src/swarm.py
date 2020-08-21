import particle as particle
import numpy as np


class Swarm:

    def __init__(self, num_particles, min_, max_):
        self.swarm = [particle.Particle() for _ in range(num_particles)]
        self.eval_count = 0

        np_vel = np.random.uniform(0, 0, len(min_))
        list_pos = []

        for i in range(len(min_)):
            list_pos.append(np.random.uniform(min_[i], max_[i], num_particles))

        np_arr = np.array(list_pos)

        for x in range(len(min_)):
            np.random.shuffle(np_arr[x, :])
        for j in range(num_particles):
            x_pos = np_arr[:, j]
            self.swarm[j].x = x_pos
            self.swarm[j].velocity = np.array(np_vel)


if __name__ == "__main__":
    test_swarm = Swarm(13, [0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0], [1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1])
    test_swarm.swarm[0].x[0] = 1.1

    for i in range(len(test_swarm.swarm)):
        print(test_swarm.swarm[i].x)
