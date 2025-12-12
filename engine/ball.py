class Ball:
    def __init__(self, x, y, ay, radius=20, width=800, height=600):
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
        

    def update(self, dt):
        self.vy += self.ay * dt # updating the velocity on y axis via delta time
        self.x += self.vx * dt # updating pos
        self.y += self.vy * dt # ^

        # reverse horizontal velocity (bouncing on da wall)
        if self.x - self.radius < 0 or self.x + self.radius > self.width:
            self.vx = -self.vx  
        # floor bounce
        if self.y + self.radius > self.height:
            self.y = self.height - self.radius
            self.vy = -self.vy * self.elasticity


