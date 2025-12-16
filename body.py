from typing import List, Optional
import pygame
from constants import DEFAULT_TRAIL_LENGTH, DEFAULT_COLOR, DEFAULT_INTEGRATOR
from type_defs import Color, Vector2
from physics import get_integrator
from exceptions import InvalidBodyError
class Body:
    def __init__(
        self,
        x: float,
        y: float,
        mass: float,
        radius: float,
        color: Color = DEFAULT_COLOR,
        trail_length: int = DEFAULT_TRAIL_LENGTH,
        integrator: str = DEFAULT_INTEGRATOR,
        vx: float = 0.0,
        vy: float = 0.0,
    ):
        if mass <= 0:
            raise InvalidBodyError(f"Mass must be positive, got {mass}")
        if radius < 0:
            raise InvalidBodyError(f"Radius must be non-negative, got {radius}")
        self.pos = Vector2(x, y)
        self.vel = Vector2(vx, vy)
        self.mass = mass
        self.radius = radius
        self.color = color
        self.trail: List[Vector2] = [self.pos.copy()]
        self.trail_length = trail_length
        self._integrator = get_integrator(integrator)
        self._old_pos: Optional[Vector2] = None
    def update(self, bodies: List["Body"], dt: float) -> None:
        self._integrator(self, bodies, dt)
        self.trail.append(self.pos.copy())
        if len(self.trail) > self.trail_length:
            self.trail.pop(0)
    def draw(self, screen: pygame.Surface, velocity_scale: float = 20) -> None:
        if len(self.trail) > 1:
            for i in range(len(self.trail) - 1):
                alpha = int(255 * (i / len(self.trail)))
                segment_surface = pygame.Surface(
                    (screen.get_width(), screen.get_height()),
                    pygame.SRCALPHA
                )
                faded_color = (*self.color, alpha)
                pygame.draw.line(
                    segment_surface,
                    faded_color,
                    (int(self.trail[i].x), int(self.trail[i].y)),
                    (int(self.trail[i + 1].x), int(self.trail[i + 1].y)),
                    1
                )
                screen.blit(segment_surface, (0, 0))
        if self.vel.length() > 0:
            end_pos = Vector2(
                self.pos.x + self.vel.x * velocity_scale,
                self.pos.y + self.vel.y * velocity_scale
            )
            pygame.draw.line(screen, (255, 255, 255), (int(self.pos.x), int(self.pos.y)), (int(end_pos.x), int(end_pos.y)), 2)
            arrow_size = 5
            arrow_angle = self.vel.angle_to(Vector2(1, 0))
            left = end_pos + Vector2(arrow_size, 0).rotate(arrow_angle + 150)
            right = end_pos + Vector2(arrow_size, 0).rotate(arrow_angle - 150)
            pygame.draw.line(screen, (255, 255, 255), (int(end_pos.x), int(end_pos.y)), (int(left.x), int(left.y)), 2)
            pygame.draw.line(screen, (255, 255, 255), (int(end_pos.x), int(end_pos.y)), (int(right.x), int(right.y)), 2)
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), int(self.radius))
    def is_colliding(self, other: "Body") -> bool:
        if other is self:
            return False
        dist = self.pos.distance_to(other.pos)
        return dist < (self.radius + other.radius)
    def kinetic_energy(self) -> float:
        return 0.5 * self.mass * (self.vel.x**2 + self.vel.y**2)
    def distance_to(self, other: "Body") -> float:
        return self.pos.distance_to(other.pos)
    def speed(self) -> float:
        return self.vel.length()
    def __repr__(self) -> str:
        return (
            f"Body(pos=({self.pos.x:.2e}, {self.pos.y:.2e}), "
            f"vel=({self.vel.x:.2e}, {self.vel.y:.2e}), "
            f"mass={self.mass:.2e}, radius={self.radius:.2e})"
        )
