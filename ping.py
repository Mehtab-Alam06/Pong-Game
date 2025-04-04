# Developing a PONG GAME using Python

import pygame
import random
import sys

pygame.init()

bounce_sound = pygame.mixer.Sound("Sounds/bounce.mp3")
score_sound = pygame.mixer.Sound("Sounds/score.wav")
menu_sound = pygame.mixer.Sound("Sounds/main_menu.mp3") 
pause_sound = pygame.mixer.Sound("Sounds/pause_screen.mp3")  
game_over_sound = pygame.mixer.Sound("Sounds/game_win.mp3")  

WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("Pong Game")

background_image = pygame.image.load("Images/playing_background.png")  
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  
menu_image = pygame.image.load("Images/background.jpg")  
menu_image = pygame.transform.scale(menu_image, (WIDTH, HEIGHT)) 
pause_image = pygame.image.load("Images/background.jpg") 
pause_image = pygame.transform.scale(pause_image, (WIDTH, HEIGHT))  
game_over_image = pygame.image.load("Images/background.jpg")  
game_over_image = pygame.transform.scale(game_over_image, (WIDTH, HEIGHT)) 

title_font = pygame.font.Font("Fonts/SuperPixel-m2L8j.ttf", 120)  
menu_font = pygame.font.Font("Fonts/WowDino-G33vP.ttf", 50)  
player_font = pygame.font.Font("Fonts/MightySouly-lxggD.ttf", 50)  
pause_font = pygame.font.Font("Fonts/KnightWarrior-w16n8.otf", 90)  
game_over_font = pygame.font.Font("Fonts/Juvanze-ovw9A.otf", 80) 
score_font = pygame.font.Font("Fonts/Juvanze-ovw9A.otf", 60) 

AMETHYST = (153, 102, 204)
AQUAMARINE = (127, 255, 212)
EMERALD = (80, 200, 120)
RUBY = (224, 17, 95)
CITRINE = (255, 223, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

NEON_BLUE = AQUAMARINE
NEON_PINK = RUBY
DARK_PURPLE = AMETHYST

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 120
BALL_RADIUS = 15

left_score, right_score = 0, 0
game_started = False
game_paused = False
game_over = False
ai_difficulty = 1
game_mode = "single_player"
menu_options = ["Start Game", "AI Difficulty", "Mode", "Exit"]
selected_option = 0

left_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 70, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS // 2, HEIGHT // 2 - BALL_RADIUS // 2, BALL_RADIUS, BALL_RADIUS)

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

def ai_control(left_paddle, ball, difficulty):
    if ball.centery < left_paddle.centery and left_paddle.top > 0:
        left_paddle.y -= min(difficulty, 7)  
    if ball.centery > left_paddle.centery and left_paddle.bottom < HEIGHT:
        left_paddle.y += min(difficulty, 7)  

def draw_paddle(paddle, color):
    shadow_color = (0, 0, 0, 100)  
    pygame.draw.rect(screen, shadow_color, paddle.move(5, 5)) 
    pygame.draw.rect(screen, color, paddle, border_radius=10)  

def draw_ball(ball):
    shadow_color = (0, 0, 0, 100)  
    pygame.draw.ellipse(screen, shadow_color, ball.move(5, 5))  
    pygame.draw.ellipse(screen, WHITE, ball) 

def draw_text_with_shadow(text, font, color, position, shadow_offset=(2, 2), shadow_color=(0, 0, 0)):
    shadow_surface = font.render(text, True, shadow_color)
    screen.blit(shadow_surface, (position[0] + shadow_offset[0], position[1] + shadow_offset[1]))
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

menu_sound_played = False
pause_sound_played = False
game_over_sound_played = False

def draw_main_menu():
    global menu_sound_played 
    screen.blit(menu_image, (0, 0))  
    title_text = title_font.render("Table Tennis", True, CITRINE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 6 + 50)) 

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

    if not menu_sound_played:
        menu_sound.play(-1)  
        menu_sound_played = True

def draw_player_names():
    if game_mode == "two_player":
        left_text = player_font.render("Player 1", True, WHITE)
        right_text = player_font.render("Player 2", True, WHITE)
    else:
        left_text = player_font.render("Computer", True, WHITE)
        right_text = player_font.render("Player", True, WHITE)

    screen.blit(left_text, (100, 50))
    screen.blit(right_text, (WIDTH - 250, 50))

