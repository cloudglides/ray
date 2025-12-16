from typing import Tuple, Literal
from dataclasses import dataclass
import math
Color = Tuple[int, int, int]
IntegratorType = Literal["euler", "verlet"]
VectorLike = Tuple[float, float]
@dataclass
class BodyState:
    x: float
    y: float
    vx: float
    vy: float
    mass: float
    radius: float
class Vector2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)
    def __rmul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)
    def __truediv__(self, scalar):
        return Vector2(self.x / scalar, self.y / scalar)
    def copy(self):
        return Vector2(self.x, self.y)
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)
    def normalize(self):
        l = self.length()
        if l == 0:
            return Vector2(0, 0)
        return self / l
    def distance_to(self, other):
        return (self - other).length()
    def angle_to(self, other):
        return math.atan2(other.y, other.x) - math.atan2(self.y, self.x)
    def rotate(self, angle):
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return Vector2(
            self.x * cos_a - self.y * sin_a,
            self.x * sin_a + self.y * cos_a
        )
