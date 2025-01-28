import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Paddle dimensions
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100

# Ball dimensions
BALL_SIZE = 20

# Paddle positions
left_paddle_y = (HEIGHT - PADDLE_HEIGHT) // 2
right_paddle_y = (HEIGHT - PADDLE_HEIGHT) // 2

# Ball position and speed
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_speed_x, ball_speed_y = 7, 7

# Paddle speed
paddle_speed = 10

# Scores
left_score = 0
right_score = 0
winning_score = 7

# Font for scoreboard and buttons
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)

# Clock
clock = pygame.time.Clock()

# Function to reset the ball
def reset_ball():
    return WIDTH // 2, HEIGHT // 2

# Function to reset the game
def reset_game():
    global left_score, right_score, ball_x, ball_y, ball_speed_x, ball_speed_y
    left_score = 0
    right_score = 0
    ball_x, ball_y = reset_ball()
    ball_speed_x, ball_speed_y = 7, 7

# Function to draw the restart button
def draw_restart_button():
    button_width, button_height = 200, 80
    button_x = (WIDTH - button_width) // 2
    button_y = (HEIGHT - button_height) // 2 + 100
    pygame.draw.rect(screen, GRAY, (button_x, button_y, button_width, button_height))
    
    # Render the "Restart" text
    restart_text = button_font.render("Restart", True, BLACK)
    
    # Calculate text position to center it inside the button
    text_width, text_height = restart_text.get_size()
    text_x = button_x + (button_width - text_width) // 2
    text_y = button_y + (button_height - text_height) // 2
    
    # Draw the text
    screen.blit(restart_text, (text_x, text_y))
    
    return pygame.Rect(button_x, button_y, button_width, button_height)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Check for mouse click on the restart button
        if event.type == pygame.MOUSEBUTTONDOWN and (left_score >= winning_score or right_score >= winning_score):
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if restart_button.collidepoint(mouse_x, mouse_y):
                reset_game()

    # Key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle_y > 0:
        left_paddle_y -= paddle_speed
    if keys[pygame.K_s] and left_paddle_y < HEIGHT - PADDLE_HEIGHT:
        left_paddle_y += paddle_speed
    if keys[pygame.K_UP] and right_paddle_y > 0:
        right_paddle_y -= paddle_speed
    if keys[pygame.K_DOWN] and right_paddle_y < HEIGHT - PADDLE_HEIGHT:
        right_paddle_y += paddle_speed

    # Ball movement
    if left_score < winning_score and right_score < winning_score:
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Ball collision with top and bottom
        if ball_y <= 0 or ball_y >= HEIGHT - BALL_SIZE:
            ball_speed_y *= -1

        # Ball collision with paddles
        if ball_x <= PADDLE_WIDTH and left_paddle_y <= ball_y <= left_paddle_y + PADDLE_HEIGHT:
            ball_speed_x *= -1
        if ball_x >= WIDTH - PADDLE_WIDTH - BALL_SIZE and right_paddle_y <= ball_y <= right_paddle_y + PADDLE_HEIGHT:
            ball_speed_x *= -1

        # Ball out of bounds (left or right)
        if ball_x <= 0:
            right_score += 1
            ball_x, ball_y = reset_ball()
        if ball_x >= WIDTH - BALL_SIZE:
            left_score += 1
            ball_x, ball_y = reset_ball()

    # Clear screen
    screen.fill(BLACK)

    # Draw paddles
    pygame.draw.rect(screen, WHITE, (0, left_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, WHITE, (WIDTH - PADDLE_WIDTH, right_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))

    # Draw ball
    pygame.draw.ellipse(screen, WHITE, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))

    # Draw scoreboard
    score_text = font.render(f"{left_score} : {right_score}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - 50, 10))

    # Check for winning condition
    if left_score >= winning_score or right_score >= winning_score:
        # Display winning message
        winner_text = font.render("Player 1 Wins!" if left_score >= winning_score else "Player 2 Wins!", True, WHITE)
        screen.blit(winner_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))

        # Draw restart button
        restart_button = draw_restart_button()

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)