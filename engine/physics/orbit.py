import math
from engine.physics.gravity import G


def circular_orbit_velocity(central_mass, radius):

    if radius <= 0:
        return 0.0

    return math.sqrt(G * central_mass / radius)

