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
        
        self.buttons = [
            Button2D(10, 20, PANEL_WIDTH - 20, 40, "Add Character", self.add_character),
            Button2D(10, 70, PANEL_WIDTH - 20, 40, "Import Character", self.import_character),
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
            char.remaining_movement = char.speed
            self.placing_char = char
    
    def draw_grid(self):
        for x in range(self.grid_width + 1):
            start_pos = (PANEL_WIDTH + x * CELL_SIZE, 0)
            end_pos = (PANEL_WIDTH + x * CELL_SIZE, self.grid_height * CELL_SIZE)
            pygame.draw.line(self.screen, GRID_COLOR, start_pos, end_pos, LINE_WIDTH)
        
        for y in range(self.grid_height + 1):
            start_pos = (PANEL_WIDTH, y * CELL_SIZE)
            end_pos = (PANEL_WIDTH + self.grid_width * CELL_SIZE, y * CELL_SIZE)
            pygame.draw.line(self.screen, GRID_COLOR, start_pos, end_pos, LINE_WIDTH)
    
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
            
            text = self.small_font.render(f"Movement: {self.selected_char.remaining_movement}/{self.selected_char.speed}", True, TEXT_COLOR)
            self.screen.blit(text, (10, y_offset))
            y_offset += 25
            
            text = self.small_font.render(f"STR:{self.selected_char.abilities['str']} DEX:{self.selected_char.abilities['dex']} CON:{self.selected_char.abilities['con']} INT:{self.selected_char.abilities['int']} WIS:{self.selected_char.abilities['wis']} CHA:{self.selected_char.abilities['cha']}", True, TEXT_COLOR)
            self.screen.blit(text, (10, y_offset))
            y_offset += 25
            
            text = self.small_font.render("Use Arrow Keys or WASD to move", True, (150, 150, 150))
            self.screen.blit(text, (10, y_offset))
    
    def handle_grid_click(self, mouse_x, mouse_y):
        if mouse_x >= PANEL_WIDTH and mouse_y < self.grid_height * CELL_SIZE:
            grid_x = (mouse_x - PANEL_WIDTH) // CELL_SIZE
            grid_y = mouse_y // CELL_SIZE
            
            if self.placing_char:
                if grid_x + self.placing_char.size <= self.grid_width and grid_y + self.placing_char.size <= self.grid_height:
                    self.placing_char.x = grid_x
                    self.placing_char.y = grid_y
                    self.characters.append(self.placing_char)
                    self.placing_char = None
            else:
                self.selected_char = None
                for char in self.characters:
                    if char.x <= grid_x < char.x + char.size and char.y <= grid_y < char.y + char.size:
                        self.selected_char = char
                        break
    
    def handle_movement(self, event):
        if self.selected_char and self.selected_char.remaining_movement > 0:
            dx, dy = 0, 0
            if event.key in (pygame.K_UP, pygame.K_w):
                dy = -1
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                dy = 1
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                dx = -1
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                dx = 1
            
            if dx != 0 or dy != 0:
                new_x = self.selected_char.x + dx
                new_y = self.selected_char.y + dy
                
                if (0 <= new_x and new_x + self.selected_char.size <= self.grid_width and
                    0 <= new_y and new_y + self.selected_char.size <= self.grid_height):
                    self.selected_char.x = new_x
                    self.selected_char.y = new_y
                    self.selected_char.remaining_movement -= 1
    
    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    else:
                        self.handle_movement(event)
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
            
            # Grid and characters
            self.draw_grid()
            for char in self.characters:
                self.draw_character(char)
            self.draw_placing_preview()
            
            # Bottom panel
            self.draw_bottom_panel()
            
            pygame.display.flip()
            self.clock.tick(60)