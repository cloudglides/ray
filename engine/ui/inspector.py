import pygame

class Inspector:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 20)

    def draw(self, screen, obj):
        if not obj:
            return

        lines = [
            f"Mass: {obj.mass:.1f}",
            f"Speed: {obj.vel.length():.1f}"
        ]

        y = 10
        for l in lines:
            txt = self.font.render(l, True, (200, 200, 200))
            screen.blit(txt, (10, y))
            y += 18

