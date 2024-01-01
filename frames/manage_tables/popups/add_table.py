import tkinter as tk
from orm.table import Table

class AddTablePopup(tk.Toplevel):
    def __init__(self, parent, restaurant):
        super().__init__(parent)
        self.title("Add Table")
        self.parent = parent
        self.app = parent.app
        self.restaurant = restaurant

        self.capacity_var = tk.IntVar()

        tk.Label(self, text="Restaurant", anchor='w').grid(row=0, column=0, columnspan=2, sticky='ew')
        restaurant_city = tk.StringVar()
        restaurant_city.set(self.restaurant.city)
        tk.Entry(self, textvariable=restaurant_city, state='disabled').grid(row=1, column=0, columnspan=2, sticky='ew')

        tk.Label(self, text="Capacity", anchor='w').grid(row=2, column=0, sticky='ew')
        tk.Entry(self, textvariable=self.capacity_var).grid(row=2, column=1, sticky='ew')

        tk.Button(self, text="Save", command=self.save).grid(row=3, column=0, columnspan=2, sticky='ew')

    def save(self):
        self.app.hrms.add_table(Table(
            self.app.hrms, 
            capacity=self.capacity_var.get(), 
            restaurant=self.restaurant
        ))
        self.parent.refresh()
        self.destroy()

