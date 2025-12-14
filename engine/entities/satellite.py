import pygame
import math
from engine.physics.gravity import G

class Satellite:
    def __init__(self, pos, vel, mass=1.0):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(vel)
        self.mass = mass
        self.radius = 5
        self.color = (255, 255, 255)
        self.rotation = 0  # angle in degrees
        self.thrust_power = 10000  # acceleration when thrusting

    def update(self, bodies, dt, gravity=True):
        if gravity:
            from engine.physics.gravity import G
            acc = pygame.Vector2()
            for other in bodies:
                if other is self:
                    continue
                r = other.pos - self.pos
                dist = max(r.length(), self.radius + other.radius)
                acc += r.normalize() * (G * other.mass / (dist * dist))
            self.vel += acc * dt
        
        self.pos += self.vel * dt

    def apply_thrust(self, dt):
        rad = math.radians(self.rotation)
        thrust_vec = pygame.Vector2(math.sin(rad), -math.cos(rad)) * self.thrust_power
        self.vel += thrust_vec * dt
        print(f"Thrust applied: {thrust_vec * dt}, New vel: {self.vel}")

    def rotate(self, angle_delta):
        self.rotation += angle_delta
        self.rotation %= 360

    def draw(self, screen):
        rad = math.radians(self.rotation)
        
        size = 1
        tip = pygame.Vector2(math.sin(rad), -math.cos(rad)) * size
        left = pygame.Vector2(math.sin(rad + 0.4), -math.cos(rad + 0.4)) * size 
        right = pygame.Vector2(math.sin(rad - 0.4), -math.cos(rad - 0.4)) * size
        
        points = [
            (int(self.pos.x + tip.x), int(self.pos.y + tip.y)),
            (int(self.pos.x + left.x), int(self.pos.y + left.y)),
            (int(self.pos.x + right.x), int(self.pos.y + right.y))
        ]
        pygame.draw.polygon(screen, self.color, points)


    def predict_trajectory(self, bodies, steps=100, dt=0.01):
        pos = self.pos.copy()
        vel = self.vel.copy()
        path = []

        for _ in range(steps):
            acc = pygame.Vector2()
            for other in bodies:
                r = other.pos - pos
                dist = r.length()
                if dist > 0.1:
                    dist = max(dist,5)
                    acc+=r.normalize()*(G*other.mass/(dist*dist))
            vel += acc * dt
            pos += vel * dt 
            path.append(pos.copy())
        return path
        
        

