import pygame
import sys
from src.ui.grid_window import GridWindow
from src.utils.input_handler import get_grid_dimensions

def main():
    # Initialize Pygame
    pygame.init()
    
    # Get grid dimensions from user
    grid_width, grid_height = get_grid_dimensions()
    
    print(f"\nCreating {grid_width}x{grid_height} grid...")
    
    # Create and run the grid window
    window = GridWindow(grid_width, grid_height)
    window.run()
    
    pygame.quit()
    sys.exit(0)

if __name__ == "__main__":
    main()