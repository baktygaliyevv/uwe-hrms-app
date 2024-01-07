import tkinter as tk
from tkinter import ttk, messagebox

class AddOrderMenuItemPopup(tk.Toplevel):
    def __init__(self, parent, restaurant):
        tk.Toplevel.__init__(self, parent)
        self.title('Add menu item to order')
        self.parent = parent
        self.app = parent.app
        self.restaurant = restaurant

        self.menu_item_var = tk.StringVar()
        self.count_var = tk.IntVar()
        
        tk.Label(self, text='Menu item', anchor='w', font=self.app.base_font).grid(row=0, column=0, columnspan=2, sticky='ew')
        parent_menu_items = list(map(lambda m: m[0], self.parent.menu_items))
        self.menu_items = list(filter(lambda i: i[0] not in parent_menu_items, list(map(lambda mi: (mi, mi.name), self.app.hrms.menu_items))))
        menu_items_names = list(map(lambda mi: mi[1], self.menu_items))
        ttk.Combobox(self, values=menu_items_names, textvariable=self.menu_item_var, state='readonly').grid(row=1, column=0, columnspan=2, sticky='ew')

        tk.Label(self, text='Count', anchor='w', font=self.app.base_font).grid(row=2, column=0, sticky='ew')
        tk.Entry(self, textvariable=self.count_var).grid(row=2, column=1, sticky='ew')

        tk.Button(self, text='Add', command=self.save).grid(row=3, column=0, columnspan=2, sticky='ew')

    def save(self):
        menu_item = next(mi[0] for mi in self.menu_items if mi[1] == self.menu_item_var.get())
        unavailable_menu_items = list(map(lambda mi: mi[0], self.restaurant.get_unavailable_menu_items()))
        if menu_item in unavailable_menu_items:
            return messagebox.showerror('Not available', 'Selected item not available in this restaurant. Please try again later.')
        self.parent.menu_items.append((menu_item, self.count_var.get()))
        self.destroy()