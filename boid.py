import numpy as np
import misc

class boid():

    ##
    #  This is the class for a 1D boid problem. The environment is of given size and wraps around.

    def __init__(self, vars):

        self.acc = 0
        self.F_alignment = 0
        self.F_cohesion = 0
        self.F_separation = 0
        self.F_migration = 0

        self.S2r = vars["S2r"]

        self.gains = vars["gains"]
        self.max_force = vars["max_force"] / self.S2r    # Max Force - non dimensionalised
        self.max_speed = vars["max_speed"] / self.S2r    # Max speed - non dimensionalised
        self.phys_time = vars["phys_time"]              # Time step for physics update

        self.size = vars["s"] / self.S2r                 # Arena size - non dimensionalised
        self.num = vars["num"]
        self.point = 0
        np.random.seed(vars["seed"])

        self.pos = np.random.rand() * self.size
        self.vel = (np.random.rand() - 0.5) * self.max_speed

        self.a = vars["sep_a"] / vars["S2r"]                       # Gaussian function: a is the height of the curve
        self.c = vars["sep_c"] / vars["S2r"]                       # Gaussian function: c is the std of the curve

    def reset(self, point):
        self.pos = np.random.rand() * self.size
        self.vel = (np.random.rand() - 0.5)*self.max_speed
        self.set_point(point)

    def set_point(self, point):
        self.point = point

    def update(self):
        self.pos += self.vel * self.phys_time
        self.vel += self.acc * self.phys_time

        if np.linalg.norm(self.vel) > self.max_speed:
            self.vel = self.vel / np.linalg.norm(self.vel) * self.max_speed

    def apply_behaviour(self, boids):
        self.acc = 0

        self.F_alignment = self.align(boids) * self.gains[0]
        self.F_cohesion = self.cohesion(boids) * self.gains[1]
        self.F_separation = self.separation(boids) * self.gains[2]
        self.F_migration = self.migration() * self.gains[3]

        self.acc += self.F_alignment
        self.acc += self.F_cohesion
        self.acc += self.F_separation
        self.acc += self.F_migration

    def align(self, boids):
        total = 0
        avg = 0
        for boid in boids:
            if self.pos != boid.pos:
                avg += boid.vel
                total += 1

        steering = avg / total

        if np.linalg.norm(steering) > self.max_force:
            steering = (steering / np.linalg.norm(steering)) * self.max_force

        return steering

    def cohesion(self, boids):
        total = 0
        center_of_mass = 0
        for boid in boids:
            if self.pos != boid.pos:
                angle = self.angles(boid.pos)
                center_of_mass += angle
                total += 1

        steering = center_of_mass / total

        if np.linalg.norm(steering) > self.max_force:
            steering = (steering / np.linalg.norm(steering)) * self.max_force

        return steering

    def separation(self, boids):
        steering = 0
        total = 0
        for boid in boids:
            if self.pos != boid.pos:
                angle = self.angles(boid.pos)

                steering += - np.sign(angle) * self.separation_profile(angle)

                total += 1

        if np.linalg.norm(steering) > self.max_force:
            steering = (steering / np.linalg.norm(steering)) * self.max_force

        return steering

    def migration(self):
        return np.sign(self.angles(self.point)) * self.max_force

    def angles(self, pos):
        assert self.pos != pos
        a = np.array([np.cos(self.pos), np.sin(self.pos)])
        b = np.array([np.cos(pos), np.sin(pos)])
        ans = np.arccos(np.dot(a, b)) * np.sign(np.cross(a, b))
        return ans

    def point_reached(self, point, threshold):
        if np.absolute(self.angles(point)) < threshold:
            return True

        return False

    def nearest_neighbour(self, flock):
        dist = 2 * np.pi
        sums = 0
        for b in flock:
            if self.pos != b.pos:
                a = np.absolute(self.angles(b.pos))
                sums += a
                if a < dist:
                    dist = a
        average = sums / len(flock)
        return dist, average

    def separation_profile(self, x):
        return self.a * np.exp(-x**2/(2 * self.c**2))