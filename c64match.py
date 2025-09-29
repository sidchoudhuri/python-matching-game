import random
import time

def create_board(size):
    """Create board"""
    if size * size % 2 != 0:
        print("Error: The board must be an even number of cells!")
        return None

    # List of 2-char symbols
    symbols = ['C=', '64', '8B', 'm0', 'F1', 'F3', 'F5', 'F7']
    # Remember to add symbols if board is bigger than 4x4
    if size * size // 2 > len(symbols):
        symbols = symbols * (size * size // 2 // len(symbols) + 1)

    board_symbols = symbols[:(size * size // 2)] * 2
    random.shuffle(board_symbols)

    grid = []
    for _ in range(size):
        row = [board_symbols.pop() for _ in range(size)]
        grid.append(row)

    return grid

def display_board(board, revealed_status):
    """Display board to con, formatted for 2-char symbols"""
    # Print column with spacing
    print("  " + " ".join(f"{i:2}" for i in range(len(board))))
    for i, row in enumerate(board):
        print(f"{i} ", end="")
        for j, cell in enumerate(row):
            if revealed_status[i][j]:
                # Print the 2-char symbol
                print(f"{cell}", end=" ")
            else:
                # Print 2-chars for alignment
                print("XX", end=" ")
        print()
    print("-" * (len(board) * 3 + 2)) # Separator line

def get_player_move(board_size, message):
    """Player input"""
    while True:
        try:
            position = input(message + f" (row col, e.g., 0 1): ")
            row, col = map(int, position.split())
            if 0 <= row < board_size and 0 <= col < board_size:
                return row, col
            else:
                print("Invalid coordinates!")
        except (ValueError, IndexError):
            print("Invalid input. Enter two numbers separated by a space.")

def play_game():
    """Main game loop"""
    print("Welcome to m0nde's C64 Match!")

    board_size = 4
    board = create_board(board_size)
    if board is None:
        return

    # --- Display Symbols before game starts ---
    all_symbols = set()
    for row in board:
        all_symbols.update(row)
    
    print("\nSymbols to match:")
    print(" ".join(sorted(list(all_symbols))))
    print("-" * 30)
    input("Press Enter to start the game and hide the symbols...")
    # --- End Display Symbols ---

    revealed_status = [[False for _ in range(board_size)] for _ in range(board_size)]
    matched_pairs = 0
    total_pairs = board_size * board_size // 2
    moves_made = 0 # Initialize move counter

    while matched_pairs < total_pairs:
        # Clear screen to hide old state
        print("\n" * 50)

        # Display move counter
        print(f"Moves made: {moves_made}")

        # Display the current state of the board
        display_board(board, revealed_status)

        # Get first guess
        row1, col1 = get_player_move(board_size, "Enter coordinates for the first symbol")
        if revealed_status[row1][col1]:
            print("That's already been matched. Try again.")
            time.sleep(1)
            continue
        revealed_status[row1][col1] = True

        # Display board with 1st selection revealed
        display_board(board, revealed_status)

        # Get second guess
        row2, col2 = get_player_move(board_size, "Enter coordinates for the 2nd symbol")
        # Check if tile was selected twice or is already matched
        if (row1, col1) == (row2, col2) or revealed_status[row2][col2]:
            print("Invalid selection. Try again.")
            revealed_status[row1][col1] = False # Hide the 1st symbol
            time.sleep(1)
            continue
        revealed_status[row2][col2] = True

        # Display board with both revealed
        display_board(board, revealed_status)

        # Valid turn completed, increment moves counter
        moves_made += 1

        # Check for match
        if board[row1][col1] == board[row2][col2]:
            print("It's a match!")
            matched_pairs += 1 # Critical fix: Increment the matched pairs count
        else:
            print("No match. Take a moment to remember their positions!")
            input("Press Enter to continue...") # Wait for input
            revealed_status[row1][col1] = False
            revealed_status[row2][col2] = False

    print(f"Congrats! You matched all the symbols in {moves_made} moves!")

if __name__ == "__main__":
    play_game()
