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

        ManageBookingsFrame(self, self.app).grid(row=1, column=0, sticky='nsew')

        stats_frame = tk.Frame(self)
        stats_frame.grid(row=1, column=1, sticky='nsew')
        stats_title_frame = tk.Frame(stats_frame)
        stats_title_frame.pack()
        tk.Label(stats_title_frame, text='Stats for ', anchor='w', font=self.app.title_font).grid(row=0, column=0, sticky='ew')
        self.restaurant_dropdown = RestaurantSelectorComponent(stats_title_frame, self.app)
        self.restaurant_dropdown.bind('<<RestaurantSelected>>', self.refresh_stats)
        self.restaurant_dropdown.grid(row=0, column=1, sticky='ew')

        tk.Label(stats_frame, text='Active bookings: 0', anchor='w', font=self.app.base_font).pack()
        tk.Label(stats_frame, text='Active deliveries: 0', anchor='w', font=self.app.base_font).pack()
        tk.Label(stats_frame, text='Active orders: 0', anchor='w', font=self.app.base_font).pack()

    def refresh_stats(self):
        pass