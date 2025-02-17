import pygame

pygame.init()

WIDTH, HEIGHT = 500, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

# Define colors
Cream = (255, 253, 208)
Green = (107, 142, 35)

# Board settings
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Load images once outside the loop for performance
PIECES = {
    "wp": pygame.image.load("wp.png"),
    "wr": pygame.image.load("wR.png"),
    "wn": pygame.image.load("wN.png"),
    "wb": pygame.image.load("wB.png"),
    "wq": pygame.image.load("wQ.png"),
    "wk": pygame.image.load("wK.png"),
    "bp": pygame.image.load("bp.png"),
    "br": pygame.image.load("bR.png"),
    "bn": pygame.image.load("bN.png"),
    "bb": pygame.image.load("bB.png"),
    "bq": pygame.image.load("bQ.png"),
    "bk": pygame.image.load("bK.png"),
}

# Initial board setup
board = [
    ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
    ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
    ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"],
]

# Turn variable to alternate between white and black
turn = "white"


def draw_board(win):
    win.fill(Cream)
    for row in range(ROWS):
        for col in range(row % 2, COLS, 2):
            pygame.draw.rect(win, Green, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def draw_pieces(win, board):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != "--":  # If the square is not empty
                win.blit(PIECES[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


# Move validation functions
def is_valid_move(piece, start_pos, end_pos, board):
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    if piece == "--":
        return False
    piece_type = piece[1]

    # Pawn Movement
    if piece_type == 'p':
        return is_valid_pawn_move(piece, start_pos, end_pos, board)

    # Rook Movement
    elif piece_type == 'r':
        return is_valid_rook_move(start_pos, end_pos, board)

    # Knight Movement
    elif piece_type == 'n':
        return is_valid_knight_move(start_pos, end_pos)

    # Bishop Movement
    elif piece_type == 'b':
        return is_valid_bishop_move(start_pos, end_pos, board)

    # Queen Movement (Rook + Bishop moves)
    elif piece_type == 'q':
        return is_valid_rook_move(start_pos, end_pos, board) or is_valid_bishop_move(start_pos, end_pos, board)

    # King Movement (One square in any direction)
    elif piece_type == 'k':
        return is_valid_king_move(start_pos, end_pos, board)

    return False


# Pawn-specific logic
def is_valid_pawn_move(piece, start_pos, end_pos, board):
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    direction = -1 if piece[0] == 'w' else 1  # White moves up (-1), Black moves down (+1)

    # Moving forward
    if start_col == end_col and board[end_row][end_col] == "--":
        if start_row + direction == end_row:
            return True
        if (piece[0] == "w" and start_row == 6) or (piece[0] == "b" and start_row == 1):
            if start_row + (2 * direction) == end_row and board[start_row + direction][end_col] == "--":
                return True

    # Capturing diagonally
    if abs(start_col - end_col) == 1 and start_row + direction == end_row:
        if board[end_row][end_col] != "--" and board[end_row][end_col][0] != piece[0]:
            return True

    return False


# Rook-specific logic
def is_valid_rook_move(start_pos, end_pos, board):
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    if start_row != end_row and start_col != end_col:
        return False

    if start_row == end_row:
        step = 1 if start_col < end_col else -1
        for col in range(start_col + step, end_col, step):
            if board[start_row][col] != "--":
                return False
    else:
        step = 1 if start_row < end_row else -1
        for row in range(start_row + step, end_row, step):
            if board[row][start_col] != "--":
                return False

    return True


# Knight-specific logic
def is_valid_knight_move(start_pos, end_pos):
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    if (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or (
            abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2):
        return True
    return False


# Bishop-specific logic
def is_valid_bishop_move(start_pos, end_pos, board):
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    if abs(start_row - end_row) != abs(start_col - end_col):
        return False

    row_step = 1 if end_row > start_row else -1
    col_step = 1 if end_col > start_col else -1

    row, col = start_row + row_step, start_col + col_step
    while row != end_row and col != end_col:
        if board[row][col] != "--":
            return False
        row += row_step
        col += col_step

    return True


# King-specific logic (Move one square in any direction)
def is_valid_king_move(start_pos, end_pos, board):
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1:
        return True

    return False


def main():
    global turn
    run = True
    clock = pygame.time.Clock()

    selected_piece = None
    selected_pos = None

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)

                if selected_piece:
                    # Try to move the piece to the new position
                    if is_valid_move(selected_piece, selected_pos, (row, col), board):
                        # Move the piece
                        board[row][col] = selected_piece
                        board[selected_pos[0]][selected_pos[1]] = "--"
                        # Switch turns
                        turn = "black" if turn == "white" else "white"
                    selected_piece = None
                    selected_pos = None
                else:
                    # Select a piece if it's the player's turn
                    if board[row][col] != "--" and board[row][col][0] == turn[0]:
                        selected_piece = board[row][col]
                        selected_pos = (row, col)

        draw_board(WIN)
        draw_pieces(WIN, board)
        pygame.display.update()

    pygame.quit()


main()
