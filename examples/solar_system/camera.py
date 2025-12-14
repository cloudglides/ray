import pygame

class Camera:
    def __init__(self, width, height):
        self.x = 0
        self.y = 0
        self.zoom = 1.0
        self.width = width
        self.height = height
        
    def to_screen(self, world_pos):
        screen_x = (world_pos.x - self.x) * self.zoom + self.width // 2
        screen_y = (world_pos.y - self.y) * self.zoom + self.height // 2
        return pygame.Vector2(screen_x, screen_y)
    
    def from_screen(self, screen_pos):
        world_x = (screen_pos.x - self.width // 2) / self.zoom + self.x
        world_y = (screen_pos.y - self.height // 2) / self.zoom + self.y
        return pygame.Vector2(world_x, world_y)
    
    def pan(self, dx, dy):
        self.x -= dx / self.zoom
        self.y -= dy / self.zoom
    
    def zoom_in(self, factor=1.2):
        self.zoom *= factor
        self.zoom = min(self.zoom, 10)
    
    def zoom_out(self, factor=1.2):
        self.zoom /= factor
        self.zoom = max(self.zoom, 0.1)
    
    def follow(self, target):
        self.x = target.pos.x
        self.y = target.pos.y
