import pygame
from engine.entities.body import Body
from engine.physics.gravity import G

class Moon(Body):
    def __init__(self, x, y, mass, radius, color, parent=None):
        super().__init__(x, y, mass, radius, color)
        self.parent = parent
    
    def update(self, bodies, dt):
        if self.parent:
            pos_rel = self.pos - self.parent.pos
            vel_rel = self.vel - self.parent.vel
            
            dist = max(pos_rel.length(), self.radius + self.parent.radius)
            acc_rel = pos_rel.normalize() * (-G * self.parent.mass / (dist * dist))
            
            vel_rel += acc_rel * dt
            pos_rel += vel_rel * dt
            
            self.pos = self.parent.pos + pos_rel
            self.vel = self.parent.vel + vel_rel
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
