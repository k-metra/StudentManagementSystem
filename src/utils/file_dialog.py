import tkinter as tk
from tkinter import filedialog

def select_file(filetypes=(("Excel Files", "*.xlsx"), ("All Files", "*.*"))) -> str | None:
    root = tk.Tk()
    root.withdraw() # Hide the root tkinter window
    root.attributes("-topmost", True) # Bring the dialog to the front

    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=filetypes
    )

    root.destroy()

    return file_path