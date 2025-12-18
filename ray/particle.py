class Particle:
    def __init__(self, pos, vel, lifetime, color, ptype):
        self.ptype = ptype
        self.pos = pos
        self.vel = vel
        self.lifetime = lifetime
        self.color = color
        self.age = 0

    def update(self, dt):
        self.age += dt
        self.pos += self.vel * dt

    def is_alive(self):
        return self.age < self.lifetime

    def alpha(self):
        return int(255 * (1 - self.age / self.lifetime))
