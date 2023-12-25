import tkinter as tk
from tkinter import ttk

class TableComponent(tk.Frame):
    def __init__(self, parent, headings, data, action_callbacks, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.headings = headings
        self.data = data
        self.action_callbacks = action_callbacks
        
        for col in range(len(headings)):
            self.grid_columnconfigure(col, weight=1)

        self.create_headers()
        self.populate_data()

    def create_headers(self):
        for col, heading in enumerate(self.headings):
            tk.Label(self, text=heading, anchor="center", font=self.master.app.base_font_bold).grid(row=0, column=col, sticky="ew")

    def populate_data(self):
        for row, item in enumerate(self.data, start=1):
            actions_frame = tk.Frame(self)
            actions_frame.grid(row=row, column=len(self.headings)-2, sticky='nsew', columnspan=2)
            actions_frame.grid_columnconfigure(tuple(range(2)), weight=1)
            tk.Button(actions_frame, text='✎', command=lambda item=item: self.action_callbacks['edit'](item)).grid(row=0, column=0, sticky='ew')
            tk.Button(actions_frame, text='✖', command=lambda item=item: self.action_callbacks['delete'](item)).grid(row=0, column=1, sticky='ew')

    def refresh_data(self, new_data):
        for widget in self.winfo_children():
            widget.destroy()
        self.data = new_data
        self.create_headers()
        self.populate_data()


ROLE_OPTIONS = ['admin', 'manager', 'chef', 'staff', 'courier', 'client']
