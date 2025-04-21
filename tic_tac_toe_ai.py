import pygame
import sys
import json
import re
from collections import deque
from crewai import Crew, Agent, Task
from langchain.llms import Ollama
import os

pygame.init()

KEY="OPENAI_API_KEY"
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
os.environ["OPENAI_API_KEY"] = KEY

board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
x_positions = deque()  
o_positions = deque()  
player = 'X'
game_over = False
winner = None
game_state = "menu"
ai_mode = False  

try:    
    ai_agent = Agent(
        role="Tic Tac Toe Strategist",
        goal="Win or block the opponent using optimal strategy",
        backstory="You're a master of Tic Tac Toe trained to think logically about each move.",
        verbose=True,
        allow_delegation=False,
        llm="gpt-4o-mini",
    )
    ai_available = True
except Exception as e:
    print(f"AI initialization failed: {e}")
    ai_available = False

title_font = pygame.font.SysFont(None, 80)
button_font = pygame.font.SysFont(None, 50)
winner_font = pygame.font.SysFont(None, 70)
mode_font = pygame.font.SysFont(None, 40)

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

play_pvp_button = Button(WIDTH//4, HEIGHT//2 - 50, WIDTH//2, 70, "Player vs Player")
play_ai_button = Button(WIDTH//4, HEIGHT//2 + 50, WIDTH//2, 70, "Player vs AI")
exit_button = Button(WIDTH//4, HEIGHT//2 + 150, WIDTH//2, 70, "Exit")

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

def get_ai_move():
    board_string = "\n".join([" ".join(["_" if not c else c for c in row]) for row in board])
    print("Current board state sent to AI:")
    print(board_string)
    instructions = f"""
Here is the current Tic Tac Toe board (X, O, or _ for empty):
{board_string}

You are 'O'. It's your turn.

Important rules:
1. This is a special Tic Tac Toe variant where each player can only have 3 pieces on the board at once.
2. When a player places a 4th piece, their oldest piece is removed.
3. You MUST choose an EMPTY space (marked with _).
4. Do NOT choose spaces that already contain X or O.

Your task:
- Return the best move as JSON: {{ "row": <0-2>, "col": <0-2> }}
- Only return the JSON. No extra explanation.
- If you see a winning move, take it.
- If you can't win immediately, block the opponent's winning move.
- If neither is possible, prefer the center, then corners, then edges.
- Always check that your chosen space is empty before returning.

Remember: Only select positions marked with _ in the board representation.
"""

    task = Task(
        description=instructions,
        expected_output="The best move as JSON: { \"row\": 0, \"col\": 2 }",
        agent=ai_agent
    )

    crew = Crew(
        agents=[ai_agent],
        tasks=[task],
        verbose=False
    )

    try:
        crew_result = crew.kickoff()
        result = str(crew_result)
        print("[AI OUTPUT]:", result)

        match = re.search(r'\{.*?\}', result)
        if match:
            move = json.loads(match.group())
            return move["row"], move["col"]
    except Exception as e:
        print("Failed to parse AI move:", e)
        return get_fallback_ai_move()

def get_fallback_ai_move():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                board[row][col] = 'O'
                if check_winner() == 'O':
                    board[row][col] = None
                    return row, col
                board[row][col] = None
    
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                board[row][col] = 'X'
                if check_winner() == 'X':
                    board[row][col] = None
                    return row, col
                board[row][col] = None
    
    if board[1][1] is None:
        return 1, 1
    
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    for row, col in corners:
        if board[row][col] is None:
            return row, col
    
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                return row, col
    
    return None

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
        
        if ai_mode and player == 'O' and not game_over:
            pygame.display.update()
            pygame.time.delay(500)
            
            if ai_available:
                ai_row, ai_col = get_ai_move()
                if ai_row is not None and ai_col is not None:
                    make_move(ai_row, ai_col)
            else:
                ai_row, ai_col = get_fallback_ai_move()
                if ai_row is not None and ai_col is not None:
                    make_move(ai_row, ai_col)


def draw_board():
    screen.fill(BG_COLOR)
    draw_lines()
    draw_figures()
    
    if not game_over:
        if ai_mode and player == 'O':
            turn_text = mode_font.render("AI is thinking...", True, TEXT_COLOR)
        else:
            turn_text = mode_font.render(f"Player {1 if player == 'X' else 2}'s Turn", True, TEXT_COLOR)
        
        turn_rect = turn_text.get_rect(center=(WIDTH//2, 30))
        screen.blit(turn_text, turn_rect)
    
    if game_over and winner:
        draw_winning_line(winner)

def draw_menu():
    screen.fill(MENU_BG_COLOR)
    
    title_text = title_font.render("Advanced Tic Tac Toe", True, TEXT_COLOR)
    title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//4))
    screen.blit(title_text, title_rect)
    
    play_pvp_button.draw()
    
    if ai_available:
        play_ai_button.draw()
    else:
        pygame.draw.rect(screen, (150, 150, 150), play_ai_button.rect, border_radius=10)
        text_surface = button_font.render(play_ai_button.text, True, (200, 200, 200))
        text_rect = text_surface.get_rect(center=play_ai_button.rect.center)
        screen.blit(text_surface, text_rect)
        
        ai_text = mode_font.render("AI mode not available - Ollama not found", True, (255, 200, 200))
        ai_rect = ai_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 120))
        screen.blit(ai_text, ai_rect)
    
    exit_button.draw()

def draw_end_screen():
    screen.fill(MENU_BG_COLOR)
    
    if ai_mode and winner == 'O':
        winner_text = winner_font.render("AI Won!", True, TEXT_COLOR)
    elif winner == 'X':
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
                if play_pvp_button.is_clicked(event.pos):
                    game_state = "game"
                    ai_mode = False
                    reset_game()
                elif play_ai_button.is_clicked(event.pos) and ai_available:
                    game_state = "game"
                    ai_mode = True
                    reset_game()
                elif exit_button.is_clicked(event.pos):
                    pygame.quit()
                    sys.exit()
            
            elif game_state == "game":
                if not game_over and (not ai_mode or player == 'X'):
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
        play_pvp_button.check_hover(mouse_pos)
        if ai_available:
            play_ai_button.check_hover(mouse_pos)
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