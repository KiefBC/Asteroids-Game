import pygame
import sys
from asteroid import Asteroid
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCORE_LARGE_ASTEROID, SCORE_MEDIUM_ASTEROID, SCORE_SMALL_ASTEROID, ASTEROID_MIN_RADIUS
from player import Player
from asteroid_field import AsteroidField
from shot import Shot

def main():
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = updatable
    Shot.containers = (shots, updatable, drawable)

    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    player = Player(x, y)
    AsteroidField()

    score = 0
    font = pygame.font.Font(None, 36)

    while True:
        # Enables the Close Window Button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collision_check(player):
                print(f"Game Over! Final Score: {score}")
                sys.exit(0)

            for shot in shots:
                if shot.collision_check(asteroid):
                    score += calculate_score(asteroid.radius)
                    asteroid.split()
                    shot.kill()

        screen.fill((0, 0, 0))
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip() # This line updates the display

        # Limit the frame rate to 60 FPS
        dt = clock.tick(60) / 1000

def calculate_score(radius):
    if radius >= ASTEROID_MIN_RADIUS:
        return SCORE_LARGE_ASTEROID
    elif radius >= ASTEROID_MIN_RADIUS * 2:
        return SCORE_MEDIUM_ASTEROID
    else:
        return SCORE_SMALL_ASTEROID

if __name__ == "__main__":
    main()
