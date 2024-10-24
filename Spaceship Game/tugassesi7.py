import pygame
import random
import os

pygame.init()

# Window size
screen_width = 600
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

# Load images
def load_image(filename):
    return pygame.image.load(os.path.join(os.path.dirname(__file__), filename))

# Load images from the same directory as the script
player_image = load_image('spaceship.png')
player_image = pygame.transform.scale(player_image, (60, 60))
enemy_image = load_image('enemy.png')
enemy_image = pygame.transform.scale(enemy_image, (40, 40))
background_image = load_image('background.jpeg')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Player setup
def reset_game():
    global player_x, player_y, enemy_speed, enemies, enemy_spawn_counter, bullets, score, game_over, enemy_speed_timer
    player_x = screen_width // 2 - 30
    player_y = screen_height - 100
    enemy_speed = 3
    enemies = []
    enemy_spawn_counter = 0
    bullets = []
    score = 0
    game_over = False
    enemy_speed_timer = 0

reset_game()  # Initialize game state

# Enemy setup
initial_enemy_count = 5
for i in range(initial_enemy_count):
    enemy_x = random.randint(0, screen_width - 40)
    enemy_y = random.randint(-100, -40)
    enemies.append(pygame.Rect(enemy_x, enemy_y, 40, 40))

# Bullet setup
bullet_speed = 7

# Game clock
clock = pygame.time.Clock()

# Score
font = pygame.font.SysFont(None, 36)

# Game over flag
game_over = False

# Timer for enemy speed increase
enemy_speed_timer = 0
enemy_speed_increment_time = 60 * 1000  # 1 minute in milliseconds

# Function to shoot bullets
def shoot_bullet():
    bullet = pygame.Rect(player_x + player_image.get_width() // 2 - 2, player_y, 4, 10)
    bullets.append(bullet)

# Main game loop
running = True
while running:
    screen.blit(background_image, (0, 0))

    if not game_over:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move player with mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()
        player_x = mouse_x - player_image.get_width() // 2

        # Constrain spaceship within screen boundaries
        if player_x < 0:
            player_x = 0
        elif player_x > screen_width - player_image.get_width():
            player_x = screen_width - player_image.get_width()

        # Shoot bullets
        if pygame.mouse.get_pressed()[0]:  # Left mouse button
            shoot_bullet()

        # Draw player
        screen.blit(player_image, (player_x, player_y))

        # Increase enemy spawn rate over time
        enemy_spawn_counter += 1
        if enemy_spawn_counter >= 40:  # Enemy spawn rate
            enemy_x = random.randint(0, screen_width - 40)
            enemy_y = random.randint(-100, -40)
            enemies.append(pygame.Rect(enemy_x, enemy_y, 40, 40))
            enemy_spawn_counter = 0  # Reset counter

        # Move and draw enemies
        for enemy in enemies[:]:
            enemy.move_ip(0, enemy_speed)
            if enemy.y > screen_height:
                game_over = True  # Game over if enemy reaches the bottom
            if enemy.y + enemy.height > player_y:  # Check if enemy touches the bottom of the screen or the spaceship
                if enemy.x > player_x and enemy.x < player_x + player_image.get_width():
                    game_over = True

            screen.blit(enemy_image, (enemy.x, enemy.y))

        # Move bullets
        for bullet in bullets[:]:
            bullet.move_ip(0, -bullet_speed)
            pygame.draw.rect(screen, (255, 255, 255), bullet)

        # Remove off-screen bullets
        bullets = [bullet for bullet in bullets if bullet.y > 0]

        # Check for collisions between bullets and enemies
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if bullet.colliderect(enemy):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 1
                    break  # Exit loop to avoid modification during iteration

        # Timer to increase enemy speed every minute
        enemy_speed_timer += clock.get_time()
        if enemy_speed_timer >= enemy_speed_increment_time:
            enemy_speed += 1  # Increase enemy speed by 1
            enemy_speed_timer = 0  # Reset the timer

        # Draw score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

    else:
        # Game over screen
        game_over_text = font.render("Game Over!", True, (255, 0, 0))
        final_score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
        play_again_text = font.render("Press R to Play Again", True, (255, 255, 255))
        screen.blit(game_over_text, (screen_width // 2 - 70, screen_height // 2 - 20))
        screen.blit(final_score_text, (screen_width // 2 - 70, screen_height // 2 + 10))
        screen.blit(play_again_text, (screen_width // 2 - 120, screen_height // 2 + 40))

        # Check for play again input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Press R to restart the game
                    reset_game()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
