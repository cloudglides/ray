import json
from .body import Body


def load_scenario(filename):

    with open(filename) as f:
        data = json.load(f)
    bodies = []
    for b in data["bodies"]:
        bodies.append(
            Body(
                x=b["x"],
                y=b["y"],
                mass=b["mass"],
                radius=b["radius"],
                vx=b.get("vx", 0),
                vy=b.get("vy", 0),
                color=tuple(b.get("color", [255, 255, 255])),
            )
        )
    return bodies
