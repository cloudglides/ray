import pygame

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


def create_buttons():
    return [
        Button(10, 10, 80, 40, "Pause"),
        Button(100, 10, 80, 40, "1x"),
        Button(190, 10, 80, 40, "2x"),
        Button(280, 10, 80, 40, "5x"),
        Button(370, 10, 100, 40, "10x"),
        Button(480, 10, 100, 40, "500x"),
        Button(1280, 850, 100, 40, "reset")
    ]


def draw_ui(screen, font, clock, TIME_SCALE, paused, camera, bodies, selected_body, followed_body, show_orbits, show_trajectories, show_help):
    from engine.physics.gravity import G
    import math
    
    panel_x = screen.get_width() - 320
    panel_y = 10
    panel_w = 310
    
    ui_lines = []
    fps = clock.get_fps()
    ui_lines.append(f"FPS: {int(fps)}")
    ui_lines.append(f"Time: {TIME_SCALE:.2f}x | {'PAUSED' if paused else 'RUN'}")
    ui_lines.append(f"Zoom: {camera.zoom:.1f}x")
    ui_lines.append(f"Bodies: {len(bodies)}")
    
    def calc_total_energy(bodies):
        ke = sum(0.5 * b.mass * (b.vel.x**2 + b.vel.y**2) for b in bodies)
        pe = 0
        for i, b1 in enumerate(bodies):
            for b2 in bodies[i+1:]:
                dist = b1.pos.distance_to(b2.pos)
                if dist > 0:
                    pe -= G * b1.mass * b2.mass / dist
        return ke + pe
    
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
        
        sun = [b for b in bodies if b.name == "Sun"][0] if any(b.name == "Sun" for b in bodies) else None
        if selected_body is not sun and sun:
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
            "Escape: Exit Fullscreen | R: Reset "
        ]
        for i, line in enumerate(help_lines):
            help_surf = font.render(line, True, (150, 150, 150))
            screen.blit(help_surf, (10, screen.get_height() - 70 + i * 20))
