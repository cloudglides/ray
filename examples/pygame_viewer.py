import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import pygame
import random
import math
from ray.engine import World
from ray.scenario import load_scenario
from ray.constants import DISPLAY_SCALE
from ray.particle import Particle
from ray.validators import EnergyTracker, MomentumTracker
from ray.type_defs import Vector2
from ray.renderer import BodyRenderer

pygame.init()
W, H = 1000, 700
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)


world = World()
try:
    for body in load_scenario("scenarios/earth_moon.json"):
        world.add_body(body)
        print(f"{body} -> speed: {body.speed():.2f} m/s")
except RayError as e:
    print(f"Error loading scenario {e}")

energy_tracker = EnergyTracker(world)
momentum_tracker = MomentumTracker(world)

paused = False
time_scale = 1.0
selected_body = None
particles = []
if world.bodies:
    cm_x = sum(b.pos.x * b.mass for b in world.bodies) / sum(
        b.mass for b in world.bodies
    )
    cm_y = sum(b.pos.y * b.mass for b in world.bodies) / sum(
        b.mass for b in world.bodies
    )
    max_dist = max(
        max(abs(b.pos.x - cm_x) for b in world.bodies),
        max(abs(b.pos.y - cm_y) for b in world.bodies),
    )
    zoom = min(W, H) / (2.5 * max_dist / DISPLAY_SCALE) if max_dist > 0 else 1.0
    zoom = max(0.001, min(zoom, 1000))
    pan_x = W // 2 - int((cm_x / DISPLAY_SCALE) * zoom)
    pan_y = H // 2 - int((cm_y / DISPLAY_SCALE) * zoom)
else:
    pan_x, pan_y = 0, 0
    zoom = 1.0
running = True
frame_count = 0
while running:
    dt = clock.tick(60) / 1000.0
    frame_count += 1
    screen.fill((10, 10, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            if event.key == pygame.K_r:
                zoom = 1.0
                pan_x, pan_y = 0, 0
            if event.key == pygame.K_1:
                time_scale = 1.0
            if event.key == pygame.K_5:
                time_scale = 50.0
            if event.key == pygame.K_0:
                time_scale = 500000.0
            if event.key == pygame.K_MINUS:
                zoom *= 0.9
            if event.key == pygame.K_EQUALS:
                zoom *= 1.1
            if event.key == pygame.K_UP:
                pan_y += 50
            if event.key == pygame.K_DOWN:
                pan_y -= 50
            if event.key == pygame.K_LEFT:
                pan_x += 50
            if event.key == pygame.K_RIGHT:
                pan_x -= 50
        if event.type == pygame.MOUSEWHEEL:
            zoom *= 1.1 if event.y > 0 else 0.9
        if event.type == pygame.MOUSEMOTION:
            if event.buttons[2]:
                pan_x += event.rel[0]
                pan_y += event.rel[1]

    particles = [p for p in particles if p.is_alive()]
    for p in particles:
        p.update(dt)
    for p in particles:
        scaled_x = pan_x + int((p.pos.x / DISPLAY_SCALE) * zoom)
        scaled_y = pan_y + int((p.pos.y / DISPLAY_SCALE) * zoom)
        alpha = p.alpha()
        if alpha > 0:
            particle_surf = pygame.Surface((10, 10), pygame.SRCALPHA)
            pygame.draw.circle(particle_surf, (*p.color, alpha), (5, 5), 5)
            screen.blit(particle_surf, (scaled_x - 5, scaled_y - 5))

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = pygame.mouse.get_pos()
            for body in world.bodies:
                BodyRenderer.draw_trail(screen, body, pan_x, pan_y, zoom, DISPLAY_SCALE)
                BodyRenderer.draw_body(screen, body, pan_x, pan_y, zoom, DISPLAY_SCALE)
                BodyRenderer.draw_velocity_vector(
                    screen, body, pan_x, pan_y, zoom, DISPLAY_SCALE
                )

    if not paused:
        substeps = min(10, max(1, int(time_scale / 100)))
        for _ in range(substeps):
            collisions = world.update((dt * time_scale) / substeps)
            bodies_to_destroy = set()
            for body1, body2 in collisions:
                bodies_to_destroy.add(body1)
                bodies_to_destroy.add(body2)
                collision_pos = (body1.pos + body2.pos) * 0.5
                particles.append(
                    Particle(
                        collision_pos, Vector2(0, 0), 0.05, (255, 255, 255), "flash"
                    )
                )
                for _ in range(30):
                    angle = random.uniform(0, 2 * math.pi)
                    vel = Vector2(math.cos(angle), math.sin(angle)) * random.uniform(
                        6e6, 1e7
                    )
                    particles.append(
                        Particle(collision_pos, vel, 5.0, (200, 100, 0), "shards")
                    )
                for _ in range(60):
                    angle = random.uniform(0, 2 * math.pi)
                    vel = Vector2(math.cos(angle), math.sin(angle)) * random.uniform(
                        2e6, 4e6
                    )
                    particles.append(
                        Particle(collision_pos, vel, 2.0, (150, 150, 150), "dust")
                    )
                for _ in range(20):
                    angle = random.uniform(0, 2 * math.pi)
                    vel = Vector2(math.cos(angle), math.sin(angle)) * 1.5e7
                    particles.append(
                        Particle(collision_pos, vel, 0.3, (255, 150, 0), "spark")
                    )
            for body in bodies_to_destroy:
                if body in world.bodies:
                    world.bodies.remove(body)

        energy_tracker.update()
        momentum_tracker.update()
        if frame_count % 100 == 0:
            energy_tracker.check_drift(1.0)
            momentum_tracker.check_drift(1e15)
        if len(world.bodies) > 1:
            dist = world.bodies[0].distance_to(world.bodies[1])
            if dist < 1e8:
                pass
                # print(f"WARNING: Distance collapsed to {dist:.2e}")
    if selected_body:
        info = f"mass:{selected_body.mass:.2e} | speed:{selected_body.speed():.1f} m/s"
        text = font.render(info, True, (255, 255, 0))
        screen.blit(text, (10, 70))
    for i, body in enumerate(world.bodies):
        scaled_x = pan_x + int((body.pos.x / DISPLAY_SCALE) * zoom)
        scaled_y = pan_y + int((body.pos.y / DISPLAY_SCALE) * zoom)
        scaled_radius = max(1, int((body.radius / DISPLAY_SCALE) * zoom))
        if -50 <= scaled_x < W + 50 and -50 <= scaled_y < H + 50:
            pygame.draw.circle(screen, body.color, (scaled_x, scaled_y), scaled_radius)
    status = "PAUSED" if paused else f"RUNNING {time_scale:.0f}x"
    text = font.render(status, True, (255, 255, 255))
    screen.blit(text, (10, 10))
    info = (
        f"Bodies: {len(world.bodies)} | FPS: {int(clock.get_fps())} | Zoom: {zoom:.2f}x"
    )
    info_text = font.render(info, True, (200, 200, 200))
    screen.blit(info_text, (10, 40))
    help_text = font.render(
        "SPACE: pause | 1/5/0: speed | -/+: zoom | Arrows: pan | R: reset | Click: select",
        True,
        (150, 150, 150),
    )
    screen.blit(help_text, (10, H - 30))
    pygame.display.flip()
pygame.quit()
