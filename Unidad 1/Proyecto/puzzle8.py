import tkinter as tk
import random
from heapq import heappush, heappop

# Datos de la cuadrícula
grid_values = [
    ["5", "1", "3"],
    ["8", "4", "7"],
    ["2", "", "6"]  # Espacio vacío
]

# Crear la ventana
root = tk.Tk()
root.title("Puzzle 8")
root.configure(bg="blue")

# Variables globales
buttons = []
empty_pos = (2, 1)  # Posición inicial del espacio vacío
edit_mode = False
entry_widgets = []
move_count = 0  # Contador de movimientos

def swap(x, y):
    global empty_pos, move_count
    if edit_mode:
        return
    ex, ey = empty_pos
    if (abs(ex - x) == 1 and ey == y) or (abs(ey - y) == 1 and ex == x):
        grid_values[ex][ey], grid_values[x][y] = grid_values[x][y], ""
        empty_pos = (x, y)
        move_count += 1  # Aumentar contador
        update_grid()
        update_move_count()
        check_win()

def shuffle_grid():
    global grid_values, empty_pos, move_count
    nums = ["1", "2", "3", "4", "5", "6", "7", "8", ""]
    random.shuffle(nums)
    grid_values = [nums[i:i+3] for i in range(0, 9, 3)]
    for i in range(3):
        for j in range(3):
            if grid_values[i][j] == "":
                empty_pos = (i, j)
    move_count = 0  # Reiniciar contador
    update_grid()
    update_move_count()

def check_win():
    """ Verifica si el usuario ha ganado. """
    correct = ["1", "2", "3", "4", "5", "6", "7", "8", ""]
    current = [grid_values[i][j] for i in range(3) for j in range(3)]
    if current == correct:
        show_win_message()

def show_win_message():
    """ Muestra un mensaje de victoria en una ventana emergente. """
    win_window = tk.Toplevel(root)
    win_window.title("¡Ganaste!")
    win_window.configure(bg="green")
    
    label = tk.Label(win_window, text="¡Ganaste!", font=("Arial", 50, "bold"), fg="white", bg="green")
    label.pack(expand=True, padx=50, pady=50)

    move_label = tk.Label(win_window, text=f"Movimientos: {move_count}", font=("Arial", 20), fg="navy", bg="green")
    move_label.pack(expand=True, padx=50, pady=10)

def update_move_count():
    """ Actualiza el label de movimientos. """
    move_label.config(text=f"Movimientos: {move_count}")

def enter_edit_mode():
    global edit_mode, entry_widgets
    edit_mode = True
    entry_widgets.clear()
    for i in range(3):
        for j in range(3):
            entry = tk.Entry(root, font=("Arial", 24), width=4, justify='center')
            value = "" if grid_values[i][j] == "" else grid_values[i][j]
            entry.insert(0, value)
            entry.grid(row=i, column=j, padx=2, pady=2)
            entry_widgets.append((i, j, entry))
    update_side_buttons(editing=True)

def save_custom_grid():
    global grid_values, empty_pos, edit_mode, entry_widgets, move_count
    new_grid = [["" for _ in range(3)] for _ in range(3)]
    new_empty_pos = None  
    
    for i, j, entry in entry_widgets:
        val = entry.get().strip()
        if val == "":
            if new_empty_pos is None:
                new_empty_pos = (i, j)
            else:
                val = "9"  
        new_grid[i][j] = val
    
    if new_empty_pos is None:
        return  
    
    grid_values = new_grid
    empty_pos = new_empty_pos  
    edit_mode = False
    move_count = 0  # Reiniciar contador al editar
    update_grid()
    update_move_count()
    update_side_buttons(editing=False)

def cancel_edit_mode():
    global edit_mode
    edit_mode = False
    update_grid()
    update_side_buttons(editing=False)

