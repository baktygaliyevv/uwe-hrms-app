import tkinter as tk
from tkinter import ttk, messagebox
from components.table import TableComponent
from components.restaurant_selector import RestaurantSelectorComponent

class ManageRestaurantProductsFrame(tk.Frame):
    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent)
        self.app = app

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        title_frame = tk.Frame(self)
        tk.Label(title_frame, text="Manage Storage at ", font=self.app.title_font).grid(row=0, column=0, sticky="w")
        self.restaurant_selector = RestaurantSelectorComponent(title_frame, app)
        self.restaurant_selector.bind('<<RestaurantSelected>>', self.refresh)
        self.restaurant_selector.grid(row=0, column=1, sticky='ew')
        title_frame.grid(row=0, columnspan=2, sticky='ew')

        # Initialize tables for products and unavailable items
        self.product_count_table = TableComponent(
            self, 
            headings=['Product', 'Count', 'Actions'], 
            data=[], 
            get_row=self.get_product_count_row)
        
        self.product_count_table.grid(row=1, column=0, sticky='nsew')

        self.unavailable_items_table = TableComponent(
            self, 
            headings=['Item', 'Reason'], 
            data=[], 
            get_row=self.get_unavailable_items_row)
        
        self.unavailable_items_table.grid(row=1, column=1, sticky='nsew')

        self.refresh() 

    def get_product_count_row(self, table, row, product):
        tk.Label(table, text=product['name'], anchor='w', font=self.app.base_font).grid(row=row, column=0, sticky='ew')
        tk.Label(table, text=str(product['count']), anchor='e', font=self.app.base_font).grid(row=row, column=1, sticky='ew')
        
        actions_frame = tk.Frame(table)
        actions_frame.grid(row=row, column=2, sticky='ew')
        tk.Button(actions_frame, text='+', command=lambda: self.increment_count(product)).grid(row=0, column=0, sticky='ew')
        tk.Button(actions_frame, text='-', command=lambda: self.decrement_count(product), state='normal' if product['count'] > 0 else 'disabled').grid(row=0, column=1, sticky='ew')

    def get_unavailable_items_row(self, table, row, item):
        tk.Label(table, text=item['name'], anchor='w', font=self.app.base_font).grid(row=row, column=0, sticky='ew')
        tk.Label(table, text=item['reason'], anchor='w', font=self.app.base_font).grid(row=row, column=1, sticky='ew')

    def on_restaurant_selected(self, event=None):
        self.refresh()

    def refresh(self, event=None):
            restaurant = self.restaurant_selector.get()
            if restaurant:
                self.product_count_table.update_data(restaurant.get_products())
                self.unavailable_items_table.update_data(restaurant.get_unavailable_items())

    def increment_count(self, product):
        new_count = product['count'] + 1
        self.app.hrms.update_product_count(product['id'], new_count)
        self.refresh()

    def decrement_count(self, product):
        new_count = max(product['count'] - 1, 0)
        self.app.hrms.update_product_count(product['id'], new_count)
        self.refresh()
