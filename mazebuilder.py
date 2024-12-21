import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

# Maze dimensions (number of rows and columns must be odd for proper maze layout)
ROWS = 200
COLS = 200
CELL_SIZE = SCREEN_WIDTH // COLS

# Colors
WALL_COLOR = (40, 40, 40)
PATH_COLOR = (200, 200, 200)
START_COLOR = (0, 255, 0)
END_COLOR = (255, 0, 0)
CURRENT_CELL_COLOR = (255, 255, 0)  # Yellow for the current cell
BACKGROUND_COLOR = (0, 0, 0)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Generator (Optimized DFS)")

def draw_maze(maze, start, end, current=None):
    """Draw the maze grid and highlight the current cell."""
    screen.fill(BACKGROUND_COLOR)
    for r in range(ROWS):
        for c in range(COLS):
            color = WALL_COLOR if maze[r][c] == 1 else PATH_COLOR
            pygame.draw.rect(screen, color, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    # Highlight start and end positions
    pygame.draw.rect(screen, START_COLOR, (start[1] * CELL_SIZE, start[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, END_COLOR, (end[1] * CELL_SIZE, end[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    # Highlight the current cell being processed
    if current:
        pygame.draw.rect(screen, CURRENT_CELL_COLOR, (current[1] * CELL_SIZE, current[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.display.flip()

def generate_maze(rows, cols):
    """Generate a maze using Depth-First Search."""
    # Ensure rows and cols are odd for proper maze layout
    if rows % 2 == 0: rows += 1
    if cols % 2 == 0: cols += 1

    # Initialize the maze with all walls
    maze = [[1 for _ in range(cols)] for _ in range(rows)]

    # Starting point
    start = (1, 1)
    end = (rows - 2, cols - 2)
    maze[start[0]][start[1]] = 0

    # Stack for DFS
    stack = [start]
    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]  # Move 2 cells at a time

    def in_bounds(r, c):
        return 0 <= r < rows and 0 <= c < cols

    iteration = 0
    while stack:
        current = stack[-1]
        r, c = current
        random.shuffle(directions)  # Randomize directions

        found = False
        for dr, dc in directions:
            nr, nc = r + dr, c + dc  # Neighbor
            if in_bounds(nr, nc) and maze[nr][nc] == 1:  # If it's a wall
                # Carve a path
                maze[r + dr // 2][c + dc // 2] = 0
                maze[nr][nc] = 0
                stack.append((nr, nc))
                found = True
                break

        # If no neighbors to visit, backtrack
        if not found:
            stack.pop()

        # Visualize every 50 iterations to reduce overhead
        iteration += 1
        if iteration % 100 == 0:
            draw_maze(maze, start, end, current=current)

    # Ensure the end point is accessible
    maze[end[0]][end[1]] = 0
    draw_maze(maze, start, end)  # Final maze rendering
    return maze, start, end

def main():
    """Main function to generate and display the maze."""
    clock = pygame.time.Clock()

    # Generate the maze
    maze, start, end = generate_maze(ROWS, COLS)

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Redraw the maze
        draw_maze(maze, start, end)
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
