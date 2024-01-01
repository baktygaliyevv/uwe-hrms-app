import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from components.table import TableComponent
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

        self.restaurant_var = tk.StringVar(self)
        self.restaurant_dropdown = ttk.Combobox(self, textvariable=self.restaurant_var, state='readonly')
        self.restaurant_dropdown['values'] = [restaurant.city for restaurant in self.app.hrms.restaurants]

        self.restaurant_dropdown.bind('<<ComboboxSelected>>', self.on_restaurant_selected)
        self.restaurant_dropdown.grid(row=1, column=0, sticky='ew')

        tk.Button(self, text="Add Table", command=self.add_table, font=self.app.base_font, bg="blue", fg="white").grid(row=0, column=1, sticky='e')

        data1, data2 = split_tables(app.hrms.tables)
        self.table1 = TableComponent(
            self,
            headings=['Table #', 'Capacity', 'Delete'],
            data=data1,
            get_row=self.get_row
        )
        self.table1.grid(row=2, column=0, sticky='nsew')
        if len(data2):
            self.table2 = TableComponent(
                self,
                headings=['Table #', 'Capacity', 'Delete'],
            data=data2,
            get_row=self.get_row
            )
            self.table2.grid(row=2, column=1, sticky='nsew')
        
        default_city = next((restaurant.city for restaurant in self.app.hrms.restaurants if restaurant.id == 1), None)
        if default_city:
            self.restaurant_var.set(default_city)
            self.on_restaurant_selected()

    def on_restaurant_selected(self, event=None):
        selected_restaurant_city = self.restaurant_var.get()
        selected_restaurant = next((r for r in self.app.hrms.restaurants if r.city == selected_restaurant_city), None)
        if selected_restaurant:
            self.selected_restaurant_id = selected_restaurant.id  
            self.refresh(selected_restaurant.id)

    def refresh(self, restaurant_id=None):
        self.table1.update_data([]) 
        self.table2.update_data([]) if hasattr(self, 'table2') else None
        self.app.hrms.reload_tables()
        if restaurant_id is not None:
            filtered_tables = [table for table in self.app.hrms.tables if table.restaurant_id == restaurant_id]
            data1, data2 = split_tables(filtered_tables)
            self.table1.update_data(data1)
            if len(data2):
                if not hasattr(self, 'table2'):
                    self.table2 = TableComponent(self, headings=['Table #', 'Capacity', 'Delete'], data=data2, get_row=self.get_row)
                    self.table2.grid(row=2, column=1, sticky='ew')
                else:
                    self.table2.update_data(data2)

    def add_table(self):
        if self.selected_restaurant_id is None:
            messagebox.showerror("Error", "Please select a restaurant first.")
            return
        popup = AddTablePopup(self, self.selected_restaurant_id)  # Pass the selected restaurant ID to the popup
        self.wait_window(popup)
        self.refresh(self.selected_restaurant_id)

    def get_row(self, table, row, table_data):
        tk.Label(table, text=table_data.id, anchor='w', font=self.app.base_font).grid(row=row, column=0, sticky='ew')
        tk.Label(table, text=table_data.capacity, anchor='w', font=self.app.base_font).grid(row=row, column=1, sticky='ew')
        tk.Button(table, text='✖', command=lambda table_data=table_data: self.delete_table(table_data)).grid(row=row, column=2, sticky='ew')

    def delete_table(self, table_data):
        action = messagebox.askquestion('Delete Table', f'Are you sure you want to delete table #{table_data.id}?', icon='warning')
        if action == 'yes':
            self.app.hrms.delete_table(table_data)
            self.refresh(self.selected_restaurant_id)
