import pygame

class Planet:
    def __init__(self, x, y, radius, mass):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)
        self.acc = pygame.Vector2(0, 0)  
        self.radius = radius
        self.color = (255, 200, 50)
        self.mass = mass
    
    def apply_gravity(self, other, G=9.8):
        direction = other.pos - self.pos
        distance = direction.length()
        if distance == 0 or distance < self.radius + other.radius:
            return
        
        force_mag = G * (self.mass * other.mass) / (distance * distance)
        direction.normalize_ip()
        force = direction * force_mag
        
        self.acc += force / self.mass
    
    def update(self, dt, all_planets, G=9.8):
        self.acc.update(0, 0)
        
        for other in all_planets:
            if other is not self:
                self.apply_gravity(other, G)
        
        self.vel += self.acc * dt
        self.pos += self.vel * dt
