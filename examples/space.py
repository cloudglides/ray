import pygame
from engine.entities.planet import Planet
from engine.entities.satellite import Satellite
from engine.physics.gravity import gravity_acceleration
from engine.physics.orbit import circular_orbit_velocity
from engine.physics.trajectory import predict
from engine.render.orbit_draw import draw_orbit

pygame.init()
screen = pygame.display.set_mode((900, 700))
clock = pygame.time.Clock()

star = Planet(450, 350, radius=60, mass=60000)

r = 180
v = circular_orbit_velocity(star.mass, r)

satellites = [
    Satellite(
        pos=star.pos + pygame.Vector2(r, 0),
        vel=pygame.Vector2(0, -v)
    )
]

running = True
while running:
    dt = clock.tick(60) / 1000

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    screen.fill((8, 10, 16))

    pygame.draw.circle(screen, (100, 100, 100), (int(star.pos.x), int(star.pos.y)), r, 1)
    for s in satellites:
        path = predict(s.pos, s.vel, [star], steps=4000, dt=0.05)
        draw_orbit(screen, path)

    for s in satellites:
        acc = gravity_acceleration(s.pos, star)
        s.update(acc, dt)

    star.draw(screen)
    for s in satellites:
        s.draw(screen)

    pygame.display.flip()

pygame.quit()

