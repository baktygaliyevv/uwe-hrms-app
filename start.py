# @d2-zhmurenko @n2-baktygaliye @a2-kaluhin @y2-bugenov
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve()))

from dotenv import load_dotenv
load_dotenv()

from orm.db import init_db
init_db()

import tkinter as tk
import tkinter.font as font
from orm.base import HRMS
from frames.main_screen.main_screen import MainFrame
from frames.login.login import LoginFrame
from frames.manage_users.manage_users import ManageUsersFrame
from frames.manage_restaurants.manage_restaurants import ManageRestaurantsFrame
from frames.manage_tables.manage_tables import ManageTablesFrame
from frames.manage_promocodes.manage_promocodes import ManagePromocodesFrame
from frames.manage_products.manage_products import ManageProductsListFrame
from frames.manage_bookings.manage_bookings import ManageBookingsFrame
from frames.manage_menu.manage_menu import ManageMenuFrame
from frames.manage_restaurant_products.manage_restaurant_products import ManageRestaurantProductsFrame
from frames.manage_orders.manage_orders import ManageOrdersFrame
from frames.manage_deliveries.manage_deliveries import ManageDeliveriesFrame

from frames.dashboards.dashboard_chef import DashboardChefFrame
from frames.dashboards.dashboard_manager import DashboardManagerFrame
from frames.dashboards.dashboard_staff import DashboardStaffFrame
from frames.dashboards.dashboard_courier import DashboardCourierFrame

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        tk.Tk.geometry(self, '950x600')
        container.pack(side='top', fill='both', expand = True)     
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.base_font = font.Font(size=12)
        self.base_font_bold = font.Font(size=12, weight='bold')
        self.entry_font = font.Font(size=12)
        self.title_font = font.Font(size=24)
        self.background_color = '#F3F3F3'
        self.button_color = '#2F9AB1'

        self.hrms = HRMS()
        self.user = None

        self.__frames = {}

        for F in (MainFrame,
                  LoginFrame, 
                  ManageUsersFrame, 
                  ManageRestaurantsFrame, 
                  ManageTablesFrame, 
                  ManagePromocodesFrame, 
                  ManageProductsListFrame, 
                  ManageBookingsFrame, 
                  ManageMenuFrame,
                  ManageOrdersFrame,
                  ManageDeliveriesFrame,
                  ManageRestaurantProductsFrame,
                  DashboardChefFrame,
                  DashboardManagerFrame,
                  DashboardStaffFrame,
                  DashboardCourierFrame
                  ):
            frame = F(container, self)
            self.__frames[F.__name__] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")

        self.show_frame('LoginFrame')
    
    def show_frame(self, cont):
        frame = self.__frames[cont]    
        frame.tkraise()
        if getattr(frame, 'render', None) and callable(frame.render):
            frame.render()

    def is_allowed(self, cont, role):
        frame = self.__frames[cont]
        if not frame.__allowed_roles__:
            return True
        return role in frame.__allowed_roles__

    def logout(self):
        self.user = None
        self.show_frame('LoginFrame')

app = MainWindow()
app.mainloop()