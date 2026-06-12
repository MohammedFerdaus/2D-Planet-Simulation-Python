import numpy as np
import config
 
class Body:
    def __init__(self, name, mass, radius, color, position, velocity):
        self.name = name
        self.mass = mass
        self.radius = radius
        self.color = color

        self.pos = np.array(position, dtype = float)
        self.vel = np.array(velocity, dtype = float)
        self.acc = np.zeros(2, dtype = float)

        self.init_pos = self.pos.copy()
        self.init_vel = self.vel.copy()

        self.trail = []
        
    def update_trail(self):
        self.trail.append(self.pos.copy())        
        if len(self.trail) > config.trail_length:
            self.trail.pop(0)

    def reset(self):
        self.pos = self.init_pos.copy()
        self.vel = self.init_vel.copy()
        self.acc = np.zeros(2, dtype = float)
        self.trail = []
        pass

def compute_forces(bodies):
    for body in bodies:
        body.acc = np.zeros(2, dtype=float)
    for i in range(len(bodies)):
        for j in range(i + 1, len(bodies)):
            body_i = bodies[i]
            body_j = bodies[j]
            dv = body_j.pos - body_i.pos
            sd = np.linalg.norm(dv) + config.softening

            sg = config.gravity / sd**2
            uv = dv/sd

            bodies[i].acc += sg * body_j.mass * uv
            bodies[j].acc -= sg * body_i.mass * uv

def integrate(bodies, dt):
    bodies[0].pos = np.array([0.0, 0.0])
    acc_old = [body.acc.copy() for body in bodies]

    for body in bodies:
        body.pos += body.vel * dt + 0.5 * body.acc * dt**2

    compute_forces(bodies)

    for i, body in enumerate(bodies):
        if i == 0:  # Pin the Sun
            continue
        body.vel += 0.5 * (acc_old[i] + body.acc) * dt
