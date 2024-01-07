import tkinter as tk
from frames.manage_bookings.manage_bookings import ManageBookingsFrame
from components.restaurant_selector import RestaurantSelectorComponent

class DashboardManagerFrame(tk.Frame):
    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent)
        self.app = app
    
    def render(self):
        if not self.app.user:
            return
        
        self.grid_columnconfigure(tuple(range(2)), weight=1)
        tk.Label(self, text=f"Hi there, {self.app.user.first_name} {self.app.user.last_name}! You are a manager", font=self.app.title_font).grid(row=0, column=0, sticky="w")
        tk.Button(self, text="≡", command=lambda: self.app.show_frame('MainFrame'), font=self.app.base_font, bg="blue", fg="white").grid(row=0, column=1, sticky='e')

        ManageBookingsFrame(self, self.app, show_back=False).grid(row=1, column=0, sticky='nsew')

        stats_frame = tk.Frame(self)
        stats_frame.grid(row=1, column=1, sticky='nsew')
        stats_title_frame = tk.Frame(stats_frame)
        stats_title_frame.pack()
        tk.Label(stats_title_frame, text='Stats for ', anchor='w', font=self.app.title_font).grid(row=0, column=0, sticky='ew')
        self.restaurant_dropdown = RestaurantSelectorComponent(stats_title_frame, self.app)
        self.restaurant_dropdown.bind('<<RestaurantSelected>>', self.refresh_stats)
        self.restaurant_dropdown.grid(row=0, column=1, sticky='ew')

        self.restaurants = tk.Label(stats_frame, text='Restaurants in system: ...', anchor='w', font=self.app.base_font)
        self.restaurants.pack()
        self.bookings = tk.Label(stats_frame, text='Active bookings: ...', anchor='w', font=self.app.base_font)
        self.bookings.pack()
        self.deliveries = tk.Label(stats_frame, text='Active deliveries: ...', anchor='w', font=self.app.base_font)
        self.deliveries.pack()
        self.menu_items = tk.Label(stats_frame, text='Available menu items: ...', anchor='w', font=self.app.base_font)
        self.menu_items.pack()
        self.orders = tk.Label(stats_frame, text='Active orders: ...', anchor='w', font=self.app.base_font)
        self.orders.pack()
        self.users = tk.Label(stats_frame, text='Users registered: ...', anchor='w', font=self.app.base_font)
        self.users.pack()

        self.refresh_stats()

    def refresh_stats(self):
        restaurant = self.restaurant_dropdown.get()
        self.restaurants.config(text=f'Restaurants in system: {len(self.app.hrms.restaurants)}')
        self.bookings.config(text=f'Active bookings: {len(restaurant.get_bookings())}')
        self.deliveries.config(text=f'Active deliveries: {len(restaurant.get_deliveries())}')
        self.menu_items.config(text=f'Available menu items: {len(self.app.hrms.menu_items)}')
        self.orders.config(text=f'Active orders: {len(restaurant.get_orders())}')
        self.users.config(text=f'Users registered: {len(self.app.hrms.users)}')