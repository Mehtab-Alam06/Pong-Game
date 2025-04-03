import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Load sound effects
bounce_sound = pygame.mixer.Sound("Sounds/bounce.mp3")
score_sound = pygame.mixer.Sound("Sounds/score.wav")
menu_sound = pygame.mixer.Sound("Sounds/main_menu.mp3")  # Sound for menu screen
pause_sound = pygame.mixer.Sound("Sounds/pause_screen.mp3")  # Sound for pause screen
game_over_sound = pygame.mixer.Sound("Sounds/game_win.mp3")  # Sound for game over screen

# Set screen size (almost full screen)
WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Set to windowed mode
pygame.display.set_caption("Pong Game")

# Load images and resize them
background_image = pygame.image.load("Images/playing_background.png")  # Load your background image
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Resize to fit window
menu_image = pygame.image.load("Images/background.jpg")  # Load your menu screen image
menu_image = pygame.transform.scale(menu_image, (WIDTH, HEIGHT))  # Resize to fit window
pause_image = pygame.image.load("Images/background.jpg")  # Load your pause screen image
pause_image = pygame.transform.scale(pause_image, (WIDTH, HEIGHT))  # Resize to fit window
game_over_image = pygame.image.load("Images/background.jpg")  # Load your game over screen image
game_over_image = pygame.transform.scale(game_over_image, (WIDTH, HEIGHT))  # Resize to fit window

# Load different fonts for various screens
title_font = pygame.font.Font("Fonts/SuperPixel-m2L8j.ttf", 120)  # Title font
menu_font = pygame.font.Font("Fonts/WowDino-G33vP.ttf", 50)  # Menu options font
player_font = pygame.font.Font("Fonts/MightySouly-lxggD.ttf", 50)  # Player text font
pause_font = pygame.font.Font("Fonts/KnightWarrior-w16n8.otf", 90)  # Increased size for pause screen font
game_over_font = pygame.font.Font("Fonts/Juvanze-ovw9A.otf", 80)  # Game over font
score_font = pygame.font.Font("Fonts/Juvanze-ovw9A.otf", 60)  # Score font

