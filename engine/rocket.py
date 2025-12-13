import pygame
import math

class Rocket:
    def __init__(self, x, y, mass, velocity=(0, 0)):
        self.pos = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(velocity)
        self.acceleration = pygame.Vector2(0, 0)
        self.mass = mass

        self.size = 18
        self.selected = False
        self.angle = -90  
    def apply_force(self, force):
        self.acceleration += force / self.mass

    def update(self, dt):
        self.velocity += self.acceleration * dt
        self.pos += self.velocity * dt

        if self.velocity.length() > 0.1:
            self.angle = math.degrees(
                math.atan2(self.velocity.y, self.velocity.x)
            )

        self.acceleration.update(0, 0)


    def predict_trajectory(self, planets, steps=600, dt=0.03):
        pos = self.pos.copy()
        vel = self.velocity.copy()

        points = []

        for _ in range(steps):
            acc = pygame.Vector2(0, 0)

            for p in planets:
                direction = p.pos - pos
                dist = max(direction.length(), p.radius + 8)

                force_mag = p.mass / (dist * dist)
                acc += direction.normalize() * force_mag

            vel += acc * dt
            pos += vel * dt
            points.append(pos.copy())

        return points


    def contains_point(self, point):
        return self.pos.distance_to(point) <= self.size


    def get_points(self):
        nose = pygame.Vector2(self.size, 0)
        left = pygame.Vector2(-self.size * 0.6, self.size * 0.5)
        right = pygame.Vector2(-self.size * 0.6, -self.size * 0.5)

        points = [nose, left, right]
        return [self.pos + p.rotate(self.angle) for p in points]

    def draw(self, screen):
        color = (255, 90, 90) if self.selected else (220, 220, 220)
        pygame.draw.polygon(screen, color, self.get_points())

        if self.selected:
            pygame.draw.polygon(screen, (255, 255, 255), self.get_points(), 2)

