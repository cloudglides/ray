import pygame
import math
from engine.physics.gravity import G
from engine.physics.trajectory import predict_trajectory

def predict_moon_trajectory(moon, planet, all_bodies, steps=2000, dt=0.01):
    pos = moon.pos.copy()
    vel = moon.vel.copy()
    path = []
    
    for _ in range(steps):
        acc = pygame.Vector2(0, 0)
        r = planet.pos - pos
        dist = max(r.length(), moon.radius + planet.radius)
        acc += r.normalize() * (G * planet.mass / (dist * dist))
        
        vel += acc * dt
        pos += vel * dt
        path.append(pos.copy())
    
    return path

def calculate_ideal_orbit(body, center, segments=300):
    r_vec = body.pos - center.pos
    radius = r_vec.length()
    
    if radius < 1:
        return []
    
    orbit_points = []
    for i in range(segments):
        angle = 2 * math.pi * i / segments
        x = center.pos.x + radius * math.cos(angle)
        y = center.pos.y + radius * math.sin(angle)
        orbit_points.append(pygame.Vector2(x, y))
    
    return orbit_points

def check_and_merge_collisions(bodies):
    merged = False
    i = 0
    while i < len(bodies):
        j = i + 1
        while j < len(bodies):
            body1 = bodies[i]
            body2 = bodies[j]
            
            if body1.is_colliding(body2):
                if body1.mass >= body2.mass:
                    larger, smaller = body1, body2
                else:
                    larger, smaller = body2, body1
                
                total_mass = larger.mass + smaller.mass
                new_vel = (larger.vel * larger.mass + smaller.vel * smaller.mass) / total_mass
                
                larger.pos = (larger.pos * larger.mass + smaller.pos * smaller.mass) / total_mass
                larger.vel = new_vel
                larger.mass = total_mass
                
                larger.radius = (larger.radius ** 3 + smaller.radius ** 3) ** (1/3)
                
                larger.color = tuple(int((larger.color[i] * (larger.mass - smaller.mass) + smaller.color[i] * smaller.mass) / larger.mass) for i in range(3))
                
                bodies.pop(j if larger is bodies[i] else i)
                merged = True
                break
            j += 1
        if not merged:
            i += 1
        else:
            merged = False

def calc_total_energy(bodies):
    ke = sum(0.5 * b.mass * (b.vel.x**2 + b.vel.y**2) for b in bodies)
    pe = 0
    for i, b1 in enumerate(bodies):
        for b2 in bodies[i+1:]:
            dist = b1.pos.distance_to(b2.pos)
            if dist > 0:
                pe -= G * b1.mass * b2.mass / dist
    return ke + pe
