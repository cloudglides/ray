import pygame
from engine.entities.planet import Planet

pygame.init()

W, H = 1000, 700
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

planets = [
    Planet(500, 350, 40, 20000, (255, 255, 100)),  # star
    Planet(500, 200, 10, 200, (100, 150, 255)),  # orbiting planet
]

planets[1].vel.x = 6.7


running = True
while running:
    dt = clock.tick(60) / 1000.0
    screen.fill((10, 10, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            new_planet = Planet(x, y, 50, 300, (200, 100, 200))
            planets.append(new_planet)

    for p in planets:
        p.update(planets, dt)

    for p in planets:
        p.draw(screen)

    # Draw center of mass
    if planets:
        total_mass = sum(p.mass for p in planets)
        cm_x = sum(p.pos.x * p.mass for p in planets) / total_mass
        cm_y = sum(p.pos.y * p.mass for p in planets) / total_mass
        pygame.draw.circle(screen, (255, 0, 0), (cm_x, cm_y), 5)

    pygame.display.flip()

pygame.quit()
