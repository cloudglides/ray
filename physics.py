from typing import List
import pygame
from constants import G, INTEGRATOR_EULER, INTEGRATOR_VERLET


def gravity_acceleration(
    pos: pygame.Vector2,
    other_pos: pygame.Vector2,
    other_mass: float,
    min_dist: float = 1.0
) -> pygame.Vector2:
    r = other_pos - pos
    dist = max(r.length(), min_dist)
    acc_mag = G * other_mass / (dist * dist)
    return r.normalize() * acc_mag


def calculate_total_acceleration(
    pos: pygame.Vector2,
    bodies: List["Body"],
    self_id: int,
    min_dist: float = 1.0
) -> pygame.Vector2:
    acc = pygame.Vector2()
    for body in bodies:
        if id(body) == self_id:
            continue
        acc += gravity_acceleration(pos, body.pos, body.mass, min_dist)
    return acc


def integrate_euler(
    body: "Body",
    bodies: List["Body"],
    dt: float
) -> None:
    acc = calculate_total_acceleration(body.pos, bodies, id(body), body.radius)
    body.vel += acc * dt
    body.pos += body.vel * dt


def integrate_verlet(
    body: "Body",
    bodies: List["Body"],
    dt: float
) -> None:
    if body._old_pos is None:
        body._old_pos = body.pos - body.vel * dt
    
    acc = calculate_total_acceleration(body.pos, bodies, id(body), body.radius)
    old_pos = body.pos.copy()
    
    body.pos = body.pos * 2 - body._old_pos + acc * (dt * dt)
    body.vel = (body.pos - old_pos) / dt
    body._old_pos = old_pos


INTEGRATORS = {
    INTEGRATOR_EULER: integrate_euler,
    INTEGRATOR_VERLET: integrate_verlet,
}


def get_integrator(method: str):
    if method not in INTEGRATORS:
        raise ValueError(f"Unknown integrator: {method}")
    return INTEGRATORS[method]


def orbital_velocity(central_mass: float, distance: float) -> float:
    return (G * central_mass / distance) ** 0.5
