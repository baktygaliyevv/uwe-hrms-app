import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from components.table import TableComponent
from frames.manage_tables.popups.add_table import AddTablePopup

class ManageTablesFrame(tk.Frame):
    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent)
        self.app = app

        self.grid_columnconfigure(1, weight=1)
        tk.Label(self, text="Tables", font=self.app.title_font).grid(row=0, column=0, sticky="w")

        self.restaurant_var = tk.StringVar(self)
        self.restaurant_dropdown = ttk.Combobox(self, textvariable=self.restaurant_var, state='readonly')
        self.restaurant_dropdown['values'] = [restaurant.city for restaurant in self.app.hrms.restaurants]
        self.restaurant_dropdown.bind('<<ComboboxSelected>>', self.on_restaurant_selected)
        self.restaurant_dropdown.grid(row=1, column=0, sticky='ew')

        tk.Button(self, text="Add Table", command=self.add_table, font=self.app.base_font, bg="blue", fg="white").grid(row=0, column=1, sticky='e')

#вот тут разделить на 2 таблицы
        self.table_component = TableComponent(
            self,
            headings=['Table #', 'Capacity', 'Delete'],
            data=self.app.hrms.tables,
            get_row=self.get_row
        )
        self.table_component.grid(row=2, column=0, columnspan=2, sticky='nsew')

# пофиксить, не работает
    def on_restaurant_selected(self, event=None):
        selected_restaurant_city = self.restaurant_var.get()
        selected_restaurant = next((r for r in self.app.hrms.restaurants if r.city == selected_restaurant_city), None)
        if selected_restaurant:
            self.refresh(selected_restaurant.__id)

    def get_row(self, table, row, table_data):
        tk.Label(table, text=table_data.number, anchor='w', font=self.app.base_font).grid(row=row, column=0, sticky='ew')
        tk.Label(table, text=table_data.capacity, anchor='w', font=self.app.base_font).grid(row=row, column=1, sticky='ew')
        tk.Button(table, text='✖', command=lambda table_data=table_data: self.delete_table(table_data)).grid(row=row, column=2, sticky='ew')

    def refresh(self, restaurant_id=None):
        if restaurant_id is not None:
            filtered_tables = [table for table in self.app.hrms.tables if table.restaurant_id == restaurant_id]
            self.table_component.update_data(filtered_tables)
        else:
            self.table_component.update_data([])

    def add_table(self):
        popup = AddTablePopup(self)
        self.wait_window(popup)

    def delete_table(self, table_data):
        action = messagebox.askquestion('Delete Table', f'Are you sure you want to delete table #{table_data.number}?', icon='warning')
        if action == 'yes':
            self.app.hrms.delete_table(table_data)
            self.refresh()
