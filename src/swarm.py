import particle as particle
import numpy as np


class Swarm:

    def __init__(self, num_particles, min_, max_):
        self.swarm = [particle.Particle() for _ in range(num_particles)]
        self.eval_count = 0

        # Create numpy array for particle positions and velocity
        np_pos = np.array([np.random.uniform(min_[x], max_[x], num_particles) for x in range(len(min_))])
        np_vel = np.random.uniform(0, 0, len(min_))

        # Assign a position and velocity to each particle in swarm
        for j in range(num_particles):
            x_pos = np_pos[:, j]
            self.swarm[j].x = x_pos
            self.swarm[j].velocity = np.array(np_vel)


if __name__ == "__main__":
    test_swarm = Swarm(13, [0, 1, 2, 0, 0], [1, 2, 3, 1, 1])

    for i in range(len(test_swarm.swarm)):
        print(test_swarm.swarm[i].x)
