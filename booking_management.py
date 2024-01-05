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

from frames.login.login import LoginFrame
from frames.manage_users.manage_users import ManageUsersFrame
from frames.manage_restaurants.manage_restaurants import ManageRestaurantsFrame
from frames.manage_tables.manage_tables import ManageTablesFrame
from frames.manage_promocodes.manage_promocodes import ManagePromocodesFrame
from frames.manage_products.manage_products import ManageProductsListFrame
from frames.manage_bookings.manage_bookings import ManageBookingsFrame

class BookingManagementWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.geometry(self, '800x600')

        container = tk.Frame(self)
        
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

        self.frames = {}

        frame = ManageBookingsFrame(container, self)
        self.frames[ManageBookingsFrame.__name__] = frame
        frame.grid(row = 0, column= 0, sticky= "nsew")
            
        
        self.show_frame('ManageBookingsFrame')

    def show_frame(self, cont):
        frame = self.frames[cont]    
        frame.tkraise()
app = BookingManagementWindow()
app.mainloop()