from typing import List
from constants import G, INTEGRATOR_EULER, INTEGRATOR_VERLET
from type_defs import Vector2
INTEGRATOR_RK4 = "rk4"
def gravity_acceleration(
    pos: Vector2,
    other_pos: Vector2,
    other_mass: float,
    min_dist: float = 1.0
) -> Vector2:
    r = other_pos - pos
    dist = max(r.length(), min_dist)
    acc_mag = G * other_mass / (dist * dist)
    return r.normalize() * acc_mag
def calculate_total_acceleration(pos, bodies, self_id, spatial_grid=None, cell_size=None, min_dist=1.0):
    acc = Vector2()
    if spatial_grid is None:
        nearby=bodies
    else:
        nearby = spatial_grid.query_radius(pos, cell_size*2)
    for body in nearby:
        if id(body) == self_id:
            continue
        acc+=gravity_acceleration(pos, body.pos, body.mass, min_dist)
    return acc
def integrate_euler(
    body: "Body",
    bodies: List["Body"],
    dt: float,
    spatial_grid=None,
    cell_size=1e8
):
    acc = calculate_total_acceleration(body.pos, bodies, id(body), spatial_grid, cell_size, body.radius)
    body.vel += acc * dt
    body.pos += body.vel * dt
def integrate_verlet(
    body: "Body",
    bodies: List["Body"],
    dt: float,
    spatial_grid=None,
    cell_size=1e8
):
    if body._old_pos is None:
        body._old_pos = body.pos - body.vel * dt
    acc = calculate_total_acceleration(body.pos, bodies, id(body), spatial_grid, cell_size, body.radius)
    old_pos = body.pos.copy()
    body.pos = body.pos * 2 - body._old_pos + acc * (dt * dt)
    body.vel = (body.pos - old_pos) / dt
    body._old_pos = old_pos
def integrate_rk4(
    body: "Body",
    bodies: List["Body"],
    dt: float,
    spatial_grid=None,
    cell_size=1e8
) -> None:
    self_id = id(body)
    min_dist = body.radius
    k1_vel = body.vel
    k1_acc = calculate_total_acceleration(body.pos, bodies, self_id, spatial_grid, cell_size, min_dist)
    k2_pos = body.pos + k1_vel * (0.5 * dt)
    k2_vel = body.vel + k1_acc * (0.5 * dt)
    k2_acc = calculate_total_acceleration(k2_pos, bodies, self_id, spatial_grid, cell_size, min_dist)
    k3_pos = body.pos + k2_vel * (0.5 * dt)
    k3_vel = body.vel + k2_acc * (0.5 * dt)
    k3_acc = calculate_total_acceleration(k3_pos, bodies, self_id, spatial_grid, cell_size, min_dist)
    k4_pos = body.pos + k3_vel * dt
    k4_vel = body.vel + k3_acc * dt
    k4_acc = calculate_total_acceleration(k4_pos, bodies, self_id, spatial_grid, cell_size, min_dist)
    body.pos += (k1_vel + k2_vel * 2 + k3_vel * 2 + k4_vel) * (dt / 6.0)
    body.vel += (k1_acc + k2_acc * 2 + k3_acc * 2 + k4_acc) * (dt / 6.0)
INTEGRATORS = {
    INTEGRATOR_EULER: integrate_euler,
    INTEGRATOR_VERLET: integrate_verlet,
    INTEGRATOR_RK4: integrate_rk4,
}
def get_integrator(method: str):
    if method not in INTEGRATORS:
        raise ValueError(f"Unknown integrator: {method}")
    return INTEGRATORS[method]
def orbital_velocity(central_mass: float, distance: float) -> float:
    return (G * central_mass / distance) ** 0.5
