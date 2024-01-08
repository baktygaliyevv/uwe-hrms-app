# @d2-zhmurenko @a2-kaluhin
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from frames.manage_deliveries.popups.add_edit_delivery_popup import AddEditDeliveryPopup
from components.restaurant_selector import RestaurantSelectorComponent
from components.table import TableComponent
from components.userinfopopup import UserInfoPopupComponent
from components.promocode_info_popup import PromocodeInfoPopup
from constants.constants import DELIVERY_STATUS_OPTIONS

class ManageDeliveriesFrame(tk.Frame):
    __allowed_roles__ = ['admin', 'chef', 'courier', 'manager']

    def __init__(self, parent, app, show_back = True):
        tk.Frame.__init__(self, parent)
        self.app = app

        self.grid_columnconfigure(tuple(range(2)), weight=1)

        title_frame = tk.Frame(self)
        tk.Label(title_frame, text="Deliveries at ", font=self.app.title_font).grid(row=0, column=0, sticky="w")
        self.restaurant_dropdown = RestaurantSelectorComponent(title_frame, app)
        self.restaurant_dropdown.bind('<<RestaurantSelected>>', lambda _: self.refresh())
        self.restaurant_dropdown.grid(row=0, column=1, sticky='ew')
        title_frame.grid(row=0, column=0, sticky='ew')

        self.show_complete = tk.BooleanVar()
        title_actions_frame = tk.Frame(self)
        title_actions_frame.grid(row=0, column=1, sticky='e')
        tk.Checkbutton(title_actions_frame, text="Show complete", variable=self.show_complete, command=self.refresh, font=self.app.base_font).grid(row=0, column=0, sticky='ew')
        tk.Button(title_actions_frame, text="Place delivery", command=self.add_delivery, font=self.app.base_font, bg="blue", fg="white").grid(row=0, column=1, sticky='ew')

        self.table = TableComponent(
            self,
            headings=['Order #', 'Client', 'Promocode', 'Address', 'Placed at', 'Status', 'Actions'],
            data=self.get_deliveries(),
            get_row=self.get_row
        )
        self.table.grid(row=1, column=0, columnspan=2, sticky='ew')
        
        if show_back:
            tk.Button(self, text="Back to main", command=lambda: self.app.show_frame('MainFrame')).grid(row=10, column=0, sticky="sw")
        
    def get_deliveries(self):
        deliveries = self.restaurant_dropdown.get().get_deliveries()
        if self.show_complete.get():
            return deliveries
        return list(filter(lambda d: d.status != 'complete', deliveries))

    def refresh(self):
        self.table.update_data(self.get_deliveries())
    
    def get_row(self, table, row, delivery):
        user = delivery.get_user()
        promocode = delivery.get_promocode()

        tk.Label(table, text=f'# {delivery.id}', anchor='w', font=self.app.base_font).grid(row=row, column=0, sticky='ew')

        user_label = tk.Label(table, text=f'{user.first_name} {user.last_name}', anchor='w', font=self.app.base_font, fg="blue", cursor="hand2")
        user_label.grid(row=row, column=1, sticky='ew')
        user_label.bind('<Button-1>', lambda _, user=user: self.show_user_popup(user))

        promocode_label = tk.Label(table, text=promocode.id if promocode else 'None', anchor='w', font=self.app.base_font)
        promocode_label.grid(row=row, column=2, sticky='ew')
        if promocode:
            promocode_label.config(fg="blue", cursor="hand2")
            promocode_label.bind('<Button-1>', lambda _, promocode=promocode: self.show_promocode_popup(promocode))

        tk.Button(table, text='Show', command=lambda delivery=delivery: self.show_address(delivery)).grid(row=row, column=3, sticky='ew')
        
        tk.Label(table, text=delivery.created_at.strftime('%H:%M'), anchor='w', font=self.app.base_font).grid(row=row, column=4, sticky='ew')

        cb = ttk.Combobox(table, values=DELIVERY_STATUS_OPTIONS, state='readonly')
        cb.grid(row=row, column=5, sticky='ew')
        cb.set(delivery.status)
        cb.bind('<<ComboboxSelected>>', lambda e, delivery=delivery: self.status_changed(delivery, e.widget.get()))
        
        actions_frame = tk.Frame(table)
        actions_frame.grid(row=row, column=6, sticky='ew')
        actions_frame.grid_columnconfigure(tuple(range(2)), weight=1)
        tk.Button(actions_frame, text='✎', command=lambda delivery=delivery: self.edit_delivery(delivery)).grid(row=0, column=0, sticky='ew')
        tk.Button(actions_frame, text='✖', command=lambda delivery=delivery: self.delete_delivery(delivery)).grid(row=0, column=1, sticky='ew')

    def status_changed(self, delivery, status):
        if delivery.status != status:
            delivery.set_status(status)
            self.refresh()
    
    def add_delivery(self):
        popup = AddEditDeliveryPopup(self, self.restaurant_dropdown.get())
        self.wait_window(popup)
    
    def edit_delivery(self, delivery):
        popup = AddEditDeliveryPopup(self, self.restaurant_dropdown.get(), delivery)
        self.wait_window(popup)
    
    def delete_delivery(self, delivery):
        action = messagebox.askquestion('Delete delivery', f'Are you sure you want to delete delivery # {delivery.id}?', icon='warning')
        if action == 'yes':
            delivery.get_restaurant().delete_delivery(delivery)
            self.refresh()
    
    def show_user_popup(self, user):
        popup = UserInfoPopupComponent(self, user)
        self.wait_window(popup)

    def show_promocode_popup(self, promocode):
        popup = PromocodeInfoPopup(self, promocode)
        self.wait_window(popup)

    def show_address(self, delivery):
        messagebox.showinfo(f'Delivery #{delivery.id}: address', delivery.address)