import pygame
import math
from engine.space.planet import Planet

pygame.init()

W, H = 1000, 700
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

G = 0.1  # gravitational constant


planets = [
    Planet(500, 350, 40, 20000),  # star
    Planet(500, 200, 10, 200),  # orbiting planet
]


planets[1].vel.x = 3.5


def apply_gravity(p1, p2):
    dx = p2.pos.x - p1.pos.x
    dy = p2.pos.y - p1.pos.y
    dist = math.hypot(dx, dy)

    if dist < 1:
        return  # avoid zero division or crazy forces

    force = G * p1.mass * p2.mass / (dist * dist)


    nx = dx / dist
    ny = dy / dist


    p1.vel.x += nx * force / p1.mass
    p1.vel.y += ny * force / p1.mass

    p2.vel.x -= nx * force / p2.mass
    p2.vel.y -= ny * force / p2.mass


running = True
while running:
    screen.fill((10, 10, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    for i in range(len(planets)):
        for j in range(i + 1, len(planets)):
            apply_gravity(planets[i], planets[j])


    for p in planets:
        p.pos += p.vel
        pygame.draw.circle(screen, p.color, (int(p.pos.x), int(p.pos.y)), p.radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
