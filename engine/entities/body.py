import pygame
from engine.physics.gravity import G

class Body:
    def __init__(self, x, y, mass, radius, color, trail_length=200):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2()
        self.mass = mass
        self.radius = radius
        self.color = color
        self.trail = [self.pos.copy()]
        self.trail_length = trail_length

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
        
        # Update trail
        self.trail.append(self.pos.copy())
        if len(self.trail) > self.trail_length:
            self.trail.pop(0)


        
        
    def draw(self, screen):
        # Draw fading trail
        if len(self.trail) > 1:
            for i in range(len(self.trail) - 1):
                alpha = int(255 * (i / len(self.trail)))
                segment_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
                faded_color = (*self.color, alpha)
                pygame.draw.line(segment_surface, faded_color, self.trail[i], self.trail[i + 1], 1)
                screen.blit(segment_surface, (0, 0))
        scale = 20
        end_pos = pygame.Vector2(self.pos.x + self.vel.x * scale, self.pos.y + self.vel.y * scale)
        pygame.draw.line(screen, (255, 255, 255), self.pos, end_pos, 2)

        if self.vel.length() > 0:
            arrow_size = 5
            arrow_angle = self.vel.angle_to((1, 0))
            left = end_pos + pygame.Vector2(arrow_size, 0).rotate(arrow_angle + 150)
            right = end_pos + pygame.Vector2(arrow_size, 0).rotate(arrow_angle - 150)
            pygame.draw.line(screen, (255, 255, 255), end_pos, left, 2)
            pygame.draw.line(screen, (255, 255, 255), end_pos, right, 2)
        # Draw planet
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

