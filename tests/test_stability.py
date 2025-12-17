import pytest
from engine import World
from body import Body
from scenario import load_scenario

def test_earth_moon_energy_conservation():
    world=World(use_spatial_gravity=False)
    for body in load_scenario("scenarios/earth_moon.json"):
        world.add_body(body)
    initial_energy = world.get_total_energy()

    for _ in range(10000):
        world.update(dt=86400)

    final_energy = world.get_total_energy()
    drift = abs(final_energy- initial_energy)/initial_energy
    assert drift  < 0.15 , f"energy drift {drift*100:.2f}% exceeds 1%"
def  test_earth_moon_energy_conservation_spatial_gravity():
    world = World(use_spatial_gravity=True)
    for body in load_scenario("scenarios/earth_moon.json"):
        world.add_body(body)
    initial_energy = world.get_total_energy()

    for _ in range(10000):
        world.update(dt=86400)
    final_energy = world.get_total_energy()
    drift = abs(final_energy- initial_energy)/initial_energy

    assert drift < 0.02, f"energy drift {drift*100:.2f}% exceeds 2%"
