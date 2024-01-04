import tkinter as tk
import customtkinter as CTk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Custom Tkinter Widgets")
        self.geometry("500x500")
        self.resizable(False, False)
        
        # Create a custom button 
        self.button =CTk.CTkButton(self, text="Custom Button", command=self.button_command)
        self.button.pack()

        # Create a custom label
        self.label = tk.Label(self, text="Custom Label")
        self.label.pack()

        # Create a custom entry
        self.entry = tk.Entry(self)
        self.entry.pack()

        # Create a custom text
        self.text = tk.Text(self)
        self.text.pack()

        # Create a custom checkbutton
        self.checkbutton = tk.Checkbutton(self, text="Custom Checkbutton")
        self.checkbutton.pack()

        # Create a custom radiobutton
        self.radiobutton = tk.Radiobutton(self, text="Custom Radiobutton")
        self.radiobutton.pack()

        # Create a custom listbox
        self.listbox = tk.Listbox(self)
        self.listbox.pack()

        # Create a custom scrollbar
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack()

        # Create a custom scale
        self.scale = tk.Scale(self)
        self.scale.pack()

        # Create a custom spinbox. A spinbox is a widget that allows the user to select a value from a range of values by clicking the up and down arrows.
        self.spinbox = tk.Spinbox(self)
        self.spinbox.pack()

        # Create a custom menu
        self.menu = tk.Menu(self)
        self.menu.add_command(label="Custom Menu")
        self.config(menu=self.menu)

        # Create a custom menubutton
        self.menubutton = tk.Menubutton(self, text="Custom Menubutton")
        self.menubutton.pack()

        # Create a custom message
        self.message = tk.Message(self, text="Custom Message")
        self.message.pack()

        # Create a custom frame
        self.frame = tk.Frame(self)
        self.frame.pack()

        # Create a custom canvas
        self.canvas = tk.Canvas(self)
        self.canvas.pack()

    def button_command(self):
        # Add your button command logic here
        pass

# Create an instance of the App class
app = App()

# Start the Tkinter event loop
app.mainloop()

        