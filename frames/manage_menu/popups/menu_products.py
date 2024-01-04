import tkinter as tk
from orm.menu_item import MenuItem
from components.table import TableComponent

class MenuProductsPopup(tk.Toplevel):
    def __init__(self, parent, menu_item: MenuItem):
        tk.Toplevel.__init__(self, parent)
        self.title(f'{menu_item.name}: products')
        self.app = parent.app

        TableComponent(
            self, 
            headings=['Name', 'Vegan', 'Vegetarian', 'Gluten Free'],
            data=menu_item.get_products(),
            get_row=self.get_row
        ).pack()

    def get_row(self, table, row, product):
        tk.Label(table, text=product.name, anchor='w', font=self.app.base_font).grid(row=row, column=0, sticky='ew')
        tk.Label(table, text='Yes' if product.vegan else 'No', anchor='w', font=self.app.base_font).grid(row=row, column=1, sticky='ew')
        tk.Label(table, text='Yes' if product.vegetarian else 'No', anchor='w', font=self.app.base_font).grid(row=row, column=2, sticky='ew')
        tk.Label(table, text='Yes' if product.gluten_free else 'No', anchor='w', font=self.app.base_font).grid(row=row, column=3, sticky='ew')