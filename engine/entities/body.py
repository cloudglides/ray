import pygame
from engine.physics.gravity import G

class Body:
    def __init__(self, x, y, mass, radius, color):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2()
        self.mass = mass
        self.radius = radius
        self.color = color

    def update(self, bodies, dt):
        acc = pygame.Vector2()
        for other in bodies:
            if other is self:
                continue
            r = other.pos - self.pos
            dist = max(r.length(), self.radius + other.radius)
            acc += r.normalize() * (G * other.mass / (dist * dist))

        self.vel += acc * dt
        self.pos += self.vel * dt

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            self.color,
            self.pos,
            self.radius
        )
    
    def is_colliding(self, other):
        if other is self:
            return False
        dist = self.pos.distance_to(other.pos)
        return dist < (self.radius + other.radius)

