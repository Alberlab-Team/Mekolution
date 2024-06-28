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
        super().__init__()
        self.path = path
        self.title("JSON Data Representation")
        self.geometry("800x600")
        
        # Read the JSON file
        self.data : dict
        self.read()

        # Create the main container
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)
        
        # Create a canvas
        self.canvas = tk.Canvas(container)
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        
        # Configure the canvas
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Bind the mouse wheel to the canvas for scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)  # For Linux
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)  # For Linux

        # Create another frame inside the canvas
        self.frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.frame, anchor="nw")
        

        # Add a button to update the JSON data
        update_button = ttk.Button(self, text="Update", command=self.display_json)
        update_button.pack(pady=10)

        self.running = True
        
        # Display JSON data
        self.display_json()
        self.update_scroll_region()

        # A little bit simple to understand no ?
        self.checkForStop()

    def checkForStop(self):
            if self.running:
                self.after(1000, self.checkForStop)
            else:
                print("data viewer singleton will be destroyed. Don't worry if you recive a Tcl_AcyncDelete log from there to 1~2 s")
                self.destroy()

    def update_scroll_region(self):
        self.canvas.update_idletasks()  # Ensure all widgets are properly managed
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas_height = self.canvas.winfo_height()  # Update canvas height

    def read(self):
        with open(self.path, 'r') as file:
            self.data = json.load(file)

    def display_json(self, indent=0):
        self.read()

        for widget in self.frame.winfo_children():
            widget.destroy()
        
        self._display_json_recursive(self.data)
        self.update_scroll_region()

    def _display_json_recursive(self, data, parent_frame=None, indent=0):
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
        self.update_scroll_region()

    def display_value(self, value, frame):
        if isinstance(value, dict) or isinstance(value, list):
            self._display_json_recursive(value, frame, indent=1)
        else:
            value_label = ttk.Label(frame, text=f"{value}")
            value_label.pack(anchor="w", padx=10)

    def _on_mousewheel(self, event):
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")


# Replace 'settings' with the actual path to your JSON file
if __name__ == "__main__":
    app = RepresentFileApp('settings.json')
    app.mainloop()