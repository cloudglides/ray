import pygame
import sys
import os
import math

# Add root to path so we can import engine
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from camera import Camera
from ui import create_buttons, draw_ui
from scenario import create_starfield, create_solar_system, CENTER
from physics_utils import calculate_ideal_orbit, check_and_merge_collisions

pygame.init()
screen = pygame.display.set_mode((1400, 900))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 20)
title_font = pygame.font.Font(None, 28)

camera = Camera(1400, 900)
camera.x = CENTER.x
camera.y = CENTER.y
camera.zoom = 1.0  



stars = create_starfield()
bodies, satellite = create_solar_system()
bodies.append(satellite)

TIME_SCALE = 0.01
buttons = create_buttons()

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
initial_states = [(b.pos.copy(), b.vel.copy()) for b in bodies]


trajectory=[]

while running:

    


    dt = clock.tick(60) / 1000 * TIME_SCALE
    
    if paused:
        dt = 0

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        satellite.rotate(-3)
    if keys[pygame.K_d]:
        satellite.rotate(3)
    if keys[pygame.K_w]:
        satellite.apply_thrust(dt)
        print("thrusting")
    
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
            elif e.key == pygame.K_LEFT:
                camera.pan(30, 0)
            elif e.key == pygame.K_r:
                for i in range(min(len(bodies), len(initial_states))):
                    bodies[i].pos = initial_states[i][0].copy()
                    bodies[i].vel = initial_states[i][1].copy()
                selected_body = None
                followed_body = None
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
                screen = pygame.display.set_mode((1400, 900))
            elif e.key == pygame.K_SPACE:
                paused = not paused
            elif e.key == pygame.K_HOME:
                camera.x = initial_camera_x
                camera.y = initial_camera_y
                camera.zoom = initial_zoom
                followed_body = None

    for b in bodies:
        b.update(bodies, dt)
    
    check_and_merge_collisions(bodies)
    trajectory = satellite.predict_trajectory(bodies, steps=100, dt=0.01)
    if trajectory and len(trajectory) > 1:
        for i in range(0, len(trajectory)-1, 5):
            p1 = camera.to_screen(trajectory[i])
            p2 = camera.to_screen(trajectory[i+1])
            pygame.draw.line(screen, (100, 255, 100), (int(p1.x), int(p1.y)), (int(p2.x), int(p2.y)), 1)


 
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
                if b.name != "Sun":
                    ref = b.parent if (hasattr(b, 'parent') and b.parent) else [bd for bd in bodies if bd.name == "Sun"][0]
                    orbit_cache[id(b)] = calculate_ideal_orbit(b, ref)
    
    if show_orbits:
        for b in bodies:
            if id(b) in orbit_cache and b.name != "Sun":
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

    for b in bodies:
        if b is satellite:
            # Draw satellite as white triangle
            satellite_screen_pos = camera.to_screen(satellite.pos)
            # Adjust satellite draw for camera zoom
            size = max(3, int(8 * camera.zoom))
            rad = math.radians(satellite.rotation)
            
            tip = satellite_screen_pos + pygame.Vector2(math.sin(rad), -math.cos(rad)) * size
            left = satellite_screen_pos + pygame.Vector2(math.sin(rad + 2.4), -math.cos(rad + 2.4)) * size * 0.6
            right = satellite_screen_pos + pygame.Vector2(math.sin(rad - 2.4), -math.cos(rad - 2.4)) * size * 0.6
            
            points = [
                (int(tip.x), int(tip.y)),
                (int(left.x), int(left.y)),
                (int(right.x), int(right.y))
            ]
            pygame.draw.polygon(screen, (255, 255, 255), points)
            
            label = font.render(b.name, True, (255, 255, 255))
            screen.blit(label, (satellite_screen_pos.x + 10, satellite_screen_pos.y - 10))
        else:
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
    
    draw_ui(screen, font, clock, TIME_SCALE, paused, camera, bodies, selected_body, followed_body, show_orbits, show_trajectories, show_help)
   


    

    pygame.display.flip()

pygame.quit()
