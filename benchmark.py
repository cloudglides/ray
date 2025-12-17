import time 
from engine import World
from body import Body 

world = World()
for i in range(100):
    world.add_body(Body(i*1e9, i*1e9, 1e24, 1e7))

start = time.time()
for _ in range(100):
    world.update(86400)
elapsed = time.time() - start

print(f"100 bodies, 100 steps: {elapsed:.2f}s ({100*100/elapsed:.0f} steps/sec)")

