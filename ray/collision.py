from typing import Optional, List, TYPE_CHECKING
from .contact import Contact 

if TYPE_CHECKING:
    from .body import Body

def resolve_elastic_collision(body1: "Body", body2: "Body") -> Optional[Contact]:

    
    collision_vector = body2.pos-body1.pos 
    distance = collision_vector.length()


    if distance==0:
        return None

    normal = collision_vector.normalize()
    rel_vel = body1.vel-body2.vel 
    vel_along_normal=rel_vel.x*normal.x+rel_vel.y*normal.y

    if vel_along_normal<0:
        return None

    overlap=(body1.radius+body2.radius) - distance 
    if overlap>=0:
        seperation=normal*(overlap/2.0)
        body1.pos-=seperation
        body2.pos+=seperation

    inv_mass_sum=1.0/body1.mass+1.0/body2.mass 
    impulse=-vel_along_normal/inv_mass_sum
    impulse_vector=normal*impulse 

    body1.vel+=impulse_vector*(1.0/body1.mass)
    body2.vel-=impulse_vector*(1.0/body2.mass)

    restitution = min(body1.restitution, body2.restitution)
    contact = Contact(body1, body2, normal, overlap, restitution)
    contact.accumulated_impulse=impulse

    return contact


def solve_collisions_iteratively(contacts: List[Contact], iterations: int = 10) -> None:
    beta=0.2
    slop=1e6
    for iterations in range(iterations):
        for contact in contacts:
            body1, body2, = contact.body1, contact.body2 

            rel_vel = body1.vel-body2.vel 
            vel_along_normal=rel_vel.x*contact.normal.x+rel_vel.y*contact.normal.y

            bias = beta*max(0, contact.penetration-slop)

            if vel_along_normal+bias>=0:
                continue

            inv_mass_sum=1.0/body1.mass+1.0/body2.mass
            impulse=-(1.0+contact.restitution)*vel_along_normal/inv_mass_sum - bias/inv_mass_sum


            if impulse<0:
                continue

            impulse_vector=contact.normal*impulse



            body1.vel+=impulse_vector*(1.0/body1.mass)
            body2.vel-=impulse_vector*(1.0/body2.mass)

            contact.accumulated_impulse+=impulse
