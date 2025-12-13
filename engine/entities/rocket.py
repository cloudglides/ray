import pygame
from engine.physics.gravity import gravity_acceleration
from engine.physics.trajectory import predict

class Rocket:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)
        self.angle = 0
        self.mass = 5
        self.throttle = 0
        self.max_thrust = 120
        self.selected = False

    @property
    def forward(self):
        return pygame.Vector2(1, 0).rotate(self.angle)

    def update(self, planets, dt):
        acc = pygame.Vector2(0, 0)

        for p in planets:
            acc += gravity_acceleration(self.pos, p)

        if self.throttle > 0:
            acc += self.forward * (self.throttle * self.max_thrust / self.mass)

        self.vel += acc * dt
        self.pos += self.vel * dt

    def draw(self, screen):
        pygame.draw.circle(screen, (120, 200, 255), self.pos, 5)
        tip = self.pos + self.forward * 12
        pygame.draw.line(screen, (255, 255, 255), self.pos, tip, 2)

    def trajectory(self, planets):
        return predict(self.pos, self.vel, planets)

    def contains(self, point):
        return self.pos.distance_to(point) < 8
