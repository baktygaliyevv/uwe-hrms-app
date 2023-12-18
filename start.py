from dotenv import load_dotenv
load_dotenv()

import sys
from pathlib import Path
import tkinter as tk
import tkinter.font as font
from orm.base import HRMS

from frames.login import LoginFrame

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        tk.Tk.geometry(self, '800x600')
        container.pack(side='top', fill='both', expand = True)     
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.base_font = font.Font(size=14)
        self.entry_font = font.Font(size=14)
        self.background_color = '#F3F3F3'
        self.button_color = '#2F9AB1'

        self.hrms = HRMS()
        self.user = None

        self.frames = {}

        for F in (LoginFrame,):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")

        self.show_frame('LoginFrame')

    def show_frame(self, cont):
        frame = self.frames[cont]    
        frame.tkraise()

sys.path.append(str(Path(__file__).resolve()))
app = MainWindow()
app.mainloop()