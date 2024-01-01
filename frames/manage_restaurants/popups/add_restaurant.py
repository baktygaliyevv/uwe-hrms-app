import tkinter as tk
from orm.restaurant import Restaurant

class AddRestaurantPopup(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.title("Add Restaurant")
        self.parent = parent
        self.app = parent.app

        self.city_var = tk.StringVar()

        tk.Label(self, text="City:").grid(row=0, column=0, padx=10, pady=5)
        tk.Entry(self, textvariable=self.city_var).grid(row=0, column=1, padx=10, pady=5)

        tk.Button(self, text="Save", command=self.save).grid(row=1, column=0, columnspan=2, pady=10)
        
    def save(self):
        city = self.city_var.get()
        self.app.hrms.add_restaurant(Restaurant(
            self.app.hrms,
            city=city
        ))
        self.parent.refresh()
        self.destroy()