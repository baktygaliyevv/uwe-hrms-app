# @d2-zhmurenko
import tkinter as tk
from orm.menu_category import MenuCategory

class AddMenuCategoryPopup(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.title("Add menu category")
        self.parent = parent
        self.app = parent.app

        self.category_var = tk.StringVar()

        tk.Label(self, text='Category', anchor='w', font=self.app.base_font).grid(row=0, column=0, sticky='ew')
        tk.Entry(self, textvariable=self.category_var).grid(row=1, column=0, sticky='ew')

        tk.Button(self, text='Save', command=self.save).grid(row=2, column=0, sticky='ew')

    def save(self):
        self.app.hrms.add_menu_category(MenuCategory(
            self.app.hrms,
            name=self.category_var.get()
        ))
        self.parent.refresh()
        self.destroy()