def update_grid():
    for widget in root.grid_slaves():
        if isinstance(widget, tk.Button) or isinstance(widget, tk.Entry):
            widget.destroy()
    for i in range(3):
        for j in range(3):
            value = grid_values[i][j]
            btn = tk.Button(
                root, text=value, font=("Arial", 24), width=4, height=2,
                bg="white" if value == "" else "#1E3A5F", fg="black" if value == "" else "white",
                relief=tk.RIDGE, borderwidth=2,
                command=lambda x=i, y=j: swap(x, y)
            )
            btn.grid(row=i, column=j, padx=2, pady=2)
    update_side_buttons(editing=False)

def update_side_buttons(editing=False):
    for widget in side_frame.winfo_children():
        widget.destroy()
    if editing:
        tk.Button(side_frame, text="Guardar", bg="navy", fg="white", font=("Arial", 14), command=save_custom_grid).pack(fill=tk.X, pady=5)
        tk.Button(side_frame, text="Cancelar", bg="maroon", fg="white", font=("Arial", 14), command=cancel_edit_mode).pack(fill=tk.X, pady=5)
    else:
        tk.Button(side_frame, text="Random", bg="purple", fg="white", font=("Arial", 14), command=shuffle_grid).pack(fill=tk.X, pady=5)
        tk.Button(side_frame, text="Editar", bg="#32a87b", fg="white", font=("Arial", 14), command=enter_edit_mode).pack(fill=tk.X, pady=5)
        tk.Button(side_frame, text="Resolver", bg="#21a303", fg="white", font=("Arial", 14), command=solve_puzzle).pack(fill=tk.X, pady=5)

# Algoritmo A* y validación
class PuzzleState:
    def __init__(self, board, parent=None, move=None):
        self.board = board
        self.parent = parent
        self.move = move
        self.g = parent.g + 1 if parent else 0
        self.h = self.manhattan_distance()
        
    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)

    def manhattan_distance(self):
        distance = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != "":
                    num = int(self.board[i][j])
                    target_row = (num-1) // 3
                    target_col = (num-1) % 3
                    distance += abs(i - target_row) + abs(j - target_col)
        return distance

    def get_blank_pos(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    return (i, j)

    def get_neighbors(self):
        neighbors = []
        row, col = self.get_blank_pos()
        directions = [("Arriba", -1, 0), ("Abajo", 1, 0), 
                     ("Izquierda", 0, -1), ("Derecha", 0, 1)]
        
        for move, dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_board = [row.copy() for row in self.board]
                new_board[row][col], new_board[new_row][new_col] = new_board[new_row][new_col], new_board[row][col]
                neighbors.append((move, new_board))
        return neighbors

def validate_grid():
    current = [grid_values[i][j] for i in range(3) for j in range(3)]
    nums = [x if x != "" else "0" for x in current]
    
    # Verificar números válidos
    valid_nums = set("0 1 2 3 4 5 6 7 8".split())
    if set(nums) != valid_nums:
        return False, "Números inválidos o faltantes"
    
    # Verificar si es solucionable (paridad de inversiones)
    inversions = 0
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i] != "0" and nums[j] != "0" and nums[i] > nums[j]:
                inversions += 1
                
    if inversions % 2 != 0:
        return False, "El puzzle no tiene solución"
    
    return True, ""

def solve_puzzle():
    validation, message = validate_grid()
    if not validation:
        tk.messagebox.showerror("Error", message)
        return
    
    # Convertir a formato del solver
    initial_board = []
    for i in range(3):
        row = []
        for j in range(3):
            row.append(grid_values[i][j] if grid_values[i][j] != "" else "")
        initial_board.append(row)
    
    # Ejecutar A*
    solution = a_star(initial_board)
    if solution:
        show_solution_steps(solution, initial_board)
    else:
        tk.messagebox.showerror("Error", "No se encontró solución")

def a_star(initial_board):
    open_heap = []
    closed_set = set()
    
    initial_state = PuzzleState(initial_board)
    heappush(open_heap, initial_state)
    
    while open_heap:
        current = heappop(open_heap)
        
        if current.h == 0:
            path = []
            while current.parent:
                path.append(current.move)
                current = current.parent
            return path[::-1]
        
        closed_set.add(tuple(map(tuple, current.board)))
        
        for move, neighbor in current.get_neighbors():
            neighbor_state = PuzzleState(neighbor, current, move)
            if tuple(map(tuple, neighbor)) not in closed_set:
                heappush(open_heap, neighbor_state)
    
    return None

def show_solution_steps(steps, initial_board):
    solution_window = tk.Toplevel(root)
    solution_window.title("Pasos de Solución")
    
    tk.Label(solution_window, text=f"Total de movimientos: {len(steps)}", 
            font=("Arial", 14)).pack(pady=10)
    
    scroll = tk.Scrollbar(solution_window)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)
    
    listbox = tk.Listbox(solution_window, width=40, height=15, 
                        yscrollcommand=scroll.set)
    listbox.pack(padx=10, pady=10)
    
    for i, step in enumerate(steps, 1):
        listbox.insert(tk.END, f"Paso {i}: Mover {step}")
    
    scroll.config(command=listbox.yview)
    
    # Botón para resolver paso a paso
    tk.Button(solution_window, text="Resolver Paso a Paso", bg="#21a303", fg="white", font=("Arial", 14), 
              command=lambda: execute_steps(steps, initial_board, listbox)).pack(pady=10)

def execute_steps(steps, initial_board, listbox):
    current_board = [row.copy() for row in initial_board]
    
    def execute_step(step_index):
        if step_index >= len(steps):
            return
        
        # Resaltar el paso actual en amarillo
        listbox.selection_clear(0, tk.END)
        listbox.selection_set(step_index)
        listbox.activate(step_index)
        listbox.see(step_index)
        
        # Realizar el movimiento en el tablero principal
        move = steps[step_index]
        move, new_board = apply_move(current_board, move)
        
        # *** Corregido: Actualizar current_board ***
        current_board[:] = [row.copy() for row in new_board]  # Se actualiza con el nuevo estado
        
        # Actualizar el tablero principal
        global grid_values, empty_pos
        grid_values = [row.copy() for row in new_board]
        empty_pos = next((i, j) for i in range(3) for j in range(3) if grid_values[i][j] == "")
        update_grid()
        
        # Esperar 1/3 de segundo antes del siguiente paso
        root.after(333, execute_step, step_index + 1)
    
    execute_step(0)


def apply_move(board, move):
    row, col = next((i, j) for i in range(3) for j in range(3) if board[i][j] == "")
    if move == "Arriba":
        new_row, new_col = row - 1, col  # Movimiento hacia arriba
    elif move == "Abajo":
        new_row, new_col = row + 1, col  # Movimiento hacia abajo
    elif move == "Izquierda":
        new_row, new_col = row, col - 1  # Movimiento hacia la izquierda
    elif move == "Derecha":
        new_row, new_col = row, col + 1  # Movimiento hacia la derecha
    
    # Verificar límites del tablero
    if 0 <= new_row < 3 and 0 <= new_col < 3:
        new_board = [row.copy() for row in board]
        new_board[row][col], new_board[new_row][new_col] = new_board[new_row][new_col], new_board[row][col]
        return move, new_board
    else:
        return move, board  # No se realiza el movimiento si está fuera de los límites

# Crear el panel lateral
side_frame = tk.Frame(root, bg="blue")
side_frame.grid(row=0, column=3, rowspan=3, padx=10, pady=10, sticky="ns")

# Label para los movimientos (abajo a la derecha)
move_label = tk.Label(root, text="Movimientos: 0", font=("Arial", 14, "bold"), fg="white", bg="blue")
move_label.grid(row=3, column=2, columnspan=2, sticky="e", padx=10, pady=10)

# Inicializar la cuadrícula y botones
update_grid()

# Iniciar la interfaz
tk.mainloop()
