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
        self.spatial_grid.clear()
        for body in self.bodies:
            self.spatial_grid.insert(body)

        for body in self.bodies:
            body.update(self.bodies, dt)
        return self.check_collisions()
    
    def check_collisions(self):
        collisions=[]
        checked_pairs= set()

        for body in self.bodies:
            nearby = self.spatial_grid.query_radius(body.pos,body.radius*3)
            for other in nearby:
                if id(body) == id(other):
                    continue
                pair_id = (min(id(body), id(other)), max(id(body), id(other)))
                if pair_id in checked_pairs:
                    continue
                if body.is_colliding(other):
                    collisions.append((body, other))
                    resolve_elastic_collision(body, other)
                    checked_pairs.add(pair_id)
            return collisions
    def get_total_energy(self):
        return sum(b.kinetic_energy() for b in self.bodies)
    
    def get_total_momentum(self):
        p = Vector2()
        for b in self.bodies:
            p += b.vel * b.mass
        return p
