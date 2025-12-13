import pygame

class Slider:
    def __init__(self, x, y, w, min_val, max_val, start_val):
        self.rect = pygame.Rect(x, y, w, 6)
        self.min = min_val
        self.max = max_val
        self.value = start_val

        self.knob_radius = 8
        self.dragging = False
        self.knob_x = self._value_to_pos(start_val)

    def _value_to_pos(self, value):
        t = (value - self.min) / (self.max - self.min)
        return self.rect.x + int(t * self.rect.w)

    def _pos_to_value(self, x):
        t = (x - self.rect.x) / self.rect.w
        t = max(0, min(1, t))
        return self.min + t * (self.max - self.min)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if abs(event.pos[0] - self.knob_x) < self.knob_radius * 2:
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.knob_x = max(self.rect.x, min(event.pos[0], self.rect.x + self.rect.w))
            self.value = self._pos_to_value(self.knob_x)

    def draw(self, screen):
        pygame.draw.rect(screen, (180, 180, 180), self.rect)
        pygame.draw.circle(screen, (255, 80, 80),
                           (self.knob_x, self.rect.centery),
                           self.knob_radius)
    def predict_trajectory(self, planets, steps=300, dt=0.05):
        pos = self.pos.copy()
        vel = self.velocity.copy()

        points = []

        for _ in range(steps):
            acc = pygame.Vector2(0, 0)

            for p in planets:
                direction = p.pos - pos
                dist = direction.length() + 1
                force_mag = p.mass / (dist * dist)
                acc += direction.normalize() * force_mag

            vel += acc * dt
            pos += vel * dt
            points.append(pos.copy())

        return points

