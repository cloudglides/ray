from type_defs import Vector2


class SpatialGrid:
    def __init__(self, cell_size: float):
        self.cell_size = cell_size
        self.grid = {}
    
    def _get_cell_key(self, pos: Vector2):
        x = int(pos.x // self.cell_size)
        y = int(pos.y // self.cell_size)
        return (x, y)
    
    def insert(self, body):
        key = self._get_cell_key(body.pos)
        if key not in self.grid:
            self.grid[key] = []
        self.grid[key].append(body)
    
    def query_radius(self, pos:Vector2, radius:float) -> List[any]:
        results=[]
        cell_key = self._get_cell_key(pos)
        x,y = cell_key 

        cells_to_check = max(1, int(radius/self.cell_size)+1)

        for dx in range(-cells_to_check, cells_to_check+1):
            for dy in range(-cells_to_check, cells_to_check+1):
                key=(x+dx, y+dy)
                if key in self.grid:
                    results.extend(self.grid[key])

        return results

    def clear(self):
        self.grid = {}
