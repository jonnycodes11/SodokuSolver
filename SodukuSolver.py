import tkinter as tk

numUnits = 9

def print_board(board):
    for row in range(numUnits):
        if row % 3 == 0 and row != 0:
            print("-----------")
        for col in range(numUnits):
            if col % 3 == 0 and col != 0:
                print("|", end="")
            print(board[row][col], end=" ")
        print()

def is_number_in_row(board, number, row):
    for i in range(numUnits):
        if board[row][i] == number:
            return True
    return False

def is_number_in_column(board, number, column):
    for i in range(numUnits):
        if board[i][column] == number:
            return True
    return False

def is_number_in_box(board, number, row, column):
    local_box_row = row - row % 3
    local_box_column = column - column % 3

    for i in range(local_box_row, local_box_row + 3):
        for j in range(local_box_column, local_box_column + 3):
            if board[i][j] == number:
                return True
    return False

def is_valid_placement(board, number, row, column):
    return not is_number_in_row(board, number, row) and \
           not is_number_in_column(board, number, column) and \
           not is_number_in_box(board, number, row, column)

def solve_board(board):
    for row in range(numUnits):
        for column in range(numUnits):
            if board[row][column] == 0:
                for number_to_try in range(1, numUnits + 1):
                    if is_valid_placement(board, number_to_try, row, column):
                        board[row][column] = number_to_try
                        update_cell(row, column, "yellow")
                        root.update()
                        root.after(20)  # Delay for visual effect

                        if solve_board(board):
                            return True
                        else:
                            board[row][column] = 0
                            update_cell(row, column, "#FF69B4")
                            root.update()
                            root.after(20)  # Delay for visual effect
                return False
    return True

def solve_sudoku():
    global board
    solve_board(board)
    update_gui()

def update_gui():
    for i in range(numUnits):
        for j in range(numUnits):
            cell_var[i][j].set(board[i][j])
            if board[i][j] == 0:
                update_cell(i, j, "white")
            else:
                update_cell(i, j, "black")

def update_cell(row, col, color):
    entry = cell_widgets[row][col]
    entry.config(bg=color)

root = tk.Tk()
root.title("Sudoku Solver")
root.resizable(False, False)

board = [
    [0, 6, 8, 3, 0, 9, 0, 7, 0],
    [0, 4, 2, 0, 0, 0, 0, 0, 1],
    [1, 0, 7, 0, 5, 0, 6, 0, 0],
    [0, 0, 5, 0, 7, 0, 1, 2, 0],
    [7, 0, 0, 0, 0, 1, 5, 8, 0],
    [0, 0, 0, 0, 3, 0, 7, 4, 0],
    [0, 0, 0, 1, 9, 0, 2, 0, 5],
    [8, 0, 1, 6, 2, 0, 3, 9, 0],
    [9, 0, 0, 5, 4, 3, 0, 1, 0]
]

cell_var = [[None for _ in range(numUnits)] for _ in range(numUnits)]
cell_widgets = [[None for _ in range(numUnits)] for _ in range(numUnits)]

main_frame = tk.Frame(root, bg="black")
main_frame.grid(padx=10, pady=10)

for i in range(numUnits):
    for j in range(numUnits):
        cell_var[i][j] = tk.StringVar()
        if board[i][j] != 0:
            cell_var[i][j].set(board[i][j])
        else:
            cell_var[i][j].set(" ")

for i in range(numUnits):
    for j in range(numUnits):
        frame = tk.Frame(main_frame, bg="white", width=50, height=50)
        frame.grid(row=i, column=j, padx=1, pady=1)
        entry = tk.Entry(frame, width=2, font=('Arial', 18, 'bold'), textvariable=cell_var[i][j], justify='center', borderwidth=0)
        entry.pack(expand=True, fill='both')
        cell_widgets[i][j] = entry

solve_button = tk.Button(root, text="Solve Sudoku", command=solve_sudoku)
solve_button.grid(row=numUnits + 1, columnspan=numUnits, pady=10)  # Added padding below the board


root.mainloop()