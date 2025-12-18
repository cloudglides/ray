import pytest
from ray.engine import World
from ray.body import Body


def test_world_init():
    w = World()
    assert len(w.bodies) == 0


def test_world_add_body():
    w = World()
    b = Body(x=0, y=0, mass=100, radius=10)
    w.add_body(b)
    assert len(w.bodies) == 1
    assert w.bodies[0] == b


def test_world_total_energy_single_body():
    w = World()
    b = Body(x=0, y=0, mass=100, radius=10, vx=10, vy=0)
    w.add_body(b)
    energy = w.get_total_energy()
    expected = 0.5 * 100 * (10**2)
    assert energy == expected


def test_world_total_energy_multiple_bodies():
    w = World()
    b1 = Body(x=0, y=0, mass=100, radius=10, vx=2, vy=0)
    b2 = Body(x=10, y=0, mass=50, radius=5, vx=4, vy=0)
    w.add_body(b1)
    w.add_body(b2)
    energy = w.get_total_energy()
    expected = (0.5 * 100 * 4) + (0.5 * 50 * 16)
    assert energy == expected


def test_world_total_momentum():
    w = World()
    b1 = Body(x=0, y=0, mass=100, radius=10, vx=1, vy=0)
    b2 = Body(x=10, y=0, mass=100, radius=10, vx=2, vy=0)
    w.add_body(b1)
    w.add_body(b2)
    p = w.get_total_momentum()
    assert p.x == 300
    assert p.y == 0


def test_world_collision_detection():
    w = World()
    b1 = Body(x=0, y=0, mass=100, radius=10)
    b2 = Body(x=5, y=0, mass=100, radius=10)
    w.add_body(b1)
    w.add_body(b2)
    w.check_collisions()
