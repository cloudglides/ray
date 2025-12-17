def resolve_elastic_collision(body1, body2) -> None:
    collision_vector = body2.pos - body1.pos
    distance = collision_vector.length()
    
    if distance == 0:
        return
    
    normal = collision_vector.normalize()
        
    rel_vel = body1.vel - body2.vel
    
    vel_along_normal = rel_vel.x * normal.x + rel_vel.y * normal.y
    print(f"collision: distance={distance:.2e}, vel_along={vel_along_normal:.2f}")
    
    if vel_along_normal <= 0:
        return
    
    inv_mass_sum = 1.0 / body1.mass + 1.0 / body2.mass
    
    impulse = -2.0 * vel_along_normal / inv_mass_sum
    
    impulse_vector = normal * impulse
   
    overlap = (body1.radius+body2.radius) - distance 
    if overlap >= 0:
        separation = normal * (overlap/2.0 + 1.0)
        body1.pos -= separation
        body2.pos += separation

    body1.vel += impulse_vector * (1.0 / body1.mass)
    body2.vel -= impulse_vector * (1.0 / body2.mass)
