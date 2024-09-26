import pygame
import sys
import random

# Initialising Pygame
pygame.init()

# Initialising surface
screen_width = 400
screen_height = 400
surface = pygame.display.set_mode((screen_width, screen_height))

# Setting the caption name
pygame.display.set_caption("Snake")

# Setting the FPS
clock = pygame.time.Clock()

# Colours
red = (255, 0, 0)
blue = (0, 0, 255)
black = (0, 0, 0)

# Grid block sizes
block_size = 20

# Rectangle Properties
rect_width = 20
rect_height = 20
rect_x = 0
rect_y = 80
rect_speed = 20

# Blueberry properties
blueberry_surf = pygame.image.load('Graphics/blueberry.png').convert_alpha()
# Get rectangle of blueberry image
blueberry_rect = blueberry_surf.get_rect(center=(200, 200))

# Variables to keep track of key states
key_w = False
key_s = False
key_a = False
key_d = False


# Score mechanic
def display_score(score):
    score_surf = test_font.render(f'Score: {score}', False, (74, 74, 74))
    score_rect = score_surf.get_rect(center=(200, 50))
    surface.blit(score_surf, score_rect)


test_font = pygame.font.Font('Font/Pixeltype.ttf', 50)

# Initialising score
current_score = 0

# Accumulators for movement
x_accumulator = 0
y_accumulator = 0

# Initialise snake body
snake_body = []


# grid function
def draw_grid():
    for x in range(0, screen_width, block_size):
        for y in range(80, screen_height, block_size):
            grid = pygame.Rect(x, y, block_size, block_size)
            pygame.draw.rect(surface, "#3c3c3b", grid, 1)


# Game states
run = True
game_active = True

while run:

    # Overwriting previous images
    surface.fill(black)

    # Drawing grid
    draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and not key_s:
                key_w = True
                key_s = False
                key_a = False
                key_d = False
            elif event.key == pygame.K_s and not key_w:
                key_w = False
                key_s = True
                key_a = False
                key_d = False
            elif event.key == pygame.K_a and not key_d:
                key_w = False
                key_s = False
                key_a = True
                key_d = False
            elif event.key == pygame.K_d and not key_a:
                key_w = False
                key_s = False
                key_a = False
                key_d = True

    # Movement logic
    if key_w:
        y_accumulator -= rect_speed
    elif key_s:
        y_accumulator += rect_speed
    elif key_a:
        x_accumulator -= rect_speed
    elif key_d:
        x_accumulator += rect_speed

    # Snapping to grid when accumulated movement exceeds block_size
    if abs(x_accumulator) >= block_size:
        rect_x += (x_accumulator // block_size) * block_size
        x_accumulator = 0  # Reset accumulator after snapping

    if abs(y_accumulator) >= block_size:
        rect_y += (y_accumulator // block_size) * block_size
        y_accumulator = 0  # Reset accumulator after snapping

        # Ensure the rectangle stays within the boundaries
    rect_x = max(0, min(rect_x, screen_width - rect_width))
    rect_y = max(80, min(rect_y, screen_height - rect_height))

    # Blueberry boundary checks
    blueberry_rect.x = max(0, min(blueberry_rect.x, screen_width - blueberry_rect.width))
    blueberry_rect.y = max(80, min(blueberry_rect.y, screen_height - blueberry_rect.height))

    if game_active:

        print(snake_body)

        snake_body.insert(0, (rect_x, rect_y))

        display_score(current_score)

        # Displaying blueberry image
        surface.blit(blueberry_surf, blueberry_rect)

        # Drawing Snake
        snake_head_rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
        snake_head = pygame.draw.rect(surface, red, snake_head_rect)

        # Collisions
        if snake_head.colliderect(blueberry_rect):
            blueberry_rect.center = (random.randint(0, 380), random.randint(80, 380))
            current_score += 1
        elif len(snake_body) > 1:
            snake_body.pop(len(snake_body) - 1)

    for block in snake_body:
        pygame.draw.rect(surface, red, pygame.Rect(block[0], block[1], rect_width, rect_height))

    pygame.display.update()
    clock.tick(10)