def draw_game_over_screen():
    global game_over_sound_played
    screen.blit(game_over_image, (0, 0))  
    if left_score >= 2:
        winner_text = "Left Player Wins!"
        win_color = NEON_BLUE
    elif right_score >= 2:
        winner_text = "Right Player Wins!"
        win_color = NEON_PINK

    play_again_text = "Press R to Play Again"
    quit_text = "Press Q to Quit"
    menu_text = "Press M to Return to Menu"

    draw_text_with_shadow(winner_text, game_over_font, win_color, (WIDTH // 2 - game_over_font.size(winner_text)[0] // 2, HEIGHT // 3))
    draw_text_with_shadow(play_again_text, player_font, CITRINE, (WIDTH // 2 - player_font.size(play_again_text)[0] // 2, HEIGHT // 1.8))
    draw_text_with_shadow(quit_text, player_font, CITRINE, (WIDTH // 2 - player_font.size(quit_text)[0] // 2, HEIGHT // 1.5))
    draw_text_with_shadow(menu_text, player_font, CITRINE, (WIDTH // 2 - player_font.size(menu_text)[0] // 2, HEIGHT // 1.3))

    if not game_over_sound_played:
        game_over_sound.play() 
        game_over_sound_played = True

    pygame.display.flip()

def draw_pause_screen():
    global pause_sound_played
    screen.blit(pause_image, (0, 0)) 
    pause_text = pause_font.render("-- Game Paused --", True, CITRINE)
    continue_text = player_font.render("Press SPACE to Continue", True, NEON_BLUE)
    exit_text = player_font.render("Press ESC to Exit", True, NEON_BLUE)
    menu_text = player_font.render("Press M to Return to Menu", True, NEON_BLUE)

    screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 3))

    screen.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, HEIGHT // 2 + 50))  
    screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 1.5 + 50))  
    screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 1.3 + 50)) 

    if not pause_sound_played:
        pause_sound.play(-1)  
        pause_sound_played = True

    pygame.display.flip()


running = True
start_time = pygame.time.get_ticks()  
speed_increment_time = 3000  
speed_increment_value = 0.1  

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
                    if selected_option == 0:  
                        reset_game()
                        game_started = True
                        menu_sound.stop()  
                        menu_sound_played = False  
                    elif selected_option == 3:  
                        running = False

            else:
                if game_over:
                    if event.key == pygame.K_r:
                        reset_game()
                        game_over_sound.stop()  
                        game_over_sound_played = False  
                    elif event.key == pygame.K_q:
                        running = False
                    elif event.key == pygame.K_m: 
                        reset_game()
                        game_started = False
                        menu_sound_played = False  
                        game_over_sound.stop()  
                        game_over_sound_played = False  

                else:
                    if event.key == pygame.K_SPACE:
                        game_paused = not game_paused
                        if game_paused:
                            pause_sound_played = False  
                        else:
                            pause_sound.stop()  
                            pause_sound_played = False  
                    elif event.key == pygame.K_m: 
                        reset_game()
                        game_started = False
                        menu_sound_played = False  
                        pause_sound.stop() 
                        pause_sound_played = False  

    if not game_started:
        draw_main_menu()
    else:
        if game_paused:
            draw_pause_screen()
        elif game_over:
            draw_game_over_screen()
        else:
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

            ball.x += BALL_SPEED[0]
            ball.y += BALL_SPEED[1]

            if ball.top <= 0 or ball.bottom >= HEIGHT:
                BALL_SPEED[1] *= -1
                bounce_sound.play()

            if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
                BALL_SPEED[0] *= -1
                bounce_sound.play()

            if ball.left <= 0:
                right_score += 1
                BALL_SPEED = reset_ball()
                score_sound.play()

            if ball.right >= WIDTH:
                left_score += 1
                BALL_SPEED = reset_ball()
                score_sound.play()

            if left_score >= 2 or right_score >= 2:
                game_over = True

            current_time = pygame.time.get_ticks()
            if current_time - start_time > speed_increment_time:
                BALL_SPEED[0] *= 1.05 
                BALL_SPEED[1] *= 1.05 
                start_time = current_time  

            screen.blit(background_image, (0, 0))  
            draw_player_names()
            draw_paddle(left_paddle, NEON_BLUE)  
            draw_paddle(right_paddle, NEON_PINK)  
            draw_ball(ball)  
            pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))  

            score_box = pygame.Rect(WIDTH // 2 - 120, 10, 240, 60)  
            pygame.draw.rect(screen, BLACK, score_box)  
            score_text = score_font.render(f"{left_score} - {right_score}", True, CITRINE)
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

    pygame.display.flip()
    pygame.time.delay(15)

pygame.quit()
sys.exit()