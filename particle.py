import pygame
from circleshape import CircleShape
from constants import THRUSTER_PARTICLE_LIFETIME

class Particle(CircleShape):
    def __init__(self, x, y, radius=2, velocity=None, lifetime=THRUSTER_PARTICLE_LIFETIME):
        super().__init__(x, y, radius)
        self.position = pygame.Vector2(x, y)
        self.velocity = velocity or pygame.Vector2(0, 0)
        self.lifetime = lifetime

    def draw(self, screen):
        pygame.draw.circle(screen, "orange", self.position, self.radius)

    def update(self, dt):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
            return
        self.position += self.velocity * dt
