import tkinter as tk
from frames.manage_orders.manage_orders import ManageOrdersFrame
from frames.manage_deliveries.manage_deliveries import ManageDeliveriesFrame

class DashboardChefFrame(tk.Frame):
    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent)
        self.app = app

    def render(self):
        if not self.app.user:
            return

        self.grid_columnconfigure(tuple(range(2)), weight=1)
        tk.Label(self, text=f"Hi there, {self.app.user.first_name} {self.app.user.last_name}! You are a chef", font=self.app.title_font).grid(row=0, column=0, sticky="w")
        tk.Button(self, text="≡", command=lambda: self.app.show_frame('MainFrame'), font=self.app.base_font, bg="blue", fg="white").grid(row=0, column=1, sticky='e')

        ManageOrdersFrame(self, self.app, show_back=False).grid(row=1, column=0, sticky='nsew')
        ManageDeliveriesFrame(self, self.app, show_back=False).grid(row=1, column=1, sticky='nsew')
