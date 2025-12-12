


class Ball:
    def __init__(self, x, y, ay, radius=20, width=800, height=600, mass=1):
        self.ay = ay
        self.x = x
        self.y = y
        self.vx = 0 # uhhh velocity
        self.vy = 0    # velocity but on y axis
        self.radius = radius 
        self.color = (255, 200, 50)
        self.elasticity = 0.8 # bouncy!
        self.width = width
        self.height = height
        self.mass = mass
        

    def update(self, dt):
        self.vy += self.ay * dt # updating the velocity on y axis via delta time
        self.x += self.vx * dt # updating pos
        self.y += self.vy * dt # ^

    def collide_with_wall(self):
        # reverse horizontal velocity (bouncing on da wall)
        if self.x - self.radius < 0 or self.x + self.radius > self.width:
            self.vx = -self.vx  
        # floor bounce
        if self.y + self.radius > self.height:
            self.y = self.height - self.radius
            self.vy = -self.vy * self.elasticity


    def collide_with_ball(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        dist = (dx**2 + dy**2) ** 0.5
        if dist == 0:
            dist = 0.001
        if dist < self.radius + other.radius:
            nx = dx / dist
            ny = dy / dist
            rel_vel_x = self.vx - other.vx
            rel_vel_y = self.vy - other.vy
            vel_along_normal = rel_vel_x * nx + rel_vel_y * ny
            if vel_along_normal > 0:
                return
            e = min(self.elasticity, other.elasticity)
            j = -(1 + e) * vel_along_normal
            j /= (1/self.mass + 1/other.mass)
            self.vx += j * nx / self.mass
            self.vy += j * ny / self.mass
            other.vx -= j * nx / other.mass
            other.vy -= j * ny / other.mass
            overlap = self.radius + other.radius - dist
            self.x -= nx * (overlap/2)
            self.y -= ny * (overlap/2)
            other.x += nx * (overlap/2)
            other.y += ny * (overlap/2)
 
