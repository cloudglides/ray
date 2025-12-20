from typing import Optional, TYPE_CHECKING
from .type_defs import Vector2

if TYPE_CHECKING:
    from .body import Body

class Contact:
    def __init__(self, body1: "Body", body2: "Body", normal: Vector2, penetration: float, restitution: float = 0.5) -> None:
        self.body1 = body1
        self.body2 = body2
        self.normal = normal.normalize()
        self.penetration = penetration
        self.accumulated_impulse = 0.0
        self.age = 0
        self.is_new = True
        self.restitution = restitution
    
    def is_same(self, other: "Contact") -> bool:
        return (id(self.body1) == id(other.body1) and id(self.body2) == id(other.body2)) or \
               (id(self.body1) == id(other.body2) and id(self.body2) == id(other.body1))
    
    def update_age(self) -> None:
        self.age += 1
    
    def is_alive(self, max_age: int = 10) -> bool:
        return self.age < max_age
