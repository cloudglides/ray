import pygame
import sys

from engine.rocket import Rocket
from engine.space.planet import Planet
from components.slider import Slider

pygame.init()


WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Orbital Physics Sandbox")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 18)


planets = [
    Planet(450, 300, radius=20, mass=90000),
]

rockets = []
selected_rocket = None


thrust_slider = Slider(
    x=20, y=110, w=220,
    min_val=-2500, max_val=2500,
    start_val=0
)

ay_slider = Slider(
    x=20, y=170, w=220,
    min_val=-20, max_val=20,
    start_val=0
)


def draw_text(text, x, y):
    screen.blit(font.render(text, True, (230, 230, 230)), (x, y))


running = True
while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if selected_rocket:
            thrust_slider.handle_event(event)
            ay_slider.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.Vector2(event.pos)

            if event.button == 3:
                rockets.append(
                    Rocket(
                        x=mouse.x,
                        y=mouse.y,
                        mass=50,
                        velocity=(0, -180)
                    )
                )

            if event.button == 1:
                selected_rocket = None
                for r in rockets:
                    r.selected = False
                    if r.contains_point(mouse):
                        r.selected = True
                        selected_rocket = r
                        break

    for r in rockets:
        for p in planets:
            direction = p.pos - r.pos
            distance = direction.length()

            safe_dist = max(distance, p.radius + 8)

            force_mag = (p.mass * r.mass) / (safe_dist * safe_dist)
            r.apply_force(direction.normalize() * force_mag)

            if distance < p.radius:
                normal = direction.normalize()
                r.pos = p.pos - normal * p.radius

                vn = r.velocity.dot(normal)
                if vn > 0:
                    r.velocity -= normal * vn

        if r == selected_rocket:
            r.apply_force(pygame.Vector2(0, ay_slider.value) * r.mass)
            r.apply_force(pygame.Vector2(0, -thrust_slider.value))

        r.update(dt)

    screen.fill((8, 10, 20))

    for p in planets:
        pygame.draw.circle(screen, (120, 150, 255), p.pos, p.radius)

    if selected_rocket:
        path = selected_rocket.predict_trajectory(
            planets,
            steps=900,
            dt=0.02
        )

        if len(path) > 1:
            pygame.draw.lines(
                screen,
                (255, 255, 255),
                False,
                path,
                1
            )

    for r in rockets:
        r.draw(screen)

    if selected_rocket:
        draw_text("Rocket Inspector", 20, 30)

        draw_text(f"Thrust", 20, 90)
        thrust_slider.draw(screen)
        draw_text(f"{thrust_slider.value:.1f}", 260, 110)

        draw_text(f"ay", 20, 150)
        ay_slider.draw(screen)
        draw_text(f"{ay_slider.value:.2f}", 260, 170)

        draw_text(
            f"Speed: {selected_rocket.velocity.length():.2f}",
            20, 230
        )

    draw_text("Right click: spawn rocket", 20, HEIGHT - 40)
    draw_text("Left click: select rocket", 20, HEIGHT - 20)

    pygame.display.flip()

pygame.quit()
sys.exit()

