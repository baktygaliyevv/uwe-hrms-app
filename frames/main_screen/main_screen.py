import tkinter as tk

class MainFrame(tk.Frame):
    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent)
        self.app = app

    def render(self):
        manage_booking_button = tk.Button(self, text='Booking management', command=lambda: self.app.show_frame('ManageBookingsFrame'))
        manage_booking_button.pack(side='top', anchor="nw", padx=10, pady=10)
        
        manage_delivery_button = tk.Button(self, text='Delivery management', command=lambda: self.app.show_frame('ManageDeliveriesFrame'))
        manage_delivery_button.pack(side='top', anchor="nw", padx=10, pady=10)

        manage_menu_button = tk.Button(self, text='Menu management', command=lambda: self.app.show_frame('ManageMenuFrame'))
        manage_menu_button.pack(side='top', anchor="nw", padx=10, pady=10)

        manage_orders_button = tk.Button(self, text='Orders management', command=lambda: self.app.show_frame('ManageOrdersFrame'))
        manage_orders_button.pack(side='top', anchor="nw", padx=10, pady=10)

        manage_products_button = tk.Button(self, text='Products management', command=lambda: self.app.show_frame('ManageProductsListFrame'))
        manage_products_button.pack(side='top', anchor="nw", padx=10, pady=10)
        
        manage_promo_button = tk.Button(self, text='Promocodes management', command=lambda: self.app.show_frame('ManagePromocodesFrame'))
        manage_promo_button.pack(side='top', anchor="nw", padx=10, pady=10)
        
        manage_rest_button = tk.Button(self, text="Restaurant Management", command=lambda: self.app.show_frame('ManageRestaurantsFrame'))
        manage_rest_button.pack(side='top', anchor="nw", padx=10, pady=10)
       
        manage_table_button = tk.Button(self, text="Table Management", command=lambda: self.app.show_frame('ManageTablesFrame'))
        manage_table_button.pack(side='top', anchor="nw", padx=10, pady=10)

        manage_user_button = tk.Button(self, text="User Management", command=lambda: self.app.show_frame('ManageUsersFrame'))
        manage_user_button.pack(side='top', anchor="nw", padx=10, pady=10)    
   