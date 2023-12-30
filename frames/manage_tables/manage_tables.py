import tkinter as tk
from tkinter import messagebox
from components.table import TableComponent
from frames.manage_tables.popups.add_edit_table import AddTablePopup

class ManageTablesFrame(tk.Frame):
    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent)
        self.app = app

        self.grid_columnconfigure(1, weight=1)
        tk.Label(self, text="Tables", font=self.app.title_font).grid(row=0, column=0, sticky="w")
        tk.Button(self, text="Add Table", command=self.add_table, font=self.app.base_font, bg="blue", fg="white").grid(row=0, column=1, sticky='e')

        self.table_component = TableComponent(
            self,
            headings=['Table #', 'Capacity', 'Delete'],
            data=self.app.hrms.tables,
            get_row=self.get_row
        )
        self.table_component.grid(row=1, column=0, columnspan=2, sticky='nsew')

    def get_row(self, table, row, table_data):
        tk.Label(table, text=table_data.number, anchor='w', font=self.app.base_font).grid(row=row, column=0, sticky='ew')
        tk.Label(table, text=table_data.capacity, anchor='w', font=self.app.base_font).grid(row=row, column=1, sticky='ew')
        tk.Button(table, text='✖', command=lambda table_data=table_data: self.delete_table(table_data)).grid(row=row, column=2, sticky='ew')

    def refresh(self):
        self.table_component.update_data(self.app.hrms.tables)

    def add_table(self):
        popup = AddTablePopup(self)
        self.wait_window(popup)

    def delete_table(self, table_data):
        action = messagebox.askquestion('Delete Table', f'Are you sure you want to delete table #{table_data.number}?', icon='warning')
        if action == 'yes':
            self.app.hrms.delete_table(table_data)
            self.refresh()
