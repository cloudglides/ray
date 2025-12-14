import pygame
import math
import random
from engine.entities.planet import Planet
from engine.entities.moon import Moon
from engine.entities.satellite import Satellite
from engine.physics.gravity import G

CENTER = pygame.Vector2(700, 450)

def create_starfield(count=200, width=3000, height=2000):
    stars = []
    for _ in range(count):
        x = random.uniform(-width // 2, width // 2)
        y = random.uniform(-height // 2, height // 2)
        brightness = random.randint(50, 200)
        stars.append((x, y, brightness))
    return stars

def create_solar_system():
    sun = Planet(*CENTER, mass=1989000, radius=25, color=(255, 220, 80))
    sun.name = "Sun"

    mercury = Planet(CENTER.x + 100, CENTER.y + 10, mass=0.330, radius=4, color=(150, 150, 150))
    mercury.vel = pygame.Vector2(0, -math.sqrt(G * sun.mass / 100))
    mercury.name = "Mercury"

    venus = Planet(CENTER.x + 190, CENTER.y - 20, mass=4.87, radius=7, color=(220, 180, 80))
    venus.vel = pygame.Vector2(0, -math.sqrt(G * sun.mass / 190))
    venus.name = "Venus"

    earth = Planet(CENTER.x + 280, CENTER.y + 30, mass=5.97, radius=8, color=(80, 120, 255))
    earth.vel = pygame.Vector2(0, -math.sqrt(G * sun.mass / 280))
    earth.name = "Earth"

    moon = Moon(earth.pos.x + 20, earth.pos.y, mass=0.073, radius=3, color=(200, 200, 200), parent=earth)
    moon_offset = moon.pos - earth.pos
    moon_tangent = pygame.Vector2(-moon_offset.y, moon_offset.x).normalize()
    moon_v_orbit = math.sqrt(G * earth.mass / moon_offset.length())
    moon.vel = earth.vel + moon_tangent * moon_v_orbit
    moon.name = "Moon"

    mars = Planet(CENTER.x + 380, CENTER.y - 40, mass=0.642, radius=5, color=(200, 80, 60))
    mars.vel = pygame.Vector2(0, -math.sqrt(G * sun.mass / 380) * 0.97)
    mars.name = "Mars"

    phobos = Moon(mars.pos.x + 15, mars.pos.y, mass=0.0001, radius=2, color=(120, 120, 120), parent=mars)
    phobos_offset = phobos.pos - mars.pos
    phobos_tangent = pygame.Vector2(-phobos_offset.y, phobos_offset.x).normalize()
    phobos_v_orbit = math.sqrt(G * mars.mass / phobos_offset.length())
    phobos.vel = mars.vel + phobos_tangent * phobos_v_orbit
    phobos.name = "Phobos"

    jupiter = Planet(CENTER.x + 600, CENTER.y + 50, mass=1898, radius=20, color=(200, 150, 80))
    jupiter.vel = pygame.Vector2(0, -math.sqrt(G * sun.mass / 600))
    jupiter.name = "Jupiter"

    io = Moon(jupiter.pos.x + 35, jupiter.pos.y, mass=0.893, radius=4, color=(255, 200, 100), parent=jupiter)
    io_offset = io.pos - jupiter.pos
    io_tangent = pygame.Vector2(-io_offset.y, io_offset.x).normalize()
    io_v_orbit = math.sqrt(G * jupiter.mass / io_offset.length())
    io.vel = jupiter.vel + io_tangent * io_v_orbit
    io.name = "Io"

    europa = Moon(jupiter.pos.x + 50, jupiter.pos.y - 15, mass=0.480, radius=3, color=(100, 150, 200), parent=jupiter)
    europa_offset = europa.pos - jupiter.pos
    europa_tangent = pygame.Vector2(-europa_offset.y, europa_offset.x).normalize()
    europa_v_orbit = math.sqrt(G * jupiter.mass / europa_offset.length())
    europa.vel = jupiter.vel + europa_tangent * europa_v_orbit
    europa.name = "Europa"

    saturn = Planet(CENTER.x + 900, CENTER.y - 30, mass=568, radius=18, color=(220, 200, 120))
    saturn.vel = pygame.Vector2(0, -math.sqrt(G * sun.mass / 900))
    saturn.name = "Saturn"

    titan = Moon(saturn.pos.x + 40, saturn.pos.y, mass=1.345, radius=4, color=(180, 150, 100), parent=saturn)
    titan_offset = titan.pos - saturn.pos
    titan_tangent = pygame.Vector2(-titan_offset.y, titan_offset.x).normalize()
    titan_v_orbit = math.sqrt(G * saturn.mass / titan_offset.length())
    titan.vel = saturn.vel + titan_tangent * titan_v_orbit
    titan.name = "Titan"

    uranus = Planet(CENTER.x + 1200, CENTER.y + 45, mass=86.8, radius=13, color=(100, 200, 220))
    uranus.vel = pygame.Vector2(0, -math.sqrt(G * sun.mass / 1200))
    uranus.name = "Uranus"

    titania = Moon(uranus.pos.x + 30, uranus.pos.y, mass=0.0352, radius=2, color=(150, 180, 200), parent=uranus)
    titania_offset = titania.pos - uranus.pos
    titania_tangent = pygame.Vector2(-titania_offset.y, titania_offset.x).normalize()
    titania_v_orbit = math.sqrt(G * uranus.mass / titania_offset.length())
    titania.vel = uranus.vel + titania_tangent * titania_v_orbit
    titania.name = "Titania"

    neptune = Planet(CENTER.x + 1500, CENTER.y - 35, mass=102, radius=12, color=(50, 100, 255))
    neptune.vel = pygame.Vector2(0, -math.sqrt(G * sun.mass / 1500))
    neptune.name = "Neptune"

    triton = Moon(neptune.pos.x + 25, neptune.pos.y, mass=0.214, radius=2, color=(180, 180, 220), parent=neptune)
    triton_offset = triton.pos - neptune.pos
    triton_tangent = pygame.Vector2(-triton_offset.y, triton_offset.x).normalize()
    triton_v_orbit = math.sqrt(G * neptune.mass / triton_offset.length())
    triton.vel = neptune.vel + triton_tangent * triton_v_orbit
    triton.name = "Triton"

    # Create controllable satellite in Earth orbit
    satellite = Satellite(earth.pos + pygame.Vector2(30, 0), pygame.Vector2(0, -6.5), mass=0.001)
    satellite.name = "Satellite"

    return [sun, mercury, venus, earth, moon, mars, phobos, jupiter, io, europa, saturn, titan, uranus, titania, neptune, triton], satellite
