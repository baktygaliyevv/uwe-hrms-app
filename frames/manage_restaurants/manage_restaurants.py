# @d2-zhmurenko @a2-kaluhin
import tkinter as tk
from tkinter import messagebox
from components.table import TableComponent
from frames.manage_restaurants.popups.add_restaurant import AddRestaurantPopup

def split_restaurants(restaurants):
    if(len(restaurants) > 6):
        return restaurants[:len(restaurants) // 2], restaurants[len(restaurants) // 2:]
    return restaurants, [] 

class ManageRestaurantsFrame(tk.Frame):
    __allowed_roles__ = ['admin']

    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent)
        self.app = app

        self.grid_columnconfigure(tuple(range(2)), weight=1)
        tk.Label(self, text="Restaurants", font=self.app.title_font).grid(row=0, column=0, sticky="w")
        tk.Button(self, text="Add Restaurant", command=self.add_restaurant, font=self.app.base_font, bg="blue", fg="white").grid(row=0, column=1, sticky='e')

        data1, data2 = split_restaurants(app.hrms.restaurants)
        self.table1 = TableComponent(
            self,
            headings=['Location', 'Delete'],
            data=data1,
            get_row=self.get_row
        )
        self.table1.grid(row=1, column=0, sticky='ew')
        if len(data2):
            self.table2 = TableComponent(
                self,
                headings=['Location', 'Delete'],
                data=data2,
                get_row=self.get_row
            )
            self.table2.grid(row=1, column=1, sticky='ew')
        back_to_main_screen_button = tk.Button(self, text="Back to main", command=lambda: self.app.show_frame('MainFrame'))
        back_to_main_screen_button.grid(row=10, column=0, sticky="sw")
        
    def get_row(self, table, row, restaurant):
        tk.Label(table, text=restaurant.city, anchor='w', font=self.app.base_font).grid(row=row, column=0, sticky='ew')
        tk.Button(table, text='✖', command=lambda restaurant=restaurant: self.delete_restaurant(restaurant)).grid(row=row, column=1, sticky='ew')

    def refresh(self):
        data1, data2 = split_restaurants(self.app.hrms.restaurants)
        self.table1.update_data(data1)
        if self.table2:
            self.table2.update_data(data2)

    def add_restaurant(self):
        popup = AddRestaurantPopup(self)
        self.wait_window(popup)

    def delete_restaurant(self, restaurant):
        action = messagebox.askquestion('Delete restaurant', f'Are you sure you want to delete "{restaurant.city}"?', icon='warning')
        if action == 'yes':
            self.app.hrms.delete_restaurant(restaurant)
            self.refresh()