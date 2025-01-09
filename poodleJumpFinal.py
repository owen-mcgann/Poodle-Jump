#!/usr/bin/env python3
#Name: Owen J. McGann
#Date: 05.24.2023
#Project: Final Project

import pygame
import random
import time

# Constants
WIDTH = 480
HEIGHT = 800
PLAYER_WIDTH = 60
PLAYER_HEIGHT = 60
PLATFORM_WIDTH = 80
PLATFORM_HEIGHT = 20
PLATFORM_GAP = 170
PLAYER_SPEED = 5
PLAYER_DIRECTION_LEFT = -1
PLAYER_DIRECTION_RIGHT = 1
player_direction = PLAYER_DIRECTION_LEFT
GRAVITY = 0.5
JUMP_HEIGHT = 15
FPS = 60

# Colors
WHITE = (255, 255, 255)
BACKGROUND_COLORS = [
    (255, 0, 0),  # Red
    (0, 255, 0),  # Green
    (0, 0, 255),  # Blue
    # Add more colors if needed
]

# Initialize Pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Poodle Jump')
clock = pygame.time.Clock()

# Load the images
player_image = pygame.image.load('poodle.jpg').convert_alpha()
player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))
platform_image = pygame.image.load('platform5.jpg').convert_alpha()
platform_image = pygame.transform.scale(platform_image, (PLATFORM_WIDTH, PLATFORM_HEIGHT))

class Score:
    def __init__(self):
        self.score = 0

    def increase_score(self):
        self.score += 1

    def save_score(self):
        with open("userScore.txt", "a") as file:
            file.write("Your score was: " + str(self.score) + "\n")

def draw_player():
    if player_direction == PLAYER_DIRECTION_LEFT:
        screen.blit(player_image, (player_x, player_y))
    else:
        # Flip the player image horizontally to face right
        flipped_player_image = pygame.transform.flip(player_image, True, False)
        screen.blit(flipped_player_image, (player_x, player_y))

def draw_platforms():
    for platform_rect in platforms:
        screen.blit(platform_image, platform_rect)

def display_score():
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score.score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def generate_new_platform():
    platform_x = random.randint(0, WIDTH - PLATFORM_WIDTH)
    platform_y = platforms[-1].y - PLATFORM_GAP
    platform_rect = pygame.Rect(platform_x, platform_y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platforms.append(platform_rect)

def generate_initial_platforms():
    initial_platform_rect = pygame.Rect(WIDTH / 2, HEIGHT - PLATFORM_HEIGHT, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platforms.append(initial_platform_rect)
    for i in range(10):
        platform_x = random.randint(0, WIDTH - PLATFORM_WIDTH)
        platform_y = HEIGHT - i * PLATFORM_GAP
        platform_rect = pygame.Rect(platform_x, platform_y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        platforms.append(platform_rect)

def reset_game():
    global player_x, player_y, player_dy, score, scored_platform, platforms, running, jumped_to_new_platform

    player_x = WIDTH // 2 - PLAYER_WIDTH // 2
    player_y = HEIGHT - PLAYER_HEIGHT
    player_rect.x = player_x
    player_rect.y = player_y
    player_dy = 0

    score.score = 0
    scored_platform = []

    jumped_to_new_platform = False

    running = True

def main():
    global player_x, player_y, player_dy, score, scored_platform, running, jumped_to_new_platform, player_direction

    running = True
    on_platform = False
    move_platforms = False  # Indicate if platforms should move
    platform_speed = 3  # Speed at which platforms move
    platform_direction = 1  # Direction of platform movement
    move_timer = pygame.time.get_ticks()  # Timer for platform movement switch

    scored_platform = []  # Initialize scored_platform variablev - scored on

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= PLAYER_SPEED
            player_direction = PLAYER_DIRECTION_LEFT
            if player_x < -PLAYER_WIDTH:  # Wrap around to the right side
                player_x = WIDTH
        if keys[pygame.K_RIGHT]:
            player_x += PLAYER_SPEED
            player_direction = PLAYER_DIRECTION_RIGHT
            if player_x > WIDTH:  # Wrap around to the left side
                player_x = -PLAYER_WIDTH

        player_rect.x = player_x
        player_rect.y = player_y

        on_platform = False
        for platform_rect in platforms:
            if player_rect.colliderect(platform_rect) and player_dy >= 0:
                on_platform = True
                if platform_rect not in scored_platform:
                    scored_platform.append(platform_rect)
                    score.increase_score()
                player_y = platform_rect.top - PLAYER_HEIGHT 
                player_dy = -JUMP_HEIGHT  #simulates jumping

        if not on_platform:
            player_dy += GRAVITY

        player_y += player_dy

        if score.score >= 10:
            move_platforms = True

        if move_platforms:
            current_time = pygame.time.get_ticks()
            if current_time - move_timer >= 1000:  # Switch direction every 1 sec
                platform_direction *= -1
                move_timer = current_time


            for platform_rect in platforms:
                if platform_direction > 0 and platform_rect.x < WIDTH - PLATFORM_WIDTH / 2:
                    platform_rect.x += platform_speed * platform_direction  # Move platforms horizontally

                if platform_direction < 0 and platform_rect.x > PLATFORM_WIDTH / 2:
                    platform_rect.x += platform_speed * platform_direction  # Move platforms horizontally

        if player_y < HEIGHT // 3:
            scroll_amount = int(abs(player_dy)) #represents players vertical movement speed
            for platform_rect in platforms:
                platform_rect.y += scroll_amount  # Scroll the platforms

            if platforms[-1].y > 0:  # Generate new platform if needed
                generate_new_platform()
                jumped_to_new_platform = False

            if player_y < 0:  # Adjust player position to prevent going off-screen
                player_y = 0

        if player_y > HEIGHT:
            running = False

        screen.fill(BACKGROUND_COLORS[score.score // 25 % len(BACKGROUND_COLORS)])
        draw_platforms()
        draw_player()
        display_score()
        pygame.display.flip()
        clock.tick(FPS)

    # Game over
    font = pygame.font.Font(None, 48) # Decreased font size to 48
    game_over_text = font.render("Game Over", True, WHITE)
    game_over_text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(game_over_text, game_over_text_rect)

    restart_text = font.render("Press Space Bar to Restart", True, WHITE)
    restart_text_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(restart_text, restart_text_rect)

    pygame.display.flip()
    time.sleep(2)

    # Save the score
    score.save_score()

    # Play again loop
    play_again = False
    while not play_again:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                play_again = True

    # Restart the game
    reset_game()
    platforms.clear()
    generate_initial_platforms()


# Run the game
player_x = WIDTH // 2 - PLAYER_WIDTH // 2
player_y = HEIGHT - PLAYER_HEIGHT
player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
player_dy = 0

platforms = []
generate_initial_platforms()

score = Score()

while True:
    main()
