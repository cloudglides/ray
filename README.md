# Ray

A physics engine for simulating multi-body collisions and gravitational interactions in 2D space.

## Overview

Ray is a rigid body dynamics simulator designed to handle complex collision scenarios with persistent contact tracking, iterative constraint solving, and energy-conserving impulse-based resolution. It uses spatial hashing for efficient broad-phase collision detection.

## Features

- **Contact Manifold System** - Persistent contact tracking prevents bodies from penetrating
- **Iterative Impulse Solver** - Multi-iteration constraint resolution with Baumgarte stabilization
- **Restitution Support** - Configurable bounce coefficients for elastic collisions
- **Spatial Hashing** - O(n) collision detection via grid-based spatial partitioning
- **Energy Tracking** - Built-in validators for energy and momentum conservation

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from ray.engine import World
from ray.body import Body
from ray.type_defs import Vector2

world = World(cell_size=5e8)

body1 = Body(
    pos=Vector2(-1e8, 0),
    vel=Vector2(1000, 0),
    mass=1e24,
    radius=1e7,
    restitution=0.8
)
body2 = Body(
    pos=Vector2(1e8, 0),
    vel=Vector2(-1000, 0),
    mass=1e24,
    radius=1e7,
    restitution=0.8
)

world.add_body(body1)
world.add_body(body2)

for i in range(1000):
    collisions = world.update(dt=100)
    for contact in collisions:
        print(f"Collision between {contact.body1} and {contact.body2}")
```

## Running Simulations

### Earth-Moon Orbital Simulation

```bash
python -m examples.pygame_viewer
```

Then press **0** to run at 500000x speed to see orbital dynamics.

### Two-Body Collision

Edit `examples/pygame_viewer.py` line 26, change:

```python
bodies = list(load_scenario("scenarios/earth_moon.json"))
```

To:

```python
bodies = list(load_scenario("scenarios/collisions.json"))
```

Then run:

```bash
python -m examples.pygame_viewer
```

Press **0** for 500000x speed to see collision.

## Scenarios

Place JSON scenario files in `scenarios/` directory:

```json
{
  "bodies": [
    {
      "name": "Body1",
      "x": 0,
      "y": 0,
      "mass": 1e24,
      "radius": 1e7,
      "vx": 0,
      "vy": 0,
      "restitution": 0.8,
      "color": [100, 150, 255]
    }
  ]
}
```

## Architecture

- **World** - Main simulation container, manages bodies and collisions
- **Body** - Rigid body with position, velocity, mass, radius
- **Contact** - Persistent collision contact with accumulated impulse for warm starting
- **SpatialGrid** - Broad-phase collision detection via spatial hashing
- **Solver** - Iterative impulse-based constraint resolution with Baumgarte stabilization

## License

GNU General Public License v3.0 - See LICENSE file for details.
