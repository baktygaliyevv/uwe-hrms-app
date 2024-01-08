# @d2-zhmurenko @a2-kaluhin
import tkinter as tk
from tkinter import messagebox
from components.table import TableComponent
from components.restaurant_selector import RestaurantSelectorComponent
from components.userinfopopup import UserInfoPopupComponent
from frames.manage_bookings.popups.add_edit_booking import AddEditBookingPopup

def get_tables_bookings(tables):
    bookings = []
    for table in tables:
        bookings.extend(table.get_bookings())
    return bookings

class ManageBookingsFrame(tk.Frame):
    __allowed_roles__ = ['admin', 'manager']

    def __init__(self, parent, app, show_back = True):
        tk.Frame.__init__(self, parent)
        self.app = app

        self.grid_columnconfigure(tuple(range(2)), weight=1)
        
        title_frame = tk.Frame(self)
        tk.Label(title_frame, text="Bookings at ", font=self.app.title_font).grid(row=0, column=0, sticky="w")
        self.restaurant_dropdown = RestaurantSelectorComponent(title_frame, app)
        self.restaurant_dropdown.bind('<<RestaurantSelected>>', self.refresh)
        self.restaurant_dropdown.grid(row=0, column=1, sticky='ew')
        title_frame.grid(row=0, column=0, sticky='ew')

        tk.Button(self, text="Add Booking", command=self.add_booking, font=self.app.base_font, bg="blue", fg="white").grid(row=0, column=1, sticky='e')

        self.table = TableComponent(
            self,
            headings=['Table #', 'Client', 'Persons', 'DateTime', 'Comment', 'Actions'],
            data=get_tables_bookings(self.restaurant_dropdown.get().get_tables()),
            get_row=self.get_row
        )
        self.table.grid(row=1, column=0, columnspan=2, sticky='ew')

        if show_back:
            tk.Button(self, text="Back to main", command=lambda: self.app.show_frame('MainFrame')).grid(row=10, column=0, sticky="sw")
        
    def refresh(self, _ = None):
        self.table.update_data(get_tables_bookings(self.restaurant_dropdown.get().get_tables()))
    
    def get_row(self, table, row, booking):
        booking_table = booking.get_table()
        user = booking.get_user()
        tk.Label(table, text=f'#{booking_table.id}', anchor='w', font=self.app.base_font).grid(row=row, column=0, sticky='ew')
        user_label = tk.Label(table, text=f'{user.first_name} {user.last_name}', anchor='w', font=self.app.base_font, fg="blue", cursor="hand2")
        user_label.grid(row=row, column=1, sticky='ew')
        user_label.bind('<Button-1>', lambda _, user=user: self.show_user_popup(user))
        tk.Label(table, text=booking.persons, anchor='w', font=self.app.base_font).grid(row=row, column=2, sticky='ew')
        tk.Label(table, text=booking.date.strftime('%d.%m.%Y %H:%M'), anchor='w', font=self.app.base_font).grid(row=row, column=3, sticky='ew')
        tk.Label(table, text=booking.comment, anchor='w', font=self.app.base_font).grid(row=row, column=4, sticky='ew')
        actions_frame = tk.Frame(table)
        actions_frame.grid(row=row, column=5, sticky='ew')
        actions_frame.grid_columnconfigure(tuple(range(2)), weight=1)
        tk.Button(actions_frame, text='✎', command=lambda booking=booking: self.edit_booking(booking)).grid(row=0, column=0, sticky='ew')
        tk.Button(actions_frame, text='✖', command=lambda booking=booking: self.delete_booking(booking)).grid(row=0, column=1, sticky='ew')

    def add_booking(self):
        popup = AddEditBookingPopup(self, self.restaurant_dropdown.get())
        self.wait_window(popup)
    
    def edit_booking(self, booking):
        popup = AddEditBookingPopup(self, self.restaurant_dropdown.get(), booking)
        self.wait_window(popup)
    
    def delete_booking(self, booking):
        booking_table = booking.get_table()
        action = messagebox.askquestion('Delete booking', f'Are you sure you want to delete {booking.date.strftime("%d.%m.%Y %H:%M")} booking of table #{booking_table.id}?', icon='warning')
        if action == 'yes':
            booking.get_table().delete_booking(booking)
            self.refresh()
    
    def show_user_popup(self, user):
        popup = UserInfoPopupComponent(self, user)
        self.wait_window(popup)