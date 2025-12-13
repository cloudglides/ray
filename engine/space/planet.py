import pygame

class Planet:
    def __init__(self, x, y, radius, mass):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)
        self.acc = pygame.Vector2(0, 0)
        self.radius = radius
        self.color = (255, 200, 50)
        self.mass = mass
        
        self.is_dragging = False
        self.drag_offset = pygame.Vector2(0, 0)
        self.drag_start_pos = None
    
    def contains_point(self, pos):
        return (self.pos - pos).length() <= self.radius
    
    def start_drag(self, mouse_pos):
        self.is_dragging = True
        self.drag_offset = self.pos - mouse_pos
        self.drag_start_pos = mouse_pos.copy()
        self.vel.update(0, 0)
    
    def update_drag(self, mouse_pos):
        if self.is_dragging:
            self.pos = mouse_pos + self.drag_offset
    
    def end_drag(self, mouse_pos, throw_strength=5.0):
        if self.is_dragging and self.drag_start_pos:
            throw_direction = mouse_pos - self.drag_start_pos
            throw_vel = throw_direction * throw_strength
            self.vel = throw_vel
        self.is_dragging = False
        self.drag_start_pos = None
    
    def apply_gravity(self, other, G=0.1):
        direction = other.pos - self.pos
        distance = direction.length()
        if distance == 0 or distance < self.radius + other.radius:
            return
        
        force_mag = G * (self.mass * other.mass) / (distance * distance)
        direction.normalize_ip()
        force = direction * force_mag
        
        self.acc += force / self.mass
    
    def update(self, dt, all_planets=None, G=100.0):
        if self.is_dragging:
            return
        
        self.acc.update(0, 0)
        
        if all_planets:
            for other in all_planets:
                if other is not self:
                    self.apply_gravity(other, G)
        
        self.vel += self.acc * dt
        self.pos += self.vel * dt
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color,
                          (int(self.pos.x), int(self.pos.y)), self.radius)
