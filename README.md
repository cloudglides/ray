# RAY

A performant N-body gravity simulator

## FEATS

- **RK4 Numerical Integration** - Highly accurate orbital mechanics
- **Elastic Collision Physics** - Realistic collision response with momentum conservation
- **Visualization** - Interactive zoom/move via pygame

# QUICK START

```python
from engine import World
from body import Body

world = World()
world.add_body(Body(x=0, y=0, mass=2e30, radius=7e8))
world.add_body(Body(x=1.5e11, y=0, mass=6e24, radius=6.4e6, vy=29780))

for _ in range(1000):
    world.update(dt=86400) # 1 day timestamp
```



