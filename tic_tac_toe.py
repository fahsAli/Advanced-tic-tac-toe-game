import pygame
import sys
from collections import deque

pygame.init()

WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
FADED_CIRCLE_COLOR = (180, 175, 160)
FADED_CROSS_COLOR = (150, 150, 150)
MENU_BG_COLOR = (52, 152, 219)
BUTTON_COLOR = (41, 128, 185)
BUTTON_HOVER_COLOR = (26, 88, 126)
TEXT_COLOR = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Advanced Tic Tac Toe')

board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
x_positions = deque()  
o_positions = deque()  
player = 'X'
game_over = False
winner = None
game_state = "menu"   


title_font = pygame.font.SysFont(None, 80)
button_font = pygame.font.SysFont(None, 50)
winner_font = pygame.font.SysFont(None, 70)

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.is_hovered = False
    
    def draw(self):
        color = BUTTON_HOVER_COLOR if self.is_hovered else BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        
        text_surface = button_font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

play_button = Button(WIDTH//4, HEIGHT//2, WIDTH//2, 70, "Play")
exit_button = Button(WIDTH//4, HEIGHT//2 + 100, WIDTH//2, 70, "Exit")

play_again_button = Button(WIDTH//4, HEIGHT//2 + 50, WIDTH//2, 70, "Play Again")
menu_button = Button(WIDTH//4, HEIGHT//2 + 150, WIDTH//2, 70, "Main Menu")

def draw_lines():
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'X':
                is_oldest_x = len(x_positions) >= 3 and (row, col) == x_positions[0]
                
                color = FADED_CROSS_COLOR if is_oldest_x else CROSS_COLOR
                pygame.draw.line(
                    screen, color,
                    (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                    ((col + 1) * SQUARE_SIZE - SPACE, (row + 1) * SQUARE_SIZE - SPACE),
                    CROSS_WIDTH
                )
                pygame.draw.line(
                    screen, color,
                    ((col + 1) * SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE),
                    (col * SQUARE_SIZE + SPACE, (row + 1) * SQUARE_SIZE - SPACE),
                    CROSS_WIDTH
                )
            elif board[row][col] == 'O':
                is_oldest_o = len(o_positions) >= 3 and (row, col) == o_positions[0]
                
                color = FADED_CIRCLE_COLOR if is_oldest_o else CIRCLE_COLOR
                pygame.draw.circle(
                    screen, color,
                    (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                    CIRCLE_RADIUS, CIRCLE_WIDTH
                )

def check_winner():
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0]:
            return board[row][0]
    
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col]:
            return board[0][col]
    
    if board[0][0] == board[1][1] == board[2][2] and board[0][0]:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2]:
        return board[0][2]
    
    return None

def draw_winning_line(winner):
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] == winner:
            y = row * SQUARE_SIZE + SQUARE_SIZE // 2
            pygame.draw.line(
                screen, (255, 0, 0), 
                (15, y), (WIDTH - 15, y), 15
            )
            return
    
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] == winner:
            x = col * SQUARE_SIZE + SQUARE_SIZE // 2
            pygame.draw.line(
                screen, (255, 0, 0), 
                (x, 15), (x, HEIGHT - 15), 15
            )
            return
    
    if board[0][0] == board[1][1] == board[2][2] == winner:
        pygame.draw.line(
            screen, (255, 0, 0), 
            (15, 15), (WIDTH - 15, HEIGHT - 15), 15
        )
        return
    
    if board[0][2] == board[1][1] == board[2][0] == winner:
        pygame.draw.line(
            screen, (255, 0, 0), 
            (WIDTH - 15, 15), (15, HEIGHT - 15), 15
        )
        return

def reset_game():
    global board, player, game_over, winner, x_positions, o_positions
    board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    x_positions = deque()
    o_positions = deque()
    player = 'X'
    game_over = False
    winner = None
    screen.fill(BG_COLOR)
    draw_lines()

def make_move(row, col):
    global player, board, game_state, game_over, winner
    
    if board[row][col] is None and not game_over:
        if player == 'X':
            if len(x_positions) >= 3:
                old_row, old_col = x_positions.popleft()
                board[old_row][old_col] = None
            x_positions.append((row, col))
        else:  
            if len(o_positions) >= 3:
                old_row, old_col = o_positions.popleft()
                board[old_row][old_col] = None
            o_positions.append((row, col))
        
        board[row][col] = player
        
        result = check_winner()
        if result:
            game_over = True
            winner = result
            draw_board()
            pygame.display.update()
            pygame.time.delay(1000) 
            game_state = "end_screen"
            return
        
        player = 'O' if player == 'X' else 'X'
        
        draw_board()


def draw_board():
    screen.fill(BG_COLOR)
    draw_lines()
    draw_figures()
    if game_over and winner:
        draw_winning_line(winner)

def draw_menu():
    screen.fill(MENU_BG_COLOR)
    
    title_text = title_font.render("Advanced Tic Tac Toe", True, TEXT_COLOR)
    title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//4))
    screen.blit(title_text, title_rect)
    
    play_button.draw()
    exit_button.draw()

def draw_end_screen():
    screen.fill(MENU_BG_COLOR)
    
    if winner == 'X':
        winner_text = winner_font.render("Player 1 Won!", True, TEXT_COLOR)
    else:
        winner_text = winner_font.render("Player 2 Won!", True, TEXT_COLOR)
    
    winner_rect = winner_text.get_rect(center=(WIDTH//2, HEIGHT//4))
    screen.blit(winner_text, winner_rect)
    
    play_again_button.draw()
    menu_button.draw()

clock = pygame.time.Clock()

while True:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "menu":
                if play_button.is_clicked(event.pos):
                    game_state = "game"
                    reset_game()
                elif exit_button.is_clicked(event.pos):
                    pygame.quit()
                    sys.exit()
            
            elif game_state == "game":
                if not game_over:
                    mouseX = event.pos[0]
                    mouseY = event.pos[1]
                    
                    clicked_row = mouseY // SQUARE_SIZE
                    clicked_col = mouseX // SQUARE_SIZE
                    
                    if 0 <= clicked_row < 3 and 0 <= clicked_col < 3:
                        make_move(clicked_row, clicked_col)
            
            elif game_state == "end_screen":
                if play_again_button.is_clicked(event.pos):
                    game_state = "game"
                    reset_game()
                elif menu_button.is_clicked(event.pos):
                    game_state = "menu"
    
    if game_state == "menu":
        play_button.check_hover(mouse_pos)
        exit_button.check_hover(mouse_pos)
    elif game_state == "end_screen":
        play_again_button.check_hover(mouse_pos)
        menu_button.check_hover(mouse_pos)
    
    if game_state == "menu":
        draw_menu()
    elif game_state == "game":
        draw_board()
    elif game_state == "end_screen":
        draw_end_screen()
    
    pygame.display.update()
    clock.tick(60)  