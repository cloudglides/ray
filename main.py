import pygame
from body import Body
from scenario import load_scenario
from constants import DISPLAY_SCALE

pygame.init()
W, H = 1000, 700
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)
bodies = load_scenario("scenarios/earth_moon.json")
paused = False
time_scale = 1.0
selected_body = None
if bodies:
    cm_x = sum(b.pos.x * b.mass for b in bodies) / sum(b.mass for b in bodies)
    cm_y = sum(b.pos.y * b.mass for b in bodies) / sum(b.mass for b in bodies)
    max_dist = max(
        max(abs(b.pos.x - cm_x) for b in bodies),
        max(abs(b.pos.y - cm_y) for b in bodies),
    )
    zoom = min(W, H) / (2.5 * max_dist / DISPLAY_SCALE) if max_dist > 0 else 1.0
    zoom = max(0.001, min(zoom, 1000))
    pan_x = W // 2 - int((cm_x / DISPLAY_SCALE) * zoom)
    pan_y = H // 2 - int((cm_y / DISPLAY_SCALE) * zoom)
else:
    pan_x, pan_y = 0, 0
    zoom = 1.0
running = True
while running:
    dt = clock.tick(60) / 1000.0
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
                time_scale = 50000.0
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
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = pygame.mouse.get_pos()
            for body in bodies:
                scaled_x = pan_x + int((body.pos.x / DISPLAY_SCALE) * zoom)
                scaled_y = pan_y + int((body.pos.y / DISPLAY_SCALE) * zoom)
                scaled_radius = max(1, int((body.radius / DISPLAY_SCALE) * zoom))
                dist = ((x - scaled_x) ** 2 + (y - scaled_y) ** 2) ** 0.5
                if dist < scaled_radius:
                    selected_body = body
                    break
    if not paused:
        substeps = min(10, max(1, int(time_scale / 100)))
        for _ in range(substeps):
            for body in bodies:
                body.update(bodies, (dt * time_scale) / substeps)
    if selected_body:
        info = f"mass:{selected_body.mass:.2e} | speed:{selected_body.speed():.1f} m/s"
        text = font.render(info, True, (255, 255, 0))
        screen.blit(text, (10, 70))
    for i, body in enumerate(bodies):
        scaled_x = pan_x + int((body.pos.x / DISPLAY_SCALE) * zoom)
        scaled_y = pan_y + int((body.pos.y / DISPLAY_SCALE) * zoom)
        scaled_radius = max(1, int((body.radius / DISPLAY_SCALE) * zoom))
        if -50 <= scaled_x < W + 50 and -50 <= scaled_y < H + 50:
            pygame.draw.circle(screen, body.color, (scaled_x, scaled_y), scaled_radius)
    status = "PAUSED" if paused else f"RUNNING {time_scale:.0f}x"
    text = font.render(status, True, (255, 255, 255))
    screen.blit(text, (10, 10))
    info = f"Bodies: {len(bodies)} | FPS: {int(clock.get_fps())} | Zoom: {zoom:.2f}x"
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
