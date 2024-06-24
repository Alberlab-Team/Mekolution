import json
import tkinter as tk
from tkinter import ttk

class RepresentFileApp(tk.Tk):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RepresentFileApp, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, path:str):
        self.PATH = path
        super().__init__()
        self.title("JSON Data Representation")
        self.geometry("800x600")
        
        # Read the JSON file
        self.read()

        # Create the main container
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)
        
        # Create a canvas
        canvas = tk.Canvas(container)
        canvas.pack(side="left", fill="both", expand=True)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        
        # Configure the canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # Create another frame inside the canvas
        self.frame = ttk.Frame(canvas)
        canvas.create_window((0,0), window=self.frame, anchor="nw")
        
        # Display JSON data
        self.display_json(self.data)

    def read(self):
        with open(self.PATH, 'r') as file:
            self.data = json.load(file)

    def display_json(self, data, parent_frame=None, indent=0):
        if parent_frame is None:
            parent_frame = self.frame
        
        if isinstance(data, dict):
            for key, value in data.items():
                self.create_collapsible_section(key, value, parent_frame, indent)
        elif isinstance(data, list):
            for idx, item in enumerate(data):
                self.create_collapsible_section(f"Item {idx}", item, parent_frame, indent)

    def create_collapsible_section(self, key, value, parent_frame, indent):
        section_frame = ttk.Frame(parent_frame)
        section_frame.pack(fill="x", pady=5, padx=indent*20)
        
        # Determine button color based on value type
        if isinstance(value, (dict, list)):
            toggle_button = tk.Button(section_frame, text=f"{key}", command=lambda: self.toggle_section(detail_frame), bg='red')
        else:
            toggle_button = tk.Button(section_frame, text=f"{key} : {value}", bg='blue')
        
        # Create a button to toggle the section
        
        toggle_button.pack(fill="x")
        
        # Create a frame for the details
        detail_frame = ttk.Frame(section_frame)
        detail_frame.pack(fill="x", padx=20)
        
        # Display the value in the detail frame
        self.display_value(value, detail_frame)

        detail_frame.pack_forget()  # Start with the details hidden

    def toggle_section(self, frame):
        if frame.winfo_viewable():
            frame.pack_forget()
        else:
            frame.pack(fill="x")

    def display_value(self, value, frame):
        if isinstance(value, dict) or isinstance(value, list):
            self.display_json(value, frame, indent=1)
        else:
            value_label = ttk.Label(frame, text=f"{value}")
            value_label.pack(anchor="w", padx=10)

"""
# Replace 'settings' with the actual path to your JSON file
app = RepresentFileApp('settings.json')
app.mainloop()
"""