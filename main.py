import random
import sys

# Увеличиваем лимит рекурсии (для больших лабиринтов стек вызовов будет глубоким)
sys.setrecursionlimit(10000)

def generate_maze(w, h):
    # Создаем матрицу, полностью заполненную стенами
    grid = [['#' for _ in range(2 * w + 1)] for _ in range(2 * h + 1)]
    
    def carve_passages(cx, cy):
        # Отмечаем текущую комнату как пустой проход
        grid[2 * cy + 1][2 * cx + 1] = ' '
        
        # Направления: вправо, вниз, влево, вверх
        dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        random.shuffle(dirs) # Рандомизация дает уникальную архитектуру каждый запуск
        
        for dx, dy in dirs:
            nx, ny = cx + dx, cy + dy
            # Проверяем, что соседняя комната в пределах графа и еще является "стеной"
            if 0 <= nx < w and 0 <= ny < h and grid[2 * ny + 1][2 * nx + 1] == '#':
                # Сносим стену между текущей комнатой и соседом
                grid[2 * cy + 1 + dy][2 * cx + 1 + dx] = ' '
                # Рекурсивно переходим в новую комнату
                carve_passages(nx, ny)
                
    # Запускаем генерацию с верхней левой комнаты графа (0, 0)
    carve_passages(0, 0)
    
    # Открываем вход и выход
    grid[1][0] = ' '              # Вход слева вверху
    grid[2 * h - 1][2 * w] = ' '  # Выход справа внизу
    
    return grid

def solve_maze(grid, x, y, end_x, end_y):
    # Базовый случай: достигли координаты выхода
    if x == end_x and y == end_y:
        grid[y][x] = '*'
        return True
    
    # Шагаем только по свободным проходам
    if grid[y][x] == ' ':
        # Оптимистично помечаем как часть правильного пути
        grid[y][x] = '*'
        
        # Проверяем 4 направления с шагом в 1 клетку
        dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            # Проверка границ массива
            if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):
                # Если рекурсивный вызов нашел выход, пробрасываем True наверх
                if solve_maze(grid, nx, ny, end_x, end_y):
                    return True
        
        # BACKTRACKING: Все направления вокруг оказались тупиками или стенами.
        # Откатываемся: затираем звездочку и помечаем точку как "плохой маршрут".
        grid[y][x] = '.'
        return False
        
    return False

# Вспомогательная функция для красивого консольного вывода
def print_grid(grid):
    for row in grid:
        # Прячем следы тупиков, чтобы они не мусорили вывод в консоли
        clean_row = [' ' if c == '.' else c for c in row]
        print("".join(clean_row))


if __name__ == "__main__":
    width, height = 15, 10
    
    print("Сгенерированный лабиринт:")
    maze = generate_maze(width, height)
    print_grid(maze)
    
    print("\nРешенный лабиринт:")
    # Координаты входа и выхода в абсолютных индексах матрицы
    start_x, start_y = 0, 1
    end_x, end_y = 2 * width, 2 * height - 1
    
    solve_maze(maze, start_x, start_y, end_x, end_y)
    print_grid(maze)