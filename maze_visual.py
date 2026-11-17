import pygame
import random
import sys

# Расширяем лимит рекурсии
sys.setrecursionlimit(10000)

# ================= НАСТРОЙКИ =================
CELL_SIZE = 25     # Размер одной клетки в пикселях
MAZE_W = 20        # Ширина лабиринта (в комнатах)
MAZE_H = 15        # Высота лабиринта (в комнатах)
DELAY_MS = 20      # Скорость анимации (задержка в миллисекундах)

# Вычисляем реальные размеры матрицы
ROWS = 2 * MAZE_H + 1
COLS = 2 * MAZE_W + 1
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

# Цвета (RGB)
COLOR_WALL = (35, 40, 48)       # Темно-синий/серый (стены)
COLOR_PATH = (240, 245, 250)    # Белый (проходы)
COLOR_GOOD_PATH = (46, 204, 113) # Зеленый (алгоритм идет вперед)
COLOR_BAD_PATH = (231, 76, 60)   # Красный (тупик, откат)

# ================= АЛГОРИТМЫ =================

def generate_maze(w, h):
    """Мгновенно генерирует лабиринт."""
    grid = [['#' for _ in range(2 * w + 1)] for _ in range(2 * h + 1)]
    
    def carve_passages(cx, cy):
        grid[2 * cy + 1][2 * cx + 1] = ' '
        dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        random.shuffle(dirs)
        
        for dx, dy in dirs:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < w and 0 <= ny < h and grid[2 * ny + 1][2 * nx + 1] == '#':
                grid[2 * cy + 1 + dy][2 * cx + 1 + dx] = ' '
                carve_passages(nx, ny)
                
    carve_passages(0, 0)
    grid[1][0] = ' '              # Вход
    grid[ROWS - 2][COLS - 1] = ' ' # Выход
    return grid

def draw_maze(screen, grid):
    """Отрисовывает текущее состояние матрицы на экране."""
    for y in range(ROWS):
        for x in range(COLS):
            rect = (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[y][x] == '#':
                pygame.draw.rect(screen, COLOR_WALL, rect)
            elif grid[y][x] == ' ':
                pygame.draw.rect(screen, COLOR_PATH, rect)
            elif grid[y][x] == '*':
                # Зеленый квадрат чуть меньше размера клетки для эстетики
                pygame.draw.rect(screen, COLOR_PATH, rect) 
                pygame.draw.rect(screen, COLOR_GOOD_PATH, (x*CELL_SIZE+4, y*CELL_SIZE+4, CELL_SIZE-8, CELL_SIZE-8))
            elif grid[y][x] == '.':
                pygame.draw.rect(screen, COLOR_PATH, rect)
                pygame.draw.rect(screen, COLOR_BAD_PATH, (x*CELL_SIZE+6, y*CELL_SIZE+6, CELL_SIZE-12, CELL_SIZE-12))

def solve_maze_visual(grid, x, y, end_x, end_y, screen):
    """Рекурсивный решатель, который обновляет экран на каждом шаге."""
    
    # Обрабатываем системные события, чтобы окно не зависло (Not Responding)
    pygame.event.pump()

    if x == end_x and y == end_y:
        grid[y][x] = '*'
        draw_maze(screen, grid)
        pygame.display.flip()
        return True
    
    if grid[y][x] == ' ':
        grid[y][x] = '*' # Отмечаем путь зеленым
        
        # --- АНИМАЦИЯ ШАГА ВПЕРЕД ---
        draw_maze(screen, grid)
        pygame.display.flip()       # Применяем изменения на экран
        pygame.time.delay(DELAY_MS) # Замораживаем кадр
        
        dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= ny < ROWS and 0 <= nx < COLS:
                if solve_maze_visual(grid, nx, ny, end_x, end_y, screen):
                    return True
        
        # Если цикл for закончился, значит это ТУПИК. 
        grid[y][x] = '.' # Меняем цвет на красный
        
        # --- АНИМАЦИЯ ОТКАТА ---
        draw_maze(screen, grid)
        pygame.display.flip()
        pygame.time.delay(DELAY_MS)
        
        return False
    return False

# ================= ЗАПУСК =================

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Визуализация Рекурсии: Поиск выхода")
    
    # 1. Генерируем лабиринт (в оперативной памяти, мгновенно)
    grid = generate_maze(MAZE_W, MAZE_H)
    
    start_x, start_y = 0, 1
    end_x, end_y = COLS - 1, ROWS - 2
    
    # 2. Отрисовываем чистый лабиринт
    screen.fill(COLOR_WALL)
    draw_maze(screen, grid)
    pygame.display.flip()
    
    # Ждем полторы секунды, чтобы зритель успел рассмотреть лабиринт
    pygame.time.wait(1500)
    
    # 3. Запускаем анимацию решения
    solve_maze_visual(grid, start_x, start_y, end_x, end_y, screen)
    
    # 4. Бесконечный цикл, чтобы окно не закрылось после нахождения выхода
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
    pygame.quit()

if __name__ == '__main__':
    main()