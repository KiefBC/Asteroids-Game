from circleshape import CircleShape
from constants import (
    PLAYER_RADIUS,
    PLAYER_SHOOT_COOLDOWN,
    PLAYER_SHOOT_SPEED,
    PLAYER_TURN_SPEED,
    PLAYER_SPEED,
    SHOT_RADIUS,
    THRUSTER_PARTICLE_SPEED,
)
import pygame
from shot import Shot
from particle import Particle

class Player(CircleShape):
    def __init__(self, x, y):
        """
        Initialize a Player instance at the specified (x, y) position with default rotation, position vector, and shooting cooldown timer.
        """
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.position = pygame.Vector2(x, y)
        self.shoot_timer = 0

    def engine_position(self):
        """
        Calculate and return the position at the rear of the ship for emitting engine particles.
        
        Returns:
            pygame.Vector2: The world coordinates at the back of the ship based on its current position, rotation, and radius.
        """
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        return self.position - forward * self.radius

    def emit_engine_particle(self):
        """
        Creates a particle at the ship's engine position with velocity opposite to the ship's forward direction, simulating engine thrust.
        """
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        velocity = -forward * THRUSTER_PARTICLE_SPEED
        pos = self.engine_position()
        Particle(pos.x, pos.y, velocity=velocity)

    def triangle(self):
        """
        Calculate and return the vertices of the player's triangular ship based on its current position, rotation, and radius.
        
        Returns:
            list[pygame.Vector2]: A list of three vectors representing the triangle's vertices in world coordinates.
        """
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position  - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "pink", self.triangle(), 2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        """
        Update the player's state based on keyboard input and elapsed time.
        
        Handles rotation, movement, shooting, and engine particle emission according to user input and cooldown timers.
        
        Parameters:
            dt (float): Time elapsed since the last update, used for frame-independent movement and actions.
        """
        self.shoot_timer -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
            self.emit_engine_particle()
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            if not self.shoot_timer > 0:
                self.shoot()

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN

        shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        shot.velocity = velocity
