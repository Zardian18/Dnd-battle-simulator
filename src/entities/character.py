import json
import os

DATA_DIR = "data/characters"
os.makedirs(DATA_DIR, exist_ok=True)

class Character:
    def __init__(self, name, char_class, race, size, speed, abilities, color, actions=1, bonus_actions=1, reactions=1):
        self.name = name
        self.char_class = char_class
        self.race = race
        self.size = size
        self.speed = speed
        self.abilities = abilities  # {str, dex, con, int, wis, cha}
        self.color = color
        
        # Action economy
        self.max_actions = actions
        self.max_bonus_actions = bonus_actions
        self.max_reactions = reactions
        
        self.remaining_actions = actions
        self.remaining_bonus_actions = bonus_actions
        self.remaining_reactions = reactions
        
        self.x = None
        self.y = None
        self.remaining_movement = speed
    
    def to_dict(self):
        return {
            "name": self.name,
            "class": self.char_class,
            "race": self.race,
            "size": self.size,
            "speed": self.speed,
            "abilities": self.abilities,
            "color": self.color,
            "actions": self.max_actions,
            "bonus_actions": self.max_bonus_actions,
            "reactions": self.max_reactions
        }
    
    @staticmethod
    def from_dict(data):
        return Character(
            data["name"],
            data["class"],
            data["race"],
            data["size"],
            data["speed"],
            data["abilities"],
            data["color"],
            data.get("actions", 1),
            data.get("bonus_actions", 1),
            data.get("reactions", 1)
        )
    
    def save(self):
        filename = os.path.join(DATA_DIR, f"{self.name.replace(' ', '_')}.json")
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)
    
    @staticmethod
    def load(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        return Character.from_dict(data)
    
    @staticmethod
    def list_saved():
        if not os.path.exists(DATA_DIR):
            return []
        return [f for f in os.listdir(DATA_DIR) if f.endswith('.json')]
    
    def reset_turn(self):
        """Reset all resources for a new turn"""
        self.remaining_movement = self.speed
        self.remaining_actions = self.max_actions
        self.remaining_bonus_actions = self.max_bonus_actions
        self.remaining_reactions = self.max_reactions
    
    def can_move_to(self, target_x, target_y):
        """Check if character can move to target position based on remaining movement"""
        if self.x is None or self.y is None:
            return False
        
        # Calculate Chebyshev distance for diagonal movement
        dx = abs(target_x - self.x)
        dy = abs(target_y - self.y)
        distance = max(dx, dy)  # Chebyshev distance
        
        return distance <= self.remaining_movement

    def move_to(self, target_x, target_y):
        """Move character to target position and deduct movement"""
        if self.can_move_to(target_x, target_y):
            dx = abs(target_x - self.x)
            dy = abs(target_y - self.y)
            distance = max(dx, dy)  # Chebyshev distance
            
            self.x = target_x
            self.y = target_y
            self.remaining_movement -= distance
            return True
        return False