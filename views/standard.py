import tkinter as tk
from tkinter import font

class StandardWindow(tk.Tk):
    def __init__(self, title="Application", window_size="800x600"):
        super().__init__()
        
        self.title(title)
        self.geometry(window_size)

        self.standard_font = font.Font(size=14)
        self.button_color = '#2F9AB1'
        self.entry_font = font.Font(size=14)

        self.configure(background='#F3F3F3')
        self.create_standard_widgets()

# class StandardStyling:
#     standard_font = font.Font(size=14)
#     button_color = '#2F9AB1'
#     background = '#FFFFFF'

# # Inherit from tk.Tk when actually creating a window
# class StandardWindow(tk.Tk):
#     def __init__(self, title="Application", window_size="800x600"):
#         super().__init__()
        
#         self.title(title)
#         self.geometry(window_size)

#         self.configure(background=StandardStyling.background)
#         self.create_standard_widgets()

    def create_standard_widgets(self):
        # вот тут можно напихать дефолтный дизайн который будем юзать везде, типо хедера
        pass

    def on_close(self):
        self.destroy()
