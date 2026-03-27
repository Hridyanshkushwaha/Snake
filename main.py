import pygame
import random
import sys

# Initialize
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
CELL = 20
ROWS = HEIGHT // CELL
COLS = WIDTH // CELL
FPS = 10

# Colors
BLACK  = (0, 0, 0)
GREEN  = (0, 200, 80)
DGREEN = (0, 150, 50)
RED    = (220, 50, 50)
WHITE  = (255, 255, 255)
GRAY   = (30, 30, 30)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 28, bold=True)
big_font = pygame.font.SysFont("monospace", 48, bold=True)


def draw_cell(x, y, color, inner=None):
    rect = pygame.Rect(x * CELL + 1, y * CELL + 1, CELL - 2, CELL - 2)
    pygame.draw.rect(screen, color, rect, border_radius=4)
    if inner:
        inner_rect = rect.inflate(-6, -6)
        pygame.draw.rect(screen, inner, inner_rect, border_radius=2)


def draw_grid():
    for x in range(COLS):
        for y in range(ROWS):
            pygame.draw.rect(screen, GRAY,
                             pygame.Rect(x * CELL, y * CELL, CELL, CELL), 1)


def random_food(snake):
    while True:
        pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        if pos not in snake:
            return pos


def show_text_center(text, fnt, color, y_offset=0):
    surf = fnt.render(text, True, color)
    rect = surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(surf, rect)


def main():
    snake = [(COLS // 2, ROWS // 2)]
    direction = (1, 0)
    next_dir = direction
    food = random_food(snake)
    score = 0
    game_over = False

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key in (pygame.K_r, pygame.K_RETURN):
                        main()  # restart
                        return
                else:
                    if event.key == pygame.K_UP    and direction != (0, 1):
                        next_dir = (0, -1)
                    elif event.key == pygame.K_DOWN  and direction != (0, -1):
                        next_dir = (0, 1)
                    elif event.key == pygame.K_LEFT  and direction != (1, 0):
                        next_dir = (-1, 0)
                    elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                        next_dir = (1, 0)

        if not game_over:
            direction = next_dir
            head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

            # Wall collision
            if not (0 <= head[0] < COLS and 0 <= head[1] < ROWS):
                game_over = True
            # Self collision
            elif head in snake:
                game_over = True
            else:
                snake.insert(0, head)
                if head == food:
                    score += 1
                    food = random_food(snake)
                else:
                    snake.pop()

        # Draw
        screen.fill(BLACK)
        draw_grid()

        # Food
        draw_cell(food[0], food[1], RED)

        # Snake
        for i, seg in enumerate(snake):
            color = GREEN if i > 0 else DGREEN
            inner = DGREEN if i > 0 else GREEN
            draw_cell(seg[0], seg[1], color, inner)

        # Score
        score_surf = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surf, (10, 10))

        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))
            show_text_center("GAME OVER", big_font, RED, -40)
            show_text_center(f"Score: {score}", font, WHITE, 20)
            show_text_center("Press R to restart", font, GRAY, 60)

        pygame.display.flip()


main()