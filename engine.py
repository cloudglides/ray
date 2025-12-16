from type_defs import Vector2
class World:
    def __init__(self):
        self.bodies = []
    def add_body(self, body):
        self.bodies.append(body)
    def update(self, dt):
        for body in self.bodies:
            body.update(self.bodies, dt)
        self.check_collisions()
    def check_collisions(self):
        for i, body1 in enumerate(self.bodies):
            for body2 in self.bodies[i + 1:]:
                if body1.is_colliding(body2):
                    pass
    def get_total_energy(self):
        return sum(b.kinetic_energy() for b in self.bodies)
    def get_total_momentum(self):
        p = Vector2()
        for b in self.bodies:
            p += b.vel * b.mass
        return p
