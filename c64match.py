import random
import time

def create_board(size):
    """Create board"""
    if size * size % 2 != 0:
        print("Error: Board size must result in an even number of cells.")
        return None

    # 2-char symbols
    symbols = ['C=', '64', '8B', 'm0', 'F1', 'F3', 'F5', 'F7']
    # Add symbols if bigger than 4x4
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
    """Display board to console with 2-char symbols"""
    # Print columns with adj spacing
    print("  " + " ".join(f"{i:2}" for i in range(len(board))))
    for i, row in enumerate(board):
        print(f"{i} ", end="")
        for j, cell in enumerate(row):
            if revealed_status[i][j]:
                # Print 2-char symbol
                print(f"{cell}", end=" ")
            else:
                # Alignment
                print("XX", end=" ")
        print()
    print("-" * (len(board) * 3 + 2)) # Adjust separator line length

def get_player_move(board_size, message):
    """Get player input"""
    while True:
        try:
            position = input(message + f" (row col, e.g., 0 1): ")
            row, col = map(int, position.split())
            if 0 <= row < board_size and 0 <= col < board_size:
                return row, col
            else:
                print("Invalid coordinates. Enter numbers within the board size.")
        except (ValueError, IndexError):
            print("Invalid input. Enter two numbers separated by a space.")

def play_game():
    """Main game loop"""
    print("Welcome to m0nde's C64 Memory Game!")
    
    board_size = 4
    board = create_board(board_size)
    if board is None:
        return
        
    revealed_status = [[False for _ in range(board_size)] for _ in range(board_size)]
    matched_pairs = 0
    total_pairs = board_size * board_size // 2

    while matched_pairs < total_pairs:
        # Display current state of board
        display_board(board, revealed_status)

        # Get first guess
        row1, col1 = get_player_move(board_size, "Enter the coordinates for your first guess")
        if revealed_status[row1][col1]:
            print("That's already been matched. Try again.")
            time.sleep(1)
            continue
        revealed_status[row1][col1] = True

        # Display board with first selection revealed
        display_board(board, revealed_status)
        
        # Get second guess
        row2, col2 = get_player_move(board_size, "Enter the coordinates for your second guess")
        # Check if the same tile was selected twice
        if (row1, col1) == (row2, col2) or revealed_status[row2][col2]:
            print("Invalid selection. Try again.")
            revealed_status[row1][col1] = False # Hide the first one again
            time.sleep(1)
            continue
        revealed_status[row2][col2] = True
        
        # Display board with all selections
        display_board(board, revealed_status)

        # Check for match
        if board[row1][col1] == board[row2][col2]:
            print("It's a match!")
            matched_pairs += 1
        else:
            print("No match. Take a moment to remember their positions!")
            input("Press Enter to continue...") # Wait for user input
            revealed_status[row1][col1] = False
            revealed_status[row2][col2] = False
        
        # Clear the screen to hide old state
        print("\n" * 50)

    print("Congrats! You matched all the symbols!")

if __name__ == "__main__":
    play_game()
