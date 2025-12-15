from typing import Tuple, Literal
from dataclasses import dataclass

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
