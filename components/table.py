import tkinter as tk
from tkinter import ttk

class TableComponent(tk.Frame):
    '''get_row(table_frame, row, obj)'''
    def __init__(self, parent, headings, data, get_row):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.headings = headings
        self.get_row = get_row

        self.grid_columnconfigure(tuple(range(len(headings))), weight=1)

        self.update_data(data)

    def update_data(self, data):
        for widget in self.winfo_children():
            widget.destroy()

        for column, heading in enumerate(self.headings):
            tk.Label(self, text=heading, anchor="w", font=self.parent.app.base_font_bold).grid(row=0, column=column, sticky="ew")

        for row, obj in enumerate(data):
            self.get_row(self, row + 1, obj)

