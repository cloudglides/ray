import pygame


class Satellite:
    def __init__(self, pos, vel, mass=1.0):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(vel)
        self.mass = mass
        self.radius = 20
        self.color = (255, 255, 255)

    def update(self, acc, dt):
        self.vel += acc * dt
        self.pos += self.vel * dt

    def draw(self, screen):
        vel_normalized = self.vel.normalize() if self.vel.length() > 0 else pygame.Vector2(0, -1)
        
        angle = vel_normalized.angle_to(pygame.Vector2(0, -1))
        tip = self.pos + vel_normalized * self.radius
        left = self.pos + pygame.Vector2(vel_normalized).rotate(140) * self.radius * 0.6
        right = self.pos + pygame.Vector2(vel_normalized).rotate(-140) * self.radius * 0.6
        
        points = [
            (int(tip.x), int(tip.y)),
            (int(left.x), int(left.y)),
            (int(right.x), int(right.y))
        ]
        pygame.draw.polygon(screen, self.color, points)

