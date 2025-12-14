import pygame

G = 6.67430e-11 * 1e4

def gravity_force(a, b):
    r = b.pos - a.pos
    dist = max(r.length(), 5)
    force_mag = G * a.mass * b.mass / (dist * dist)
    return r.normalize() * force_mag

def gravity_acceleration(pos, planet):
    r = planet.pos - pos
    dist = max(r.length(), 5)
    acc_mag = G * planet.mass / (dist * dist)
    return r.normalize() * acc_mag

