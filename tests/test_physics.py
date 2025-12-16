import pytest
from type_defs import Vector2
from physics import gravity_acceleration, orbital_velocity
from constants import G


def test_vector2_add():
    v1 = Vector2(1, 2)
    v2 = Vector2(3, 4)
    result = v1 + v2
    assert result.x == 4
    assert result.y == 6


def test_vector2_sub():
    v1 = Vector2(5, 7)
    v2 = Vector2(2, 3)
    result = v1 - v2
    assert result.x == 3
    assert result.y == 4


def test_vector2_mul():
    v = Vector2(2, 3)
    result = v * 2
    assert result.x == 4
    assert result.y == 6


def test_vector2_length():
    v = Vector2(3, 4)
    assert v.length() == 5.0


def test_vector2_normalize():
    v = Vector2(3, 4)
    normalized = v.normalize()
    assert abs(normalized.length() - 1.0) < 1e-10


def test_vector2_distance():
    v1 = Vector2(0, 0)
    v2 = Vector2(3, 4)
    assert v1.distance_to(v2) == 5.0


def test_gravity_acceleration_magnitude():
    earth_pos = Vector2(0, 0)
    moon_pos = Vector2(1e8, 0)
    earth_mass = 5.972e24
    
    acc = gravity_acceleration(moon_pos, earth_pos, earth_mass)
    
    expected_mag = G * earth_mass / (1e8 ** 2)
    actual_mag = acc.length()
    
    assert abs(actual_mag - expected_mag) < 1e-10


def test_gravity_acceleration_direction():
    earth_pos = Vector2(0, 0)
    moon_pos = Vector2(1e8, 0)
    earth_mass = 5.972e24
    
    acc = gravity_acceleration(moon_pos, earth_pos, earth_mass)
    
    assert acc.x < 0
    assert acc.y == 0


def test_orbital_velocity():
    earth_mass = 5.972e24
    orbit_radius = 384400e3
    
    v = orbital_velocity(earth_mass, orbit_radius)
    
    expected = (G * earth_mass / orbit_radius) ** 0.5
    
    assert abs(v - expected) < 1e-6


def test_gravity_zero_distance_clamped():
    pos = Vector2(0, 0)
    other_pos = Vector2(0, 0)
    mass = 1e24
    min_dist = 1.0
    
    acc = gravity_acceleration(pos, other_pos, mass, min_dist)
    
    expected_mag = G * mass / (min_dist ** 2)
    
    assert acc.length() == expected_mag or acc.length() == 0
