import pygame

def draw_orbit(screen, points):
    if len(points) < 2:
        return
    orbit_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    pygame.draw.lines(
        orbit_surface,
        (100, 200, 100, 150),  
        False,
        points,
        2
    )
    screen.blit(orbit_surface, (0, 0))

