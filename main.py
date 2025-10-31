import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shooting import Shot


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # --- Fonts ---
    font = pygame.font.Font(None, 36)
    big_font = pygame.font.Font(None, 72)

    # --- Welcome Screen ---
    show_welcome_screen(screen, big_font, font)

    # --- Groups ---
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (updatable, drawable, shots)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    score = 0
    lives = PLAYER_LIVES
    respawn_timer = 0
    running = True

    # --- Game Loop ---
    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Handle respawning
        if respawn_timer > 0:
            respawn_timer -= dt
            if respawn_timer <= 0 and player not in updatable:
                player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                player.make_invincible()

        updatable.update(dt)

        # Player ↔ Asteroid collisions (skip if invincible)
        if player in updatable and not player.invincible:
            for asteroid in asteroids:
                if player.collides_with(asteroid):
                    lives -= 1
                    player.kill()
                    respawn_timer = PLAYER_RESPAWN_DELAY
                    if lives <= 0:
                        running = False
                    break

        # Shots ↔ Asteroid collisions
        for asteroid in list(asteroids):
            for shot in list(shots):
                if shot.collides_with(asteroid):
                    shot.kill()
                    asteroid.split()
                    if asteroid.radius <= ASTEROID_MIN_RADIUS:
                        score += SCORE_SMALL
                    elif asteroid.radius <= ASTEROID_MIN_RADIUS * 2:
                        score += SCORE_MEDIUM
                    else:
                        score += SCORE_LARGE

        # --- Drawing ---
        screen.fill("black")
        for entity in drawable:
            entity.draw(screen)

        # HUD
        score_text = font.render(f"Score: {score}", True, "white")
        lives_text = font.render(f"Lives: {lives}", True, "white")
        screen.blit(score_text, (20, 20))
        screen.blit(lives_text, (20, 60))

        pygame.display.flip()

    # --- Game Over Screen ---
    show_game_over_screen(screen, big_font, font, score)


def show_welcome_screen(screen, big_font, font):
    """Display title and wait for any key to start."""
    title_text = big_font.render("ASTEROIDS", True, "white")
    prompt_text = font.render("Press any key to start", True, "gray")

    waiting = True
    while waiting:
        screen.fill("black")
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(prompt_text, (SCREEN_WIDTH // 2 - prompt_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False


def show_game_over_screen(screen, big_font, font, score):
    """Display game over and final score."""
    game_over_text = big_font.render("GAME OVER", True, "red")
    final_score_text = font.render(f"Final Score: {score}", True, "white")
    prompt_text = font.render("Press any key to exit", True, "gray")

    screen.fill("black")
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(prompt_text, (SCREEN_WIDTH // 2 - prompt_text.get_width() // 2, SCREEN_HEIGHT // 2 + 60))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

    pygame.quit()


if __name__ == "__main__":
    main()
