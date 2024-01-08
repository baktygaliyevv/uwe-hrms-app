# @a2-kaluhin @d2-zhmurenko
import tkinter as tk

DASHBOARDS = {
    'admin': 'MainFrame',
    'manager': 'DashboardManagerFrame',
    'chef': 'DashboardChefFrame',
    'staff': 'DashboardStaffFrame',
    'courier': 'DashboardCourierFrame' 
}

class MainFrame(tk.Frame):
    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent)
        self.app = app
        self.buttons = []

    def render(self):
        self.buttons = [
            tk.Button(self, text='Dashboard', command=lambda: self.goto(self.get_dashboard())),
            tk.Button(self, text='Booking management', command=lambda: self.goto('ManageBookingsFrame'), state=self.get_state('ManageBookingsFrame')),
            tk.Button(self, text='Delivery management', command=lambda: self.goto('ManageDeliveriesFrame'), state=self.get_state('ManageDeliveriesFrame')),
            tk.Button(self, text='Menu management', command=lambda: self.goto('ManageMenuFrame'), state=self.get_state('ManageMenuFrame')),
            tk.Button(self, text='Orders management', command=lambda: self.goto('ManageOrdersFrame'), state=self.get_state('ManageOrdersFrame')),
            tk.Button(self, text='Products management', command=lambda: self.goto('ManageProductsListFrame'), state=self.get_state('ManageProductsListFrame')),
            tk.Button(self, text='Promocodes management', command=lambda: self.goto('ManagePromocodesFrame'), state=self.get_state('ManagePromocodesFrame')),
            tk.Button(self, text="Restaurant Management", command=lambda: self.goto('ManageRestaurantsFrame'), state=self.get_state('ManageRestaurantsFrame')),
            tk.Button(self, text='Restaurant storage management', command=lambda: self.goto('ManageRestaurantProductsFrame'), state=self.get_state('ManageRestaurantProductsFrame')),
            tk.Button(self, text="Table Management", command=lambda: self.goto('ManageTablesFrame'), state=self.get_state('ManageTablesFrame')),
            tk.Button(self, text="User Management", command=lambda: self.goto('ManageUsersFrame'), state=self.get_state('ManageUsersFrame')),
            tk.Button(self, text="Logout", command=lambda: self.app.logout())
        ]

        r = 0
        c = 0
        for b in self.buttons:
            if c == 4:
                c = 0
                r += 1
            b.grid(row=r, column=c, sticky='nsew', padx=5, pady=5)
            c += 1

    def goto(self, frame):
        self.app.show_frame(frame)
        for button in self.buttons:
            button.grid_forget()

    def get_state(self, frame):
        return 'normal' if self.app.is_allowed(frame, self.app.user.role) else 'disabled'
    
    def get_dashboard(self):
        return DASHBOARDS[self.app.user.role]