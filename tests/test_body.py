import pytest
from body import Body 
from exceptions import InvalidBodyError 


def test_body_init():
    b = Body(x=0,y=0,mass=1e24,radius=1e6)
    assert b.pos.x == 0
    assert b.pos.y == 0
    assert b.mass == 1e24
    assert b.radius == 1e6 
def test_body_invalid_mass():
    with pytest.raises(InvalidBodyError):
        Body(x=0,y=0,mass=-100,radius=1e6)
def test_body_invalid_radius():
    with pytest.raises(InvalidBodyError):
        Body(x=0,y=0,mass=1e24,radius=-1e6)
def test_body_kinetic_energy():
    b = Body(x=0,y=0,mass=100,radius=10, vx=2, vy=0)
    ke = b.kinetic_energy()
    expected = 0.5*100*(2**2 + 0**2)
    assert ke == expected
def test_body_speed():
    b = Body(x=0,y=0,mass=100, radius=10, vx=3, vy=4)
    assert b.speed() == 5.0
def test_body_collision_same_body():
    b = Body(x=0,y=0,mass=100,radius=10)
    assert b.is_colliding(b) == False
def test_body_collision_overlapping():
    b1 = Body(x=0,y=0,mass=100,radius=10)
    b2 = Body(x=5,y=0,mass=100,radius=10)
    assert b1.is_colliding(b2) == True
def test_body_collision_not_overlapping():
    b1 = Body(x=0,y=0,mass=100,radius=10)
    b2 = Body(x=100,y=0,mass=100,radius=10)
    assert b1.is_colliding(b2) == False
def test_body_distance_to():
    b1 = Body(x=0,y=0,mass=100,radius=10)
    b2 = Body(x=3,y=4,mass=100,radius=10)
    assert b1.distance_to(b2) == 5.0
    

