from tkinter import Tk, Label, Button, Listbox, Scrollbar, VERTICAL, END
import os
from src.entities.character import Character, DATA_DIR

class CharacterImportDialog:
    def __init__(self):
        self.result = None
        self.root = Tk()
        self.root.title("Import Character")
        self.root.geometry("400x400")
        
        Label(self.root, text="Select a character to import:", font=('Arial', 12, 'bold')).pack(pady=10)
        
        scrollbar = Scrollbar(self.root, orient=VERTICAL)
        self.listbox = Listbox(self.root, yscrollcommand=scrollbar.set, width=50, height=15)
        scrollbar.config(command=self.listbox.yview)
        scrollbar.pack(side='right', fill='y')
        self.listbox.pack(pady=10, padx=10)
        
        for filename in Character.list_saved():
            self.listbox.insert(END, filename[:-5].replace('_', ' '))
        
        Button(self.root, text="Import", command=self.import_character, width=15, bg='#2196F3', fg='white').pack(pady=10)
        Button(self.root, text="Cancel", command=self.root.destroy, width=15).pack()
    
    def import_character(self):
        selection = self.listbox.curselection()
        if selection:
            filename = Character.list_saved()[selection[0]]
            self.result = Character.load(os.path.join(DATA_DIR, filename))
            self.root.destroy()
    
    def show(self):
        self.root.wait_window()
        return self.result