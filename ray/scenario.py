import json
from typing import List
from pathlib import Path
from .body import Body
from .exceptions import RayError


def load_scenario(filename: str) -> List[Body]:
    filepath = Path(filename)

    if not filepath.exists():
        raise RayError(f"Scenario file not found: {filename}")
    
    try:
        with open(filepath) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise RayError(f"Invalid JSON in {filename}: {e}")
    except Exception as e:
        raise RayError(f"Failed to read scenario {filename}: {e}")

    if "bodies" not in data:
        raise RayError(f"Scenario must contain 'bodies' key. Got {list(data.keys())}")

    bodies = []

    for i, b in enumerate(data["bodies"]):
        try:
            if not all(key in b for key in ["x", "y", "mass", "radius"]):
                missing = [k for k in ["x", "y", "mass", "radius"] if k not in b]
                raise RayError(f"Body {i} missing required fields: {missing}")

            bodies.append(Body(
                x=b["x"],
                y=b["y"],
                mass=b["mass"],
                radius=b["radius"],
                vx=b.get("vx", 0),
                vy=b.get("vy", 0),
                color=tuple(b.get("color", [255, 255, 255]))
            ))
        except RayError:
            raise
        except Exception as e:
            raise RayError(f"Failed to parse body {i}: {e}")

    return bodies
