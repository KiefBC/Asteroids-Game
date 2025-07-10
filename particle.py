import pygame
from circleshape import CircleShape
from constants import THRUSTER_PARTICLE_LIFETIME

class Particle(CircleShape):
    def __init__(self, x, y, radius=2, velocity=None, lifetime=THRUSTER_PARTICLE_LIFETIME):
        """
        Initialize a particle with a given position, radius, velocity, and lifetime.
        
        Parameters:
            x (float): The initial x-coordinate of the particle.
            y (float): The initial y-coordinate of the particle.
            radius (float, optional): The radius of the particle. Defaults to 2.
            velocity (pygame.Vector2, optional): The initial velocity vector. Defaults to a zero vector if not provided.
            lifetime (float, optional): The duration the particle remains active. Defaults to THRUSTER_PARTICLE_LIFETIME.
        """
        super().__init__(x, y, radius)
        self.position = pygame.Vector2(x, y)
        self.velocity = velocity or pygame.Vector2(0, 0)
        self.lifetime = lifetime

    def draw(self, screen):
        """
        Render the particle as an orange circle on the specified screen at its current position and radius.
        """
        pygame.draw.circle(screen, "orange", self.position, self.radius)

    def update(self, dt):
        """
        Update the particle's state by advancing its position and reducing its lifetime.
        
        If the particle's lifetime expires, it is removed; otherwise, its position is updated based on its velocity and the elapsed time.
        """
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
            return
        self.position += self.velocity * dt
