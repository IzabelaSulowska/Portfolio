# Created by Izabela Sulowska

import pygame
import sys

# --- Initialization ---
pygame.init()

# Window and board dimensions
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 6
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# Window settings
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BG_COLOR)

# Board
board = [[0]*BOARD_COLS for _ in range(BOARD_ROWS)]

# --- Functions ---
def draw_lines():
    # Horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2*SQUARE_SIZE), (WIDTH, 2*SQUARE_SIZE), LINE_WIDTH)
    # Vertical lines
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2*SQUARE_SIZE, 0), (2*SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:  # Cross
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col*SQUARE_SIZE + SPACE, row*SQUARE_SIZE + SPACE),
                                 (col*SQUARE_SIZE + SQUARE_SIZE - SPACE, row*SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col*SQUARE_SIZE + SPACE, row*SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col*SQUARE_SIZE + SQUARE_SIZE - SPACE, row*SQUARE_SIZE + SPACE),
                                 CROSS_WIDTH)
            elif board[row][col] == 2:  # Circle
                pygame.draw.circle(screen, CIRCLE_COLOR,
                                   (col*SQUARE_SIZE + SQUARE_SIZE//2, row*SQUARE_SIZE + SQUARE_SIZE//2),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == 0

def is_board_full():
    for row in board:
        if 0 in row:
            return False
    return True

def draw_win_line(start_pos, end_pos):
    pygame.draw.line(screen, (168, 52, 139), start_pos, end_pos, 15)

def check_win(player):
    # --- Rows ---
    for row in range(BOARD_ROWS):
        if all(board[row][col] == player for col in range(BOARD_COLS)):
            y = row * SQUARE_SIZE + SQUARE_SIZE // 2
            draw_win_line((0, y), (WIDTH, y))
            return True

    # --- Columns ---
    for col in range(BOARD_COLS):
        if all(board[row][col] == player for row in range(BOARD_ROWS)):
            x = col * SQUARE_SIZE + SQUARE_SIZE // 2
            draw_win_line((x, 0), (x, HEIGHT))
            return True

    # --- Diagonal top-left → bottom-right ---
    if all(board[i][i] == player for i in range(BOARD_ROWS)):
        draw_win_line((0, 0), (WIDTH, HEIGHT))
        return True

    # --- Diagonal top-right → bottom-left ---
    if all(board[i][BOARD_ROWS - 1 - i] == player for i in range(BOARD_ROWS)):
        draw_win_line((WIDTH, 0), (0, HEIGHT))
        return True

    return False


def restart():
    screen.fill(BG_COLOR)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0

# --- Main loop ---
draw_lines()
player = 1
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX, mouseY = event.pos

            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE

            if available_square(clicked_row, clicked_col):
                mark_square(clicked_row, clicked_col, player)

                # draw figures FIRST
                screen.fill(BG_COLOR)
                draw_lines()
                draw_figures()

                # check for a win
                if check_win(player):
                    game_over = True
                else:
                    # switch player only if there is NO win
                    player = 2 if player == 1 else 1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                player = 1
                game_over = False

    pygame.display.update()
