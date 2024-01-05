import tkinter as tk
from tkinter import messagebox
from frames.manage_orders.popups.add_edit_order_popup import AddEditOrderPopup
from components.restaurant_selector import RestaurantSelectorComponent
from components.table import TableComponent
from components.userinfopopup import UserInfoPopupComponent
from components.promocode_info_popup import PromocodeInfoPopup
from utils.generate_bill import generate_bill

class ManageOrdersFrame(tk.Frame):
    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent)
        self.app = app

        self.grid_columnconfigure(tuple(range(2)), weight=1)

        title_frame = tk.Frame(self)
        tk.Label(title_frame, text="Orders at ", font=self.app.title_font).grid(row=0, column=0, sticky="w")
        self.restaurant_dropdown = RestaurantSelectorComponent(title_frame, app)
        self.restaurant_dropdown.bind('<<RestaurantSelected>>', self.refresh)
        self.restaurant_dropdown.grid(row=0, column=1, sticky='ew')
        title_frame.grid(row=0, column=0, sticky='ew')

        self.show_complete = tk.BooleanVar()
        title_actions_frame = tk.Frame(self)
        title_actions_frame.grid(row=0, column=1, sticky='e')
        tk.Checkbutton(title_actions_frame, text="Show complete", variable=self.show_complete, command=self.refresh, font=self.app.base_font).grid(row=0, column=0, sticky='ew')
        tk.Button(title_actions_frame, text="Place order", command=self.add_order, font=self.app.base_font, bg="blue", fg="white").grid(row=0, column=1, sticky='ew')

        self.table = TableComponent(
            self,
            headings=['Order #', 'Table', 'Client', 'Placed at', 'Complete at', 'Promocode', 'Actions'],
            data=self.get_restaurant_dropdown_data(),
            get_row=self.get_row
        )
        self.table.grid(row=1, column=0, columnspan=2, sticky='ew')

    def get_restaurant_dropdown_data(self):
        orders = self.restaurant_dropdown.get().get_orders()
        if self.show_complete.get():
            return orders
        return list(filter(lambda o: not o.complete_at, orders))

    def refresh(self):
        self.table.update_data(self.get_restaurant_dropdown_data())
    
    def get_row(self, table, row, order):
        user = order.get_user()
        promocode = order.get_promocode()

        tk.Label(table, text=f'# {order.id}', anchor='w', font=self.app.base_font).grid(row=row, column=0, sticky='ew')

        tk.Label(table, text=str(order.get_table().id), anchor='w', font=self.app.base_font).grid(row=row, column=1, sticky='ew')

        user_label = tk.Label(table, text=f'{user.first_name} {user.last_name}' if user else 'Guest', anchor='w', font=self.app.base_font)
        user_label.grid(row=row, column=2, sticky='ew')
        if user:
            user_label.config(fg="blue", cursor="hand2")
            user_label.bind('<Button-1>', lambda _, user=user: self.show_user_popup(user))
        
        tk.Label(table, text=order.created_at.strftime('%H:%M'), anchor='w', font=self.app.base_font).grid(row=row, column=3, sticky='ew')

        if order.complete_at:
            tk.Label(table, text=order.complete_at.strftime('%H:%M'), anchor='w', font=self.app.base_font).grid(row=row, column=4, sticky='ew')
        else:
            tk.Button(table, text='Complete', command=lambda order=order: self.set_order_complete(order)).grid(row=row, column=4, sticky='ew')
        
        promocode_label = tk.Label(table, text=promocode.id if promocode else 'None', anchor='w', font=self.app.base_font)
        promocode_label.grid(row=row, column=5, sticky='ew')
        if promocode:
            promocode_label.config(fg="blue", cursor="hand2")
            promocode_label.bind('<Button-1>', lambda _, promocode=promocode: self.show_promocode_popup(promocode))
        
        actions_frame = tk.Frame(table)
        actions_frame.grid(row=row, column=6, sticky='ew')
        actions_frame.grid_columnconfigure(tuple(range(2)), weight=1)
        tk.Button(actions_frame, text='✎', command=lambda order=order: self.edit_order(order)).grid(row=0, column=0, sticky='ew')
        tk.Button(actions_frame, text='✖', command=lambda order=order: self.delete_order(order)).grid(row=0, column=1, sticky='ew')

    def add_order(self):
        popup = AddEditOrderPopup(self, self.restaurant_dropdown.get())
        self.wait_window(popup)
    
    def edit_order(self, order):
        popup = AddEditOrderPopup(self, self.restaurant_dropdown.get(), order)
        self.wait_window(popup)

    def set_order_complete(self, order):
        order.set_complete()
        self.refresh()
        generate_bill(order)
    
    def delete_order(self, order):
        action = messagebox.askquestion('Delete order', f'Are you sure you want to delete order # {order.id}?', icon='warning')
        if action == 'yes':
            order.get_table().delete_order(order)
            self.refresh()
    
    def show_user_popup(self, user):
        popup = UserInfoPopupComponent(self, user)
        self.wait_window(popup)

    def show_promocode_popup(self, promocode):
        popup = PromocodeInfoPopup(self, promocode)
        self.wait_window(popup)