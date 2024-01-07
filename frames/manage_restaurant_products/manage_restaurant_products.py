import tkinter as tk
from tkinter import ttk, messagebox
from components.table import TableComponent
from components.restaurant_selector import RestaurantSelectorComponent

class ManageRestaurantProductsFrame(tk.Frame):
    __allowed_roles__ = ['admin', 'manager', 'chef']

    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent)
        self.app = app

        self.grid_columnconfigure(tuple(range(2)), weight=1)

        title_frame = tk.Frame(self)
        tk.Label(title_frame, text="Storage at ", font=self.app.title_font).grid(row=0, column=0, sticky="w")

        self.restaurant_selector = RestaurantSelectorComponent(title_frame, app)
        self.restaurant_selector.bind('<<RestaurantSelected>>', lambda _: self.refresh())
        self.restaurant_selector.grid(row=0, column=1, sticky='ew')
        title_frame.grid(row=0, column=0, columnspan=2, sticky='ew')

        self.product_count_table = TableComponent(
            self, 
            headings=['Product', 'Count', 'Actions'], 
            data=[], 
            get_row=self.get_product_count_row
        )
        self.product_count_table.grid(row=1, column=0, sticky='nsew')

        self.unavailable_items_table = TableComponent(
            self, 
            headings=['Item', 'Out of stock'],
            data=[], 
            get_row=self.get_unavailable_items_row
        )
        self.unavailable_items_table.grid(row=1, column=1, sticky='nsew')
        tk.Button(self, text="Back to main", command=lambda: self.app.show_frame('MainFrame')).grid(row=10, column=0, sticky="sw")
        self.refresh() 

    def get_product_count_row(self, table, row, product_count):
        product, count = product_count

        tk.Label(table, text=product.name, anchor='w', font=self.app.base_font).grid(row=row, column=0, sticky='ew')
        count_label = tk.Label(table, text=str(count), anchor='e', font=self.app.base_font)
        count_label.grid(row=row, column=1, sticky='ew')
 
        actions_frame = tk.Frame(table)
        increment_button = tk.Button(
            actions_frame,
            text='+',
            command=lambda product_count=product_count: self.increment_count(product_count)
        )
        increment_button.grid(row=0, column=0, sticky='ew')
        
        decrement_button = tk.Button(
            actions_frame,
            text='-',
            state='normal' if count > 0 else 'disabled'
        )
        decrement_button.config(
            command=lambda product_count=product_count: self.decrement_count(product_count),
        )
        decrement_button.grid(row=0, column=1, sticky='ew')
    
        actions_frame.grid(row=row, column=2, sticky='ew')

    def get_unavailable_items_row(self, table, row, item):
        menu_item, products = item
        tk.Label(table, text=menu_item.name, anchor='w', font=self.app.base_font).grid(row=row, column=0, sticky='ew')
        tk.Label(table, text=' '.join(list(map(lambda p: p.name, products))), anchor='w', font=self.app.base_font).grid(row=row, column=1, sticky='ew')

    def refresh(self, event=None):
        restaurant = self.restaurant_selector.get()
        if restaurant:
            self.product_count_table.update_data(restaurant.get_products())
            self.unavailable_items_table.update_data(restaurant.get_unavailable_menu_items())

    def increment_count(self, product_count):
        product, count = product_count
        self.restaurant_selector.get().update_product_count(product, count + 1)
        self.refresh()

    def decrement_count(self, product_count):
        product, count = product_count
        self.restaurant_selector.get().update_product_count(product, count - 1)
        self.refresh()