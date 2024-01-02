import tkinter as tk
from tkinter import ttk

class RestaurantSelectorComponent(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.app = parent.app

        self.dropdown = ttk.Combobox(self, values=[restaurant.city for restaurant in self.app.hrms.restaurants])
        self.dropdown.set(self.app.hrms.restaurants[0].city)
        self.dropdown.bind('<<ComboboxSelected>>', lambda e: self.event_generate('<<RestaurantSelected>>'))
        self.dropdown.pack()

    def get(self):
        selected_city = self.dropdown.get()
        return self.app.hrms.get_restaurant(city=selected_city)