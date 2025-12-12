import pygame
import time
from engine.ball import Ball


ay = 500 
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball")
clock = pygame.time.Clock()


balls = []


# main loop
running = True
prev_time = time.time()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            balls.append(Ball(mx, my, ay, width=WIDTH, height=HEIGHT)) 
    now = time.time()
    dt = now - prev_time
    prev_time = now

    for b in balls:
        b.update(dt)
        for i in range(len(balls)):
            for j in range(i + 1, len(balls)):
                b1 = balls[i]
                b2 = balls[j]

                dx = b1.x - b2.x
                dy = b1.y - b2.y
                distance = (dx**2 + dy**2) ** 0.5

                if distance < b1.radius + b2.radius:
                    b1.vx, b2.vx = b2.vx, b1.vx
                    b1.vy, b2.vy = b2.vy, b1.vy


    screen.fill((30, 30, 30))

    for b in balls:
        pygame.draw.circle(screen, b.color, (int(b.x), int(b.y)), b.radius) 
    pygame.display.flip() 
    clock.tick(60)        # 60 FPS

pygame.quit()


