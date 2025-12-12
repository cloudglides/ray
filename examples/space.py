import pygame
from engine.space.planet import Planet

pygame.init()

WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Sandbox")
clock = pygame.time.Clock()

planets = []

dragging_planet = None
drag_offset = pygame.Vector2(0, 0)
mouse_down = False
mouse_down_pos = None
THROW_STRENGTH = 5.0


def get_planet_under_mouse(pos):
    for p in reversed(planets): 
        if (p.pos - pos).length() <= p.radius:
            return p
    return None


running = True
while running:
    dt = clock.tick(60) / 1000

    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True
            mouse_down_pos = mouse_pos

            target = get_planet_under_mouse(mouse_pos)
            if target:
                dragging_planet = target
                drag_offset = target.pos - mouse_pos
                target.vel.update(0, 0)  
        elif event.type == pygame.MOUSEMOTION:
            if dragging_planet:
                dragging_planet.pos = mouse_pos + drag_offset

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_down = False

            release_pos = mouse_pos

            if dragging_planet:
                throw_vel = (mouse_down_pos - release_pos) * THROW_STRENGTH
                dragging_planet.vel = throw_vel
                dragging_planet = None

            else:
                velocity = (mouse_down_pos - release_pos) * THROW_STRENGTH
                p = Planet(mouse_down_pos.x, mouse_down_pos.y,
                           radius=20, mass=5000000)
                p.vel = velocity
                planets.append(p)

    for p in planets:
        if p is not dragging_planet:
            p.update(dt, planets)

    screen.fill((10, 10, 15))

    if mouse_down and not dragging_planet:
        pygame.draw.line(screen, (200, 200, 255),
                         mouse_down_pos, mouse_pos, 2)
        pygame.draw.circle(screen, (200, 200, 255),
                           (int(mouse_down_pos.x), int(mouse_down_pos.y)), 8, 1)

    for p in planets:
        pygame.draw.circle(screen, p.color,
                           (int(p.pos.x), int(p.pos.y)), p.radius)

    pygame.display.flip()

pygame.quit()

