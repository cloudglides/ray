# Ray

A performant N-body gravity simulator with elastic collision physics and particle effects.

## Features

- **RK4 Numerical Integration** - Accurate orbital mechanics (adaptive timesteps recommended for long simulations)
- **Elastic Collision Physics** - Momentum-conserving rigid body collisions
- **Spatial Grid Collision Detection** - O(n log n) collision checks
- **Physics Validation** - Built-in energy and momentum tracking
- **Decoupled Architecture** - Core physics engine independent of rendering
- **Interactive Visualization** - Pygame-based viewer with pan/zoom controls

## Installation

```bash
pip install pygame
```

## Quick Start

```python
from engine import World
from body import Body

world = World()
sun = Body(x=0, y=0, mass=2e30, radius=7e8)
earth = Body(x=1.5e11, y=0, mass=6e24, radius=6.4e6, vy=29780)

world.add_body(sun)
world.add_body(earth)

for step in range(1000):
    world.update(dt=86400)
```

## Scenarios

Pre-configured scenarios in `scenarios/`:
- `earth_moon.json` - Earth-Moon system
- `collisions.json` - 50 bodies colliding

Load a scenario:

```python
from scenario import load_scenario

world = World()
for body in load_scenario("scenarios/earth_moon.json"):
    world.add_body(body)
```

## Viewer Controls

Run the interactive viewer:

```bash
python examples/pygame_viewer.py
```

**Keyboard:**
- `SPACE` - Pause/Resume
- `1/5/0` - Time scale (1x, 50x, 50000x)
- `-/+` - Zoom out/in
- `ARROW KEYS` - Pan
- `R` - Reset view
- `CLICK` - Select body for info

## Architecture

### Core Engine

- **`engine.py`** - World simulation loop, collision detection
- **`physics.py`** - Integrators (Euler, Verlet, RK4), gravity calculations
- **`body.py`** - Celestial body class with kinematics
- **`collision.py`** - Elastic collision resolution
- **`spatial_grid.py`** - Spatial partitioning for collision detection
- **`validators.py`** - Energy and momentum conservation tracking

### Rendering

- **`renderer.py`** - Decoupled rendering (no pygame in core)
- **`particle.py`** - Visual particle effects
- **`examples/pygame_viewer.py`** - Interactive visualization

## Physics Model

### Integrators

| Integrator | Accuracy | Energy Conservation | Speed | Use Case |
|-----------|----------|-------------------|-------|----------|
| Euler | O(h) | Poor | Fast | Testing |
| Verlet | O(h²) | Good | Medium | Long simulations |
| RK4 (default) | O(h⁴) | Moderate | Slower | High precision short-term |

Switch integrators:

```python
body = Body(..., integrator="verlet")
```

### Gravity

Gravitational acceleration between two bodies:

```
a = G * M / r²
```

- Gravitational constant: `G = 6.67430e-11` (SI units)
- Minimum distance clamping to prevent singularities
- Full O(n²) gravity calculation

### Collisions

Elastic collisions with momentum conservation:
- Impulse-based resolution
- Automatic separation of overlapping bodies
- Coefficient of restitution: 1.0 (perfectly elastic)

## Constants

Edit `constants.py` to tune:

```python
G = 6.67430e-11                    # Gravitational constant
DISPLAY_SCALE = 1e8                # Rendering scale factor
DEFAULT_TRAIL_LENGTH = 200         # Body trail history
DEFAULT_INTEGRATOR = "rk4"         # Integration method
```

## Stability & Validation

### Energy Conservation

```python
from validators import EnergyTracker

tracker = EnergyTracker(world)
for _ in range(1000):
    world.update(dt=86400)
    tracker.update()

print(f"Energy drift: {tracker.drift_percent():.2f}%")
```

Expected drift with RK4: <20% over 10,000 steps.

### Momentum Conservation

```python
from validators import MomentumTracker

tracker = MomentumTracker(world)
for _ in range(1000):
    world.update(dt=86400)
    tracker.update()

print(f"Momentum change: {tracker.drift_magnitude():.2e}")
```

## Performance

### Benchmarks (100 bodies, 100 steps)

- **Collision detection:** ~40,000 steps/sec (spatial grid)
- **Full O(n²) gravity:** ~1,100 steps/sec
- **Rendering:** 60 FPS (pygame)

### Optimization Tips

1. **Reduce trail length** - Set `trail_length=50` for faster rendering
2. **Increase timestep** - Larger `dt` = fewer steps needed
3. **Use faster integrator** - Euler is 3x faster than RK4
4. **Spatial collision grid** - Already enabled by default

## Limitations

1. **No soft-body physics** - All bodies are rigid spheres
2. **No drag/friction** - Only gravitational and collision forces
3. **No multi-threading** - Pure Python (GIL-bound)
4. **No relativistic effects** - Newtonian mechanics only
5. **Fixed spatial grid** - Cell size must be tuned per scenario
6. **Energy drift** - Long simulations (>50,000 steps) require validation

## Testing

```bash
pytest tests/ -v
```

Includes:
- Vector math validation
- Gravity calculation accuracy
- Collision detection
- Physics conservation (energy, momentum)
- Integration method comparisons

## API Reference

### World

```python
world = World(cell_size=1e8)
world.add_body(body)
world.update(dt)
collisions = world.check_collisions()
energy = world.get_total_energy()
momentum = world.get_total_momentum()
```

### Body

```python
body = Body(
    x=0, y=0,              # Position (m)
    mass=1e24,             # Mass (kg)
    radius=1e7,            # Radius (m)
    vx=0, vy=0,            # Velocity (m/s)
    color=(255,255,255),   # RGB tuple
    integrator="rk4"       # Integration method
)
body.update(bodies, dt, spatial_grid, cell_size)
body.is_colliding(other)
body.kinetic_energy()
body.speed()
```

## License

MIT