# Colors (Crystals and Effects)
AMETHYST = (153, 102, 204)
AQUAMARINE = (127, 255, 212)
EMERALD = (80, 200, 120)
RUBY = (224, 17, 95)
CITRINE = (255, 223, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game Colors
NEON_BLUE = AQUAMARINE
NEON_PINK = RUBY
DARK_PURPLE = AMETHYST

# Paddle and Ball settings
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 120
BALL_RADIUS = 15

# Game Variables
left_score, right_score = 0, 0
game_started = False
game_paused = False
game_over = False
ai_difficulty = 1
game_mode = "single_player"
menu_options = ["Start Game", "AI Difficulty", "Mode", "Exit"]
selected_option = 0

# Paddle and Ball Positions
left_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 70, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS // 2, HEIGHT // 2 - BALL_RADIUS // 2, BALL_RADIUS, BALL_RADIUS)

# Reset the ball position and speed
def reset_ball():
    ball.x, ball.y = WIDTH // 2 - BALL_RADIUS // 2, HEIGHT // 2 - BALL_RADIUS // 2
    return [random.choice([-3, 3]), random.choice([-3, 3])]

BALL_SPEED = reset_ball()

def reset_game():
    global left_score, right_score, game_paused, game_over, BALL_SPEED
    left_score, right_score = 0, 0
    game_paused = False
    game_over = False
    BALL_SPEED = reset_ball()

# AI paddle control (only for single player)
def ai_control(left_paddle, ball, difficulty):
    if ball.centery < left_paddle.centery and left_paddle.top > 0:
        left_paddle.y -= min(difficulty, 7)  # Limit AI speed
    if ball.centery > left_paddle.centery and left_paddle.bottom < HEIGHT:
        left_paddle.y += min(difficulty, 7)  # Limit AI speed

# Draw paddles with 3D effect
def draw_paddle(paddle, color):
    # Draw shadow
    shadow_color = (0, 0, 0, 100)  # Semi-transparent black for shadow
    pygame.draw.rect(screen, shadow_color, paddle.move(5, 5))  # Draw shadow slightly offset
    # Draw paddle with rounded corners
    pygame.draw.rect(screen, color, paddle, border_radius=10)  # Draw paddle

# Draw ball with 3D effect
def draw_ball(ball):
    # Draw shadow
    shadow_color = (0, 0, 0, 100)  # Semi-transparent black for shadow
    pygame.draw.ellipse(screen, shadow_color, ball.move(5, 5))  # Draw shadow slightly offset
    # Draw ball
    pygame.draw.ellipse(screen, WHITE, ball)  # Draw ball

# Draw text with 3D effect
def draw_text_with_shadow(text, font, color, position, shadow_offset=(2, 2), shadow_color=(0, 0, 0)):
    # Draw shadow
    shadow_surface = font.render(text, True, shadow_color)
    screen.blit(shadow_surface, (position[0] + shadow_offset[0], position[1] + shadow_offset[1]))
    # Draw actual text
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

# Add flags to track sound playback
menu_sound_played = False
pause_sound_played = False
game_over_sound_played = False

# Draw Main Menu
def draw_main_menu():
    global menu_sound_played  # Use the global flag

    screen.blit(menu_image, (0, 0))  # Draw menu background
    title_text = title_font.render("Pong Game", True, CITRINE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 6 + 50))  # Adjusted position

    for i, option in enumerate(menu_options):
        if option == "AI Difficulty":
            option_text = f"{option}: {ai_difficulty}"
        elif option == "Mode":
            option_text = f"{option}: {'Two Player' if game_mode == 'two_player' else 'Single Player'}"
        else:
            option_text = option

        color = CITRINE if i == selected_option else NEON_BLUE
        draw_text_with_shadow(option_text, menu_font, color, (WIDTH // 2 - menu_font.size(option_text)[0] // 2, HEIGHT // 2 + i * 70 + 50))

    box_y = HEIGHT // 2 + selected_option * 70 + 50
    pygame.draw.rect(screen, NEON_PINK, (WIDTH // 2 - 250, box_y - 10, 500, 60), 3)

    # Play menu sound only once
    if not menu_sound_played:
        menu_sound.play(-1)  # Loop the sound
        menu_sound_played = True

# Display player names
def draw_player_names():
    if game_mode == "two_player":
        left_text = player_font.render("Player 1", True, WHITE)
        right_text = player_font.render("Player 2", True, WHITE)
    else:
        left_text = player_font.render("Computer", True, WHITE)
        right_text = player_font.render("Player", True, WHITE)

    screen.blit(left_text, (100, 50))
    screen.blit(right_text, (WIDTH - 250, 50))

# Draw Game Over Screen with Image and Contrast Font Color
def draw_game_over_screen():
    global game_over_sound_played
    screen.blit(game_over_image, (0, 0))  # Draw game over background

    # Display the winner text with contrasting color
    if left_score >= 2:
        winner_text = "Left Player Wins!"
        win_color = NEON_BLUE
    elif right_score >= 2:
        winner_text = "Right Player Wins!"
        win_color = NEON_PINK

    # Change font color for instructions
    play_again_text = "Press R to Play Again"
    quit_text = "Press Q to Quit"
    menu_text = "Press M to Return to Menu"

    # Blit the texts onto the screen with shadows
    draw_text_with_shadow(winner_text, game_over_font, win_color, (WIDTH // 2 - game_over_font.size(winner_text)[0] // 2, HEIGHT // 3))
    draw_text_with_shadow(play_again_text, player_font, CITRINE, (WIDTH // 2 - player_font.size(play_again_text)[0] // 2, HEIGHT // 1.8))
    draw_text_with_shadow(quit_text, player_font, CITRINE, (WIDTH // 2 - player_font.size(quit_text)[0] // 2, HEIGHT // 1.5))
    draw_text_with_shadow(menu_text, player_font, CITRINE, (WIDTH // 2 - player_font.size(menu_text)[0] // 2, HEIGHT // 1.3))

    if not game_over_sound_played:
        game_over_sound.play()  # Play game over sound
        game_over_sound_played = True

    pygame.display.flip()

# Draw Pause Screen
def draw_pause_screen():
    global pause_sound_played
    screen.blit(pause_image, (0, 0))  # Draw pause background
    pause_text = pause_font.render("-- Game Paused --", True, CITRINE)
    continue_text = player_font.render("Press SPACE to Continue", True, NEON_BLUE)
    exit_text = player_font.render("Press ESC to Exit", True, NEON_BLUE)
    menu_text = player_font.render("Press M to Return to Menu", True, NEON_BLUE)

    # Center the "Game Paused" text
    screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 3))

    # Adjusted positions for the other texts
    screen.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, HEIGHT // 2 + 50))  # Adjusted position
    screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 1.5 + 50))  # Adjusted position
    screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 1.3 + 50))  # Adjusted position

    if not pause_sound_played:
        pause_sound.play(-1)  # Loop the pause sound
        pause_sound_played = True

    pygame.display.flip()

# Main Game Loop
running = True
start_time = pygame.time.get_ticks()  # Get the initial time
speed_increment_time = 3000  # Time in milliseconds to increase speed
speed_increment_value = 0.1  # Speed increment value

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if not game_started:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_LEFT:
                    if selected_option == 1:
                        ai_difficulty = max(1, ai_difficulty - 1)
                    elif selected_option == 2:
                        game_mode = "single_player"
                elif event.key == pygame.K_RIGHT:
                    if selected_option == 1:
                        ai_difficulty = min(5, ai_difficulty + 1)
                    elif selected_option == 2:
                        game_mode = "two_player"
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:  # Start Game
                        reset_game()
                        game_started = True
                        menu_sound.stop()  # Stop the menu sound when starting the game
                        menu_sound_played = False  # Reset the flag
                    elif selected_option == 3:  # Exit
                        running = False

            else:
                if game_over:
                    if event.key == pygame.K_r:
                        reset_game()
                        game_over_sound.stop()  # Stop game over sound
                        game_over_sound_played = False  # Reset the flag
                    elif event.key == pygame.K_q:
                        running = False
                    elif event.key == pygame.K_m:  # Return to main menu
                        reset_game()
                        game_started = False
                        menu_sound_played = False  # Reset the flag to allow sound to play again
                        game_over_sound.stop()  # Stop game over sound when returning to menu
                        game_over_sound_played = False  # Reset the flag

                else:
                    if event.key == pygame.K_SPACE:
                        game_paused = not game_paused
                        if game_paused:
                            pause_sound_played = False  # Reset flag to allow sound to play again
                        else:
                            pause_sound.stop()  # Stop pause sound when resuming
                            pause_sound_played = False  # Reset the flag
                    elif event.key == pygame.K_m:  # Return to main menu from pause
                        reset_game()
                        game_started = False
                        menu_sound_played = False  # Reset the flag to allow sound to play again
                        pause_sound.stop()  # Stop pause sound when returning to menu
                        pause_sound_played = False  # Reset the flag

    if not game_started:
        draw_main_menu()
    else:
        if game_paused:
            draw_pause_screen()
        elif game_over:
            draw_game_over_screen()
        else:
            # Paddle movement
            keys = pygame.key.get_pressed()
            if game_mode == "two_player":
                if keys[pygame.K_w] and left_paddle.top > 0:
                    left_paddle.y -= 7
                if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
                    left_paddle.y += 7
            else:
                ai_control(left_paddle, ball, ai_difficulty)

            if keys[pygame.K_UP] and right_paddle.top > 0:
                right_paddle.y -= 7
            if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
                right_paddle.y += 7

            # Ball movement
            ball.x += BALL_SPEED[0]
            ball.y += BALL_SPEED[1]

            # Ball collision with walls
            if ball.top <= 0 or ball.bottom >= HEIGHT:
                BALL_SPEED[1] *= -1
                bounce_sound.play()

            # Ball collision with paddles
            if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
                BALL_SPEED[0] *= -1
                bounce_sound.play()

            # Scoring
            if ball.left <= 0:
                right_score += 1
                BALL_SPEED = reset_ball()
                score_sound.play()

            if ball.right >= WIDTH:
                left_score += 1
                BALL_SPEED = reset_ball()
                score_sound.play()

            # Check for game over
            if left_score >= 2 or right_score >= 2:
                game_over = True

            # Increase ball speed over time
            current_time = pygame.time.get_ticks()
            if current_time - start_time > speed_increment_time:
                BALL_SPEED[0] *= 1.05  # Increase speed by 5%
                BALL_SPEED[1] *= 1.05  # Increase speed by 5%
                start_time = current_time  # Reset the timer

            # Draw the game elements
            screen.blit(background_image, (0, 0))  # Draw playing background
            draw_player_names()
            draw_paddle(left_paddle, NEON_BLUE)  # Draw left paddle with 3D effect
            draw_paddle(right_paddle, NEON_PINK)  # Draw right paddle with 3D effect
            draw_ball(ball)  # Draw ball with 3D effect
            pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))  # Draw center line

            # Draw a box over the score
            score_box = pygame.Rect(WIDTH // 2 - 120, 10, 240, 60)  # Adjusted size for better fit
            pygame.draw.rect(screen, BLACK, score_box)  # Draw the box
            score_text = score_font.render(f"{left_score} - {right_score}", True, CITRINE)
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

    pygame.display.flip()
    pygame.time.delay(15)

pygame.quit()
sys.exit()