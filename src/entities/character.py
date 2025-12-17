import json
import os

DATA_DIR = "data/characters"
os.makedirs(DATA_DIR, exist_ok=True)

class Character:
    def __init__(self, name, char_class, race, size, speed, abilities, color):
        self.name = name
        self.char_class = char_class
        self.race = race
        self.size = size
        self.speed = speed
        self.abilities = abilities  # {str, dex, con, int, wis, cha}
        self.color = color
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
            "color": self.color
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
            data["color"]
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
    
    def reset_movement(self):
        self.remaining_movement = self.speed