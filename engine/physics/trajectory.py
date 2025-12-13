import pygame
from engine.physics.gravity import G

def predict_trajectory(body, bodies, steps=3000, dt=0.005):
    pos = body.pos.copy()
    vel = body.vel.copy()
    path = []

    for _ in range(steps):
        acc = pygame.Vector2()
        for other in bodies:
            if other is body:
                continue
            r = other.pos - pos
            dist = max(r.length(), body.radius + other.radius)
            acc += r.normalize() * (G * other.mass / (dist * dist))

        vel += acc * dt
        pos += vel * dt
        path.append(pos.copy())

    return path

predict = predict_trajectory

