import pygame
from type_defs import Vector2

class BodyRenderer:
    @staticmethod
    def draw_body(screen, body, pan_x, pan_y, zoom, display_scale, velocity_scale=20):
        scaled_x = pan_x + int((body.pos.x/display_scale) *zoom)
        scaled_y = pan_y + int((body.pos.y/display_scale)*zoom)
        scaled_radius = max(1, int((body.radius/display_scale)*zoom))

        if -50 <= scaled_x < screen.get_width() + 50 and -50 <= scaled_y < screen.get_height() +50:
            pygame.draw.circle(screen, body.color, (scaled_x, scaled_y), scaled_radius)


    @staticmethod
    def draw_trail(screen, body, pan_x, pan_y, zoom, display_scale):
        if len(body.trail) < 2:
            return
        for i in range(len(body.trail)-1):
            alpha = int(255*(i/len(body.trail)))
            trail_start_x=pan_x+int((body.trail[i].x/display_scale)*zoom)
            trail_start_y=pan_y+int((body.trail[i].y/display_scale)*zoom)
            trail_end_x=pan_x+int((body.trail[i+1].x/display_scale)*zoom)
            trail_end_y=pan_y+int((body.trail[i+1].y/display_scale)*zoom)

            segment_surface = pygame.Surface(
                    (screen.get_width(), screen.get_height()),
                    pygame.SRCALPHA
                    )

            faded_color = (*body.color, alpha)

            pygame.draw.line(
                    segment_surface,
                    faded_color,
                    (trail_start_x, trail_start_y),
                    (trail_end_x, trail_end_y),
                    1
                    )

            screen.blit(segment_surface, (0,0))
    @staticmethod
    def draw_velocity_vector(screen, body, pan_x, pan_y, zoom, display_scale, velocity_scale=20):
        if body.vel.length() == 0:
             return
        scaled_x=pan_x+int((body.pos.x/display_scale)*zoom)
        scaled_y=pan_y+int((body.pos.y/display_scale)*zoom)

        end_pos = Vector2(
                body.pos.x + body.vel.x *velocity_scale,
                body.pos.y+body.vel.y*velocity_scale
                )
        scaled_end_x = pan_x + int((end_pos.x/display_scale)*zoom)
        scaled_end_y = pan_y + int((end_pos.y/display_scale)*zoom)

        pygame.draw.line(screen, (255, 255, 255), (scaled_x, scaled_y), (scaled_end_x, scaled_end_y), 2)

        arrow_size=5 
        arrow_angle=body.vel.angle_to(Vector2(1,0))

        left=end_pos+Vector2(arrow_size, 0).rotate(arrow_angle+150)
        left_x=pan_x+int((left.x/display_scale)*zoom)
        left_y=pan_y+int((left.y/display_scale)*zoom)

        right=end_pos+Vector2(arrow_size, 0).rotate(arrow_angle-150)
        right_x=pan_x+int((right.x/display_scale)*zoom)
        right_y=pan_y+int((right.y/display_scale)*zoom)

        pygame.draw.line(screen, (255, 255, 255), (scaled_end_x, scaled_end_y), (left_x, left_y), 2)
        pygame.draw.line(screen, (255,255,255), (scaled_end_x, scaled_end_y), (right_x, right_y), 2)
        
