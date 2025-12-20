from typing import List, Set, Tuple, TYPE_CHECKING
from .type_defs import Vector2
from .spatial_grid import SpatialGrid
from .collision import *
from .contact import Contact

if TYPE_CHECKING:
    from .body import Body


class World:
    def __init__(
            self,
            cell_size: float = 5e8,
            use_spatial_energy: bool = False,
            ) -> None:
        self.bodies: List["Body"] = []
        self.spatial_grid: SpatialGrid = SpatialGrid(cell_size)
        self.contacts: List[Contact] = []

    def update(self, dt: float) -> List[Contact]:
        self.spatial_grid.clear()
        for body in self.bodies:
            self.spatial_grid.insert(body)

        for body in self.bodies:
            body.update(self.bodies, dt, self.spatial_grid, self.spatial_grid.cell_size)

        collisions = self.check_collisions()
        solve_collisions_iteratively(collisions, iterations=10)
        return collisions 

    def add_body(self, body: "Body") -> None:
        self.bodies.append(body)
    
    def check_collisions(self) -> List[Contact]:
        collisions: List[Contact] = []
        checked_pairs: Set[Tuple[int, int]] = set()

        for body in self.bodies:
            search_radius = body.radius+self.spatial_grid.cell_size
            nearby=self.spatial_grid.query_radius(body.pos, search_radius)

            for other in nearby:
                if id(body)>=id(other):
                    continue

                pair_id = (id(body), id(other))
                if pair_id in checked_pairs:
                    continue
                
                if body.is_colliding(other):
                    contact = resolve_elastic_collision(body,other)
                    if contact:
                        collisions.append(contact)
                    checked_pairs.add(pair_id)

        return collisions



    def get_total_energy(self) -> float:
        return sum(b.kinetic_energy() for b in self.bodies)
    
    def get_total_momentum(self) -> Vector2:
        p = Vector2()
        for b in self.bodies:
            p += b.vel * b.mass
        return p
