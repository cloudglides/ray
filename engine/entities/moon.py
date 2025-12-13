import pygame
from engine.entities.body import Body
from engine.physics.gravity import G

class Moon(Body):
    def __init__(self, x, y, mass, radius, color, parent=None):
        super().__init__(x, y, mass, radius, color)
        self.parent = parent
    
    def update(self, bodies, dt):
        if self.parent:
            r = self.parent.pos - self.pos
            dist = max(r.length(), self.radius + self.parent.radius)
            acc = r.normalize() * (G * self.parent.mass / (dist * dist))
            
            self.vel += acc * dt
            self.pos += self.vel * dt
        else:
            acc = pygame.Vector2()
            for other in bodies:
                if other is self:
                    continue
                r = other.pos - self.pos
                dist = max(r.length(), self.radius + other.radius)
                acc += r.normalize() * (G * other.mass / (dist * dist))
            
            self.vel += acc * dt
            self.pos += self.vel * dt
