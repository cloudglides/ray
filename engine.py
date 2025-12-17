from type_defs import Vector2
from spatial_grid import SpatialGrid
from collision import resolve_elastic_collision



class World:
    def __init__(self, cell_size: float = 1e8):
        self.bodies = []
        self.spatial_grid = SpatialGrid(cell_size)
    
    def add_body(self, body):
        self.bodies.append(body)
    
    def update(self, dt):
        for body in self.bodies:
            body.update(self.bodies, dt)
        return self.check_collisions()
    
    def check_collisions(self):
        collisions=[]
        for i, body1 in enumerate(self.bodies):
            for body2 in self.bodies[i + 1:]:
                if body1.is_colliding(body2):
                    collisions.append((body1,body2))
                    resolve_elastic_collision(body1, body2)
        return collisions
    
    def get_total_energy(self):
        return sum(b.kinetic_energy() for b in self.bodies)
    
    def get_total_momentum(self):
        p = Vector2()
        for b in self.bodies:
            p += b.vel * b.mass
        return p
