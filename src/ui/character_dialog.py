from tkinter import Tk, Toplevel, Label, Entry, Button, StringVar, colorchooser, Frame
from src.entities.character import Character

class CharacterCreationDialog:
    def __init__(self):
        self.result = None
        self.root = Tk()
        self.root.title("Create Character")
        self.root.geometry("400x450")
        
        self.name_var = StringVar()
        self.class_var = StringVar()
        self.race_var = StringVar()
        self.size_var = StringVar()
        self.speed_var = StringVar()
        
        self.actions_var = StringVar(value="1")
        self.bonus_actions_var = StringVar(value="1")
        self.reactions_var = StringVar(value="1")
        
        self.str_var = StringVar()
        self.dex_var = StringVar()
        self.con_var = StringVar()
        self.int_var = StringVar()
        self.wis_var = StringVar()
        self.cha_var = StringVar()
        
        self.selected_color = (255, 0, 0)
        
        self.current_window = None
        self.show_page1()
    
    def show_page1(self):
        if self.current_window:
            self.current_window.destroy()
        
        self.current_window = Frame(self.root)
        self.current_window.pack(fill='both', expand=True, padx=20, pady=20)
        
        Label(self.current_window, text="Basic Information", font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        
        Label(self.current_window, text="Name:").grid(row=1, column=0, pady=5, sticky='w')
        Entry(self.current_window, textvariable=self.name_var, width=30).grid(row=1, column=1, pady=5)
        
        Label(self.current_window, text="Class:").grid(row=2, column=0, pady=5, sticky='w')
        Entry(self.current_window, textvariable=self.class_var, width=30).grid(row=2, column=1, pady=5)
        
        Label(self.current_window, text="Race:").grid(row=3, column=0, pady=5, sticky='w')
        Entry(self.current_window, textvariable=self.race_var, width=30).grid(row=3, column=1, pady=5)
        
        Label(self.current_window, text="Size (1-5):").grid(row=4, column=0, pady=5, sticky='w')
        Entry(self.current_window, textvariable=self.size_var, width=30).grid(row=4, column=1, pady=5)
        
        Label(self.current_window, text="Speed:").grid(row=5, column=0, pady=5, sticky='w')
        Entry(self.current_window, textvariable=self.speed_var, width=30).grid(row=5, column=1, pady=5)
        
        Label(self.current_window, text="Actions:").grid(row=6, column=0, pady=5, sticky='w')
        Entry(self.current_window, textvariable=self.actions_var, width=30).grid(row=6, column=1, pady=5)
        
        Label(self.current_window, text="Bonus Actions:").grid(row=7, column=0, pady=5, sticky='w')
        Entry(self.current_window, textvariable=self.bonus_actions_var, width=30).grid(row=7, column=1, pady=5)
        
        Label(self.current_window, text="Reactions:").grid(row=8, column=0, pady=5, sticky='w')
        Entry(self.current_window, textvariable=self.reactions_var, width=30).grid(row=8, column=1, pady=5)
        
        Button(self.current_window, text="Next", command=self.show_page2, width=15).grid(row=9, column=1, pady=20)
    
    def show_page2(self):
        try:
            if not self.name_var.get():
                return
            size = int(self.size_var.get())
            speed = int(self.speed_var.get())
            actions = int(self.actions_var.get())
            bonus_actions = int(self.bonus_actions_var.get())
            reactions = int(self.reactions_var.get())
            
            if size < 1 or size > 5:
                return
            if speed < 0 or actions < 0 or bonus_actions < 0 or reactions < 0:
                return
        except ValueError:
            return
        
        if self.current_window:
            self.current_window.destroy()
        
        self.current_window = Frame(self.root)
        self.current_window.pack(fill='both', expand=True, padx=20, pady=20)
        
        Label(self.current_window, text="Ability Scores", font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        
        Label(self.current_window, text="Strength:").grid(row=1, column=0, pady=5, sticky='w')
        Entry(self.current_window, textvariable=self.str_var, width=30).grid(row=1, column=1, pady=5)
        
        Label(self.current_window, text="Dexterity:").grid(row=2, column=0, pady=5, sticky='w')
        Entry(self.current_window, textvariable=self.dex_var, width=30).grid(row=2, column=1, pady=5)
        
        Label(self.current_window, text="Constitution:").grid(row=3, column=0, pady=5, sticky='w')
        Entry(self.current_window, textvariable=self.con_var, width=30).grid(row=3, column=1, pady=5)
        
        Label(self.current_window, text="Intelligence:").grid(row=4, column=0, pady=5, sticky='w')
        Entry(self.current_window, textvariable=self.int_var, width=30).grid(row=4, column=1, pady=5)
        
        Label(self.current_window, text="Wisdom:").grid(row=5, column=0, pady=5, sticky='w')
        Entry(self.current_window, textvariable=self.wis_var, width=30).grid(row=5, column=1, pady=5)
        
        Label(self.current_window, text="Charisma:").grid(row=6, column=0, pady=5, sticky='w')
        Entry(self.current_window, textvariable=self.cha_var, width=30).grid(row=6, column=1, pady=5)
        
        Button(self.current_window, text="Back", command=self.show_page1, width=15).grid(row=7, column=0, pady=20)
        Button(self.current_window, text="Next", command=self.show_page3, width=15).grid(row=7, column=1, pady=20)
    
    def show_page3(self):
        try:
            str_val = int(self.str_var.get())
            dex_val = int(self.dex_var.get())
            con_val = int(self.con_var.get())
            int_val = int(self.int_var.get())
            wis_val = int(self.wis_var.get())
            cha_val = int(self.cha_var.get())
        except ValueError:
            return
        
        if self.current_window:
            self.current_window.destroy()
        
        self.current_window = Frame(self.root)
        self.current_window.pack(fill='both', expand=True, padx=20, pady=20)
        
        Label(self.current_window, text="Choose Color", font=('Arial', 14, 'bold')).pack(pady=20)
        
        Label(self.current_window, text="Select character color:").pack(pady=10)
        
        self.color_preview = Label(self.current_window, text="     ", bg='#ff0000', width=15, height=3)
        self.color_preview.pack(pady=10)
        
        Button(self.current_window, text="Choose Color", command=self.choose_color, width=20).pack(pady=10)
        
        btn_frame = Frame(self.current_window)
        btn_frame.pack(pady=20)
        Button(btn_frame, text="Back", command=self.show_page2, width=15).pack(side='left', padx=5)
        Button(btn_frame, text="Save Character", command=self.create_character, width=15, bg='#4CAF50', fg='white').pack(side='left', padx=5)
    
    def choose_color(self):
        color = colorchooser.askcolor(title="Choose character color")
        if color[0]:
            self.selected_color = tuple(int(c) for c in color[0])
            self.color_preview.config(bg=color[1])
    
    def create_character(self):
        abilities = {
            "str": int(self.str_var.get()),
            "dex": int(self.dex_var.get()),
            "con": int(self.con_var.get()),
            "int": int(self.int_var.get()),
            "wis": int(self.wis_var.get()),
            "cha": int(self.cha_var.get())
        }
        
        self.result = Character(
            self.name_var.get(),
            self.class_var.get(),
            self.race_var.get(),
            int(self.size_var.get()),
            int(self.speed_var.get()),
            abilities,
            self.selected_color,
            int(self.actions_var.get()),
            int(self.bonus_actions_var.get()),
            int(self.reactions_var.get())
        )
        
        self.result.save()
        self.root.destroy()
    
    def show(self):
        self.root.wait_window()
        return self.result