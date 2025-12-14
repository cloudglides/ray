import pygame
from engine.entities.body import Body
from engine.physics.gravity import G

class Moon(Body):
    def __init__(self, x, y, mass, radius, color, parent=None):
        super().__init__(x, y, mass, radius, color)
        self.parent = parent
    
    def update(self, bodies, dt):
        # Always apply gravity from all bodies
        acc = pygame.Vector2()
        for other in bodies:
            if other is self:
                continue
            r = other.pos - self.pos
            dist = max(r.length(), self.radius + other.radius)
            acc += r.normalize() * (G * other.mass / (dist * dist))
        
        self.vel += acc * dt
        self.pos += self.vel * dt
        
        # Update trail
        self.trail.append(self.pos.copy())
        if len(self.trail) > self.trail_length:
            self.trail.pop(0)
