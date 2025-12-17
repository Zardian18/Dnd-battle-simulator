import sys

def get_grid_dimensions():
    print("=" * 50)
    print("D&D Battle Simulator - Grid Setup")
    print("=" * 50)
    
    while True:
        try:
            dimensions = input("\nEnter grid size (format: WIDTHxHEIGHT, e.g., 10x15): ").strip()
            
            if 'x' not in dimensions.lower():
                print("Invalid format. Please use WIDTHxHEIGHT (e.g., 10x15)")
                continue
            
            width, height = dimensions.lower().split('x')
            width = int(width)
            height = int(height)
            
            if width <= 0 or height <= 0:
                print("Dimensions must be positive numbers!")
                continue
            
            if width > 100 or height > 100:
                print("Maximum grid size is 100x100")
                continue
            
            return width, height
            
        except ValueError:
            print("Invalid input. Please enter numbers only (e.g., 10x15)")
        except KeyboardInterrupt:
            print("\n\nExiting...")
            sys.exit(0)