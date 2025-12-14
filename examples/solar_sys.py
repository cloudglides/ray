import pygame
import random
import math
from engine.entities.planet import Planet
from engine.entities.moon import Moon
from engine.physics.trajectory import predict_trajectory
from engine.physics.gravity import G

pygame.init()
screen = pygame.display.set_mode((1400, 900))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 20)
title_font = pygame.font.Font(None, 28)

CENTER = pygame.Vector2(700, 450)

class Camera:
    def __init__(self, width, height):
        self.x = 0
        self.y = 0
        self.zoom = 1.0
        self.width = width
        self.height = height
        
    def to_screen(self, world_pos):
        screen_x = (world_pos.x - self.x) * self.zoom + self.width // 2
        screen_y = (world_pos.y - self.y) * self.zoom + self.height // 2
        return pygame.Vector2(screen_x, screen_y)
    
    def from_screen(self, screen_pos):
        world_x = (screen_pos.x - self.width // 2) / self.zoom + self.x
        world_y = (screen_pos.y - self.height // 2) / self.zoom + self.y
        return pygame.Vector2(world_x, world_y)
    
    def pan(self, dx, dy):
        self.x -= dx / self.zoom
        self.y -= dy / self.zoom
    
    def zoom_in(self, factor=1.2):
        self.zoom *= factor
        self.zoom = min(self.zoom, 10)
    
    def zoom_out(self, factor=1.2):
        self.zoom /= factor
        self.zoom = max(self.zoom, 0.1)
    
    def follow(self, target):
        self.x = target.pos.x
        self.y = target.pos.y

camera = Camera(1400, 900)
camera.x = CENTER.x
camera.y = CENTER.y
camera.zoom = 1.0  

def create_starfield(count=200, width=3000, height=2000):
    stars = []
    for _ in range(count):
        x = random.uniform(-width // 2, width // 2)
        y = random.uniform(-height // 2, height // 2)
        brightness = random.randint(50, 200)
        stars.append((x, y, brightness))
    return stars

stars = create_starfield()

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

bodies = [sun, mercury, venus, earth, moon, mars, phobos, jupiter, io, europa, saturn, titan, uranus, titania, neptune, triton]

TIME_SCALE = 0.01

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = (60, 60, 60)
        self.hover_color = (120, 120, 120)
        
    def draw(self, screen, font):
        color = self.hover_color if self.rect.collidepoint(pygame.mouse.get_pos()) else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        text_surf = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
        
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

buttons = [
    Button(10, 10, 80, 40, "Pause"),
    Button(100, 10, 80, 40, "1x"),
    Button(190, 10, 80, 40, "2x"),
    Button(280, 10, 80, 40, "5x"),
    Button(370, 10, 100, 40, "10x"),
    Button(480, 10, 100, 40, "500x"),
    Button(1280, 850, 100, 40, "reset")
]

running = True
paused = False
selected_body = None
followed_body = None
panning = False
pan_start = None
show_orbits = True
show_trajectories = True
show_help = True
orbit_cache = {}
trajectory_cache = {}
recalc_counter = 0
initial_camera_x = camera.x
initial_camera_y = camera.y
initial_zoom = camera.zoom
initial_body_count = len(bodies)
merged_count = 0


initial_states = [(b.pos.copy(), b.vel.copy()) for b in bodies]

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


speed_mult = 1.0
while running:
    dt = clock.tick(60) / 1000 * TIME_SCALE
    
    if paused:
        dt = 0

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.MOUSEBUTTONDOWN:
            pos = e.pos
            
            button_clicked = False
            if buttons[0].is_clicked(pos):
                paused = not paused
                button_clicked = True
            elif buttons[1].is_clicked(pos):
                TIME_SCALE = 0.01
                button_clicked = True
            elif buttons[2].is_clicked(pos):
                TIME_SCALE = 0.02
                button_clicked = True
            elif buttons[3].is_clicked(pos):
                TIME_SCALE = 0.05
                button_clicked = True
            elif buttons[4].is_clicked(pos):
                TIME_SCALE = 0.1
                button_clicked = True
            elif buttons[5].is_clicked(pos):
                TIME_SCALE = 50.0
                button_clicked = True
            elif buttons[6].is_clicked(pos):
                for i in range(min(len(bodies), len(initial_states))):
                    bodies[i].pos = initial_states[i][0].copy()
                    bodies[i].vel = initial_states[i][1].copy()
                selected_body = None
                followed_body = None
                button_clicked = True
            if not button_clicked:
                if e.button == 1:  
                    world_pos = camera.from_screen(pygame.Vector2(pos))
                    selected_body = None
                    followed_body = None
                    for b in bodies:
                        if world_pos.distance_to(b.pos) < 50:
                            selected_body = b
                            followed_body = b
                            camera.zoom = 0.8
                            break
                elif e.button == 3:  
                    panning = True
                    pan_start = pygame.Vector2(pos)
        
        elif e.type == pygame.MOUSEBUTTONUP:
            if e.button == 3:
                panning = False
        
        elif e.type == pygame.MOUSEMOTION:
            if panning and pan_start:
                dx = e.pos[0] - pan_start.x
                dy = e.pos[1] - pan_start.y
                camera.pan(dx, dy)
                pan_start = pygame.Vector2(e.pos)
        
        elif e.type == pygame.KEYDOWN: 
            if e.key == pygame.K_EQUALS or e.key == pygame.K_PLUS:
                camera.zoom_in(1.15)
            elif e.key == pygame.K_MINUS:
                camera.zoom_out(1.15)
            elif e.key == pygame.K_UP:
                camera.pan(0, 30)
            elif e.key == pygame.K_DOWN:
                camera.pan(0, -30)
            elif e.key == pygame.K_LEFT:
                camera.pan(30, 0)
            elif e.key == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                keys = pygame.key.get_mods()
    
            elif e.key == pygame.KMOD_ALT:  
                 new_planet = Planet(x, y, 100000, 5, (50, 50, 50))  
            elif e.key == pygame.K_RIGHT:
                camera.pan(-30, 0)
            elif e.key == pygame.K_o:
                show_orbits = not show_orbits
            elif e.key == pygame.K_t:
                show_trajectories = not show_trajectories
            elif e.key == pygame.K_h:
                show_help = not show_help
            elif e.key == pygame.K_f:
                screen = pygame.display.set_mode((1400, 900), pygame.FULLSCREEN)
            elif e.key == pygame.K_ESCAPE:
                screen = pygame.display.set_mode((1400,900))
            elif e.key == pygame.K_SPACE:
                paused = not paused
                button_clicked = True
                print(f"Key pressed")
            elif e.key == pygame.K_HOME:
                camera.x = initial_camera_x
                camera.y = initial_camera_y
                camera.zoom = initial_zoom
                followed_body = None
            elif e.key == pygame.K_f:
                followed_body = selected_body if selected_body else None
            elif e.key == pygame.K_ESCAPE:
                running = False

    for b in bodies:
        b.update(bodies, dt)
    
    check_and_merge_collisions(bodies)
    
    if selected_body not in bodies:
        selected_body = None
    if followed_body not in bodies:
        followed_body = None
    
    if followed_body:
        camera.follow(followed_body)

    screen.fill((8, 10, 16))

    for star in stars:
        screen_pos = camera.to_screen(pygame.Vector2(star[0], star[1]))
        if 0 <= screen_pos.x < 1400 and 0 <= screen_pos.y < 900:
            brightness = int(star[2] * (camera.zoom / 2))
            brightness = min(255, max(50, brightness))
            pygame.draw.circle(screen, (brightness, brightness, brightness), screen_pos, 1)

    recalc_counter += 1
    if recalc_counter >= 10:  
        recalc_counter = 0
        trajectory_cache.clear()
        
        if show_orbits:
            for b in bodies:
                if b is not sun:
                    ref = b.parent if (hasattr(b, 'parent') and b.parent) else sun
                    orbit_cache[id(b)] = calculate_ideal_orbit(b, ref)
        
        if show_trajectories:
            for b in bodies:
                trajectory_cache[id(b)] = predict_trajectory(b, bodies, steps=1500, dt=0.01)
    
    if show_orbits:
        for b in bodies:
            if id(b) in orbit_cache and b is not sun:
                path = orbit_cache[id(b)]
                if len(path) > 1:
                    path = path[::5]
                    screen_path = [camera.to_screen(p) for p in path]
                    if len(screen_path) > 1:
                        color = (150, 150, 150) if b.mass > 0.5 else (100, 100, 100)
                        pygame.draw.lines(
                            screen,
                            color,
                            True,
                            screen_path,
                            1
                        )
    
    if show_trajectories:
        for b in bodies:
            if id(b) in trajectory_cache:
                path = trajectory_cache[id(b)]
                if len(path) > 1:
                    path = path[::3]
                    screen_path = [camera.to_screen(p) for p in path]
                    if len(screen_path) > 1:
                        pygame.draw.lines(
                            screen,
                            (120, 120, 120),
                            False,
                            screen_path,
                            1
                        )

    for b in bodies:
        screen_pos = camera.to_screen(b.pos)
        radius = max(2, int(b.radius * camera.zoom))
        pygame.draw.circle(screen, b.color, screen_pos, radius)
        
        label = font.render(b.name, True, (255, 255, 255))
        screen.blit(label, (screen_pos.x + radius + 5, screen_pos.y - 10))

    for btn in buttons:
        btn.draw(screen, font)
    
    center_x, center_y = screen.get_width()//2, screen.get_height()//2 
    pygame.draw.line(screen, (80,80,80), (center_x - 10, center_y), (center_x+10,center_y), 1)
    pygame.draw.line(screen, (80,80,80), (center_x, center_y-10), (center_x,center_y+10), 1)
    
    panel_x = screen.get_width() - 320
    panel_y = 10
    panel_w = 310
    panel_h = 0
    
    ui_lines = []
    fps = clock.get_fps()
    ui_lines.append(f"FPS: {int(fps)}")
    ui_lines.append(f"Time: {TIME_SCALE:.2f}x | {'PAUSED' if paused else 'RUN'}")
    ui_lines.append(f"Zoom: {camera.zoom:.1f}x")
    ui_lines.append(f"Bodies: {len(bodies)}")
    total_energy = calc_total_energy(bodies)
    ui_lines.append(f"Energy: {total_energy:.2e}")
    ui_lines.append(f"Orbits: {'ON' if show_orbits else 'OFF'} | Trajs: {'ON' if show_trajectories else 'OFF'}")
    
    if followed_body:
        ui_lines.append(f"Following: {followed_body.name}")
    
    if selected_body:
        ui_lines.append("---")
        ui_lines.append(f"Name: {selected_body.name}")
        ui_lines.append(f"Mass: {selected_body.mass:.2e}")
        ui_lines.append(f"Radius: {selected_body.radius}")
        ui_lines.append(f"Vel: {selected_body.vel.length():.2f}")
        
        v_escape = math.sqrt(2 * G * selected_body.mass / selected_body.radius)
        ui_lines.append(f"V_escape: {v_escape:.4e}")
        
        if selected_body is not sun:
            r_vec = selected_body.pos - sun.pos
            v_vec = selected_body.vel
            r = r_vec.length()
            v = v_vec.length()
            energy = v * v / 2 - G * sun.mass / r
            if energy != 0:
                a = -G * sun.mass / (2 * energy)
                h = r_vec.x * v_vec.y - r_vec.y * v_vec.x
                if abs(h) > 0.1 and a > 0:
                    e_x = v_vec.y * h / (G * sun.mass) - r_vec.x / r
                    e_y = -v_vec.x * h / (G * sun.mass) - r_vec.y / r
                    e = math.sqrt(e_x * e_x + e_y * e_y)
                    ui_lines.append(f"SMA: {a:.1f}  Ecc: {e:.3f}")
                    ui_lines.append(f"Dist: {r:.1f}")
    
    panel_h = len(ui_lines) * 20 + 20
    pygame.draw.rect(screen, (20, 20, 20), (panel_x, panel_y, panel_w, panel_h))
    pygame.draw.rect(screen, (200, 200, 200), (panel_x, panel_y, panel_w, panel_h), 2)
    
    for i, line in enumerate(ui_lines):
        text_surf = font.render(line, True, (255, 255, 255))
        screen.blit(text_surf, (panel_x + 10, panel_y + 10 + i * 20))
    
    if show_help:
        help_lines = [
            "Click: Select/Follow | F: Fullscreen | Space: Pause | Home: Reset view",
            "O: Orbits | T: Trajectories | H: Help | +/-: Zoom | Arrows: Move View",
            "Escape: Exit Fullscreen"
        ]
        for i, line in enumerate(help_lines):
            help_surf = font.render(line, True, (150, 150, 150))
            screen.blit(help_surf, (10, screen.get_height() - 70 + i * 20))

    pygame.display.flip()

pygame.quit()
