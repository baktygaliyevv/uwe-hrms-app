import tkinter as tk
from orm.table import Table

class AddTablePopup(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
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
    # вот тут нужен фикс с бд связанный 
    def save(self):
        id = self.number_var.get()
        capacity = self.capacity_var.get()
        self.app.hrms.add_table(Table(id, capacity))
        self.parent.refresh()
        self.destroy()
