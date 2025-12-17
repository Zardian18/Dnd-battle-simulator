import pygame
from src.ui.button import Button2D
from src.ui.character_dialog import CharacterCreationDialog
from src.ui.import_dialog import CharacterImportDialog
from src.utils.constants import *

class GridWindow:
    def __init__(self, grid_width, grid_height):
        self.grid_width = grid_width
        self.grid_height = grid_height
        
        self.window_width = PANEL_WIDTH + grid_width * CELL_SIZE
        self.window_height = grid_height * CELL_SIZE + BOTTOM_PANEL_HEIGHT
        
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(f"D&D Battle Simulator - {grid_width}x{grid_height} Grid")
        
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)
        
        self.characters = []
        self.selected_char = None
        self.placing_char = None
        self.movement_preview_cells = []
        
        self.buttons = [
            Button2D(10, 20, PANEL_WIDTH - 20, 40, "Add Character", self.add_character),
            Button2D(10, 70, PANEL_WIDTH - 20, 40, "Import Character", self.import_character),
            Button2D(10, 120, PANEL_WIDTH - 20, 40, "End Turn", self.end_turn),
            Button2D(10, 170, PANEL_WIDTH - 20, 40, "Delete Entity", self.delete_entity),
        ]
        
        self.clock = pygame.time.Clock()
    
    def add_character(self):
        dialog = CharacterCreationDialog()
        char = dialog.show()
        if char:
            self.placing_char = char
    
    def import_character(self):
        dialog = CharacterImportDialog()
        char = dialog.show()
        if char:
            char.reset_turn()
            self.placing_char = char
    
    def end_turn(self):
        """Reset all characters' resources for a new turn"""
        for char in self.characters:
            char.reset_turn()
        print("Turn ended - all resources restored!")
    
    def delete_entity(self):
        """Delete the selected character from the board"""
        if self.selected_char:
            self.characters.remove(self.selected_char)
            print(f"Deleted {self.selected_char.name} from the board")
            self.selected_char = None
    
    def draw_grid(self):
        for x in range(self.grid_width + 1):
            start_pos = (PANEL_WIDTH + x * CELL_SIZE, 0)
            end_pos = (PANEL_WIDTH + x * CELL_SIZE, self.grid_height * CELL_SIZE)
            pygame.draw.line(self.screen, GRID_COLOR, start_pos, end_pos, LINE_WIDTH)
        
        for y in range(self.grid_height + 1):
            start_pos = (PANEL_WIDTH, y * CELL_SIZE)
            end_pos = (PANEL_WIDTH + self.grid_width * CELL_SIZE, y * CELL_SIZE)
            pygame.draw.line(self.screen, GRID_COLOR, start_pos, end_pos, LINE_WIDTH)
    
    def draw_movement_range(self):
        """Highlight cells within movement range of selected character"""
        if self.selected_char and self.selected_char.remaining_movement > 0:
            char = self.selected_char
            movement_range = char.remaining_movement
            
            for x in range(self.grid_width):
                for y in range(self.grid_height):
                    # Calculate Chebyshev distance for diagonal movement
                    dx = abs(x - char.x)
                    dy = abs(y - char.y)
                    distance = max(dx, dy)  # Chebyshev distance
                    
                    # Check if this cell is within movement range
                    if distance > 0 and distance <= movement_range:
                        # Check if character would fit at this position
                        if x + char.size <= self.grid_width and y + char.size <= self.grid_height:
                            # Draw highlight on the top-left cell of where character would be
                            rect = pygame.Rect(
                                PANEL_WIDTH + x * CELL_SIZE + 2,
                                y * CELL_SIZE + 2,
                                CELL_SIZE - 4,
                                CELL_SIZE - 4
                            )
                            s = pygame.Surface((CELL_SIZE - 4, CELL_SIZE - 4))
                            s.set_alpha(50)
                            s.fill(MOVEMENT_HIGHLIGHT_COLOR)
                            self.screen.blit(s, rect)

    
    def draw_character(self, char):
        if char.x is not None and char.y is not None:
            for dx in range(char.size):
                for dy in range(char.size):
                    rect = pygame.Rect(
                        PANEL_WIDTH + (char.x + dx) * CELL_SIZE + 2,
                        (char.y + dy) * CELL_SIZE + 2,
                        CELL_SIZE - 4,
                        CELL_SIZE - 4
                    )
                    pygame.draw.rect(self.screen, char.color, rect)
                    
                    # Highlight selected character
                    if char == self.selected_char:
                        pygame.draw.rect(self.screen, SELECTED_COLOR, rect, 3)
                    else:
                        pygame.draw.rect(self.screen, GRID_COLOR, rect, 2)
    
    def draw_placing_preview(self):
        if self.placing_char:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_x >= PANEL_WIDTH and mouse_y < self.grid_height * CELL_SIZE:
                grid_x = (mouse_x - PANEL_WIDTH) // CELL_SIZE
                grid_y = mouse_y // CELL_SIZE
                
                for dx in range(self.placing_char.size):
                    for dy in range(self.placing_char.size):
                        if grid_x + dx < self.grid_width and grid_y + dy < self.grid_height:
                            rect = pygame.Rect(
                                PANEL_WIDTH + (grid_x + dx) * CELL_SIZE + 2,
                                (grid_y + dy) * CELL_SIZE + 2,
                                CELL_SIZE - 4,
                                CELL_SIZE - 4
                            )
                            s = pygame.Surface((CELL_SIZE - 4, CELL_SIZE - 4))
                            s.set_alpha(128)
                            s.fill(self.placing_char.color)
                            self.screen.blit(s, rect)
    
    def draw_bottom_panel(self):
        bottom_y = self.grid_height * CELL_SIZE
        pygame.draw.rect(self.screen, PANEL_COLOR, (0, bottom_y, self.window_width, BOTTOM_PANEL_HEIGHT))
        
        if self.selected_char:
            y_offset = bottom_y + 10
            text = self.small_font.render(f"Name: {self.selected_char.name}", True, TEXT_COLOR)
            self.screen.blit(text, (10, y_offset))
            y_offset += 25
            
            text = self.small_font.render(f"Class: {self.selected_char.char_class} | Race: {self.selected_char.race}", True, TEXT_COLOR)
            self.screen.blit(text, (10, y_offset))
            y_offset += 25
            
            text = self.small_font.render(
                f"Movement: {self.selected_char.remaining_movement}/{self.selected_char.speed} | "
                f"Actions: {self.selected_char.remaining_actions}/{self.selected_char.max_actions} | "
                f"Bonus: {self.selected_char.remaining_bonus_actions}/{self.selected_char.max_bonus_actions} | "
                f"Reactions: {self.selected_char.remaining_reactions}/{self.selected_char.max_reactions}",
                True, TEXT_COLOR
            )
            self.screen.blit(text, (10, y_offset))
            y_offset += 25
            
            text = self.small_font.render(
                f"STR:{self.selected_char.abilities['str']} DEX:{self.selected_char.abilities['dex']} "
                f"CON:{self.selected_char.abilities['con']} INT:{self.selected_char.abilities['int']} "
                f"WIS:{self.selected_char.abilities['wis']} CHA:{self.selected_char.abilities['cha']}",
                True, TEXT_COLOR
            )
            self.screen.blit(text, (10, y_offset))
            y_offset += 25
            
            text = self.small_font.render("Click on a highlighted cell to move", True, (150, 150, 150))
            self.screen.blit(text, (10, y_offset))
    
    def handle_grid_click(self, mouse_x, mouse_y):
        if mouse_x >= PANEL_WIDTH and mouse_y < self.grid_height * CELL_SIZE:
            grid_x = (mouse_x - PANEL_WIDTH) // CELL_SIZE
            grid_y = mouse_y // CELL_SIZE
            
            if self.placing_char:
                # Place new character
                if grid_x + self.placing_char.size <= self.grid_width and grid_y + self.placing_char.size <= self.grid_height:
                    self.placing_char.x = grid_x
                    self.placing_char.y = grid_y
                    self.characters.append(self.placing_char)
                    self.placing_char = None
            elif self.selected_char:
                # Try to move selected character
                if self.selected_char.can_move_to(grid_x, grid_y):
                    # Check if destination is valid (character fits)
                    if grid_x + self.selected_char.size <= self.grid_width and grid_y + self.selected_char.size <= self.grid_height:
                        self.selected_char.move_to(grid_x, grid_y)
                        print(f"{self.selected_char.name} moved to ({grid_x}, {grid_y})")
                else:
                    # Click outside movement range - try to select a character
                    clicked_char = None
                    for char in self.characters:
                        if char.x <= grid_x < char.x + char.size and char.y <= grid_y < char.y + char.size:
                            clicked_char = char
                            break
                    
                    if clicked_char:
                        self.selected_char = clicked_char
                        print(f"Selected {clicked_char.name}")
            else:
                # No character selected, try to select one
                for char in self.characters:
                    if char.x <= grid_x < char.x + char.size and char.y <= grid_y < char.y + char.size:
                        self.selected_char = char
                        print(f"Selected {char.name}")
                        break
    
    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    button_clicked = False
                    for btn in self.buttons:
                        if btn.handle_event(event):
                            button_clicked = True
                            break
                    
                    if not button_clicked:
                        self.handle_grid_click(*event.pos)
                elif event.type == pygame.MOUSEMOTION:
                    for btn in self.buttons:
                        btn.handle_event(event)
            
            # Draw everything
            self.screen.fill(BACKGROUND_COLOR)
            
            # Side panel
            pygame.draw.rect(self.screen, PANEL_COLOR, (0, 0, PANEL_WIDTH, self.grid_height * CELL_SIZE))
            for btn in self.buttons:
                btn.draw(self.screen, self.font)
            
            # Grid and movement range
            self.draw_grid()
            self.draw_movement_range()
            
            # Characters
            for char in self.characters:
                self.draw_character(char)
            self.draw_placing_preview()
            
            # Bottom panel
            self.draw_bottom_panel()
            
            pygame.display.flip()
            self.clock.tick(60)