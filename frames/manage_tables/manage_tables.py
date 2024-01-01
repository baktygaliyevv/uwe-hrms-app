import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from components.table import TableComponent
from components.restaurant_selector import RestaurantSelectorComponent
from frames.manage_tables.popups.add_table import AddTablePopup

def split_tables(tables):
    if len(tables) > 6:
        return tables[:len(tables) // 2], tables[len(tables) // 2:]
    return tables, []

class ManageTablesFrame(tk.Frame):
    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent)
        self.app = app

        self.grid_columnconfigure(tuple(range(2)), weight=1)
        tk.Label(self, text="Tables", font=self.app.title_font).grid(row=0, column=0, sticky="w")

        self.restaurant_dropdown = RestaurantSelectorComponent(self)
        self.restaurant_dropdown.bind('<<RestaurantSelected>>', self.refresh)
        self.restaurant_dropdown.grid(row=1, column=0, sticky='ew')

        tk.Button(self, text="Add Table", command=self.add_table, font=self.app.base_font, bg="blue", fg="white").grid(row=0, column=1, sticky='e')

        data1, data2 = split_tables(self.restaurant_dropdown.get().get_tables())
        self.table1 = TableComponent(
            self,
            headings=['Table #', 'Capacity', 'Delete'],
            data=data1,
            get_row=self.get_row
        )
        self.table1.grid(row=2, column=0, sticky='nsew')
        self.table2 = TableComponent(
            self,
            headings=['Table #', 'Capacity', 'Delete'],
            data=data2,
            get_row=self.get_row
        )
        self.table2.grid(row=2, column=1, sticky='nsew')

    def refresh(self, _ = None):
        data1, data2 = split_tables(self.restaurant_dropdown.get().get_tables())
        self.table1.update_data(data1)
        self.table2.update_data(data2)

    def get_row(self, table, row, table_data):
        tk.Label(table, text=table_data.id, anchor='w', font=self.app.base_font).grid(row=row, column=0, sticky='ew')
        tk.Label(table, text=table_data.capacity, anchor='w', font=self.app.base_font).grid(row=row, column=1, sticky='ew')
        tk.Button(table, text='✖', command=lambda table_data=table_data: self.delete_table(table_data)).grid(row=row, column=2, sticky='ew')

    def add_table(self):
        restaurant = self.restaurant_dropdown.get()
        if restaurant is None:
            return messagebox.showerror("Error", "Please select a restaurant first.")
        popup = AddTablePopup(self, restaurant)  # Pass the selected restaurant ID to the popup
        self.wait_window(popup)

    def delete_table(self, table_data):
        action = messagebox.askquestion('Delete Table', f'Are you sure you want to delete table #{table_data.id}?', icon='warning')
        if action == 'yes':
            self.restaurant_dropdown.get().delete_table(table_data)
            self.refresh()
