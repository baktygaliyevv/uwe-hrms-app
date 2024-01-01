import tkinter as tk
from orm.table import Table

class AddTablePopup(tk.Toplevel):
    def __init__(self, parent, restaurant_id):
        super().__init__(parent)
        self.restaurant_id = restaurant_id
        self.title("Add Table")
        self.parent = parent
        self.app = parent.app

        self.number_var = tk.StringVar()
        self.capacity_var = tk.IntVar()

        tk.Label(self, text="Table #").grid(row=0, column=0, padx=10, pady=5)
        tk.Entry(self, textvariable=self.number_var).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self, text="Capacity").grid(row=1, column=0, padx=10, pady=5)
        tk.Entry(self, textvariable=self.capacity_var).grid(row=1, column=1, padx=10, pady=5)

        tk.Button(self, text="Save", command=self.save).grid(row=2, column=0, columnspan=2, pady=10)

    def save(self):
        table_number = self.number_var.get() 
        capacity = self.capacity_var.get()

        new_table = Table(id=table_number, capacity=capacity, restaurant_id=self.restaurant_id)
        self.app.hrms.add_table(new_table)
        self.parent.refresh()
        self.destroy()

