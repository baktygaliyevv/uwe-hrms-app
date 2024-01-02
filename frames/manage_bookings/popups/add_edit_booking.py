import tkinter as tk
from tkinter import ttk
from datetime import date, time, datetime
from tkcalendar import DateEntry
from tktimepicker import SpinTimePickerOld
from tktimepicker import constants
from orm.booking import Booking
from frames.manage_users.popups.add_edit_user import AddEditUserPopup

class AddEditBookingPopup(tk.Toplevel):
    def __init__(self, parent, restaurant, booking = None):
        tk.Toplevel.__init__(self, parent)
        self.title(f"Edit booking {booking.date.strftime('%d.%m.%Y %H:%M')} booking of table #{booking.get_table().id}?" if booking else "Add Booking")
        self.parent = parent
        self.app = parent.app
        self.booking = booking
        self.restaurant = restaurant

        now = datetime.now()

        tk.Label(self, text='Restaurant', anchor='w').grid(row=0, column=0, columnspan=2, sticky='ew')
        restaurant_city = tk.StringVar()
        restaurant_city.set(restaurant.city)
        tk.Entry(self, textvariable=restaurant_city, state='disabled').grid(row=1, column=0, columnspan=2, sticky='ew')

        table_ids = list(map(lambda t: t.id, restaurant.get_tables()))
        self.table_id_var = tk.IntVar(value=table_ids[0])
        tk.Label(self, text='Table # ', anchor='w').grid(row=2, column=0, sticky='ew')
        ttk.Combobox(self, values=table_ids, textvariable=self.table_id_var, state='disabled' if booking else 'readonly').grid(row=2, column=1, sticky='ew')

        user_names = self.get_users_list()
        self.user_name_var = tk.StringVar(value=user_names[0])
        tk.Label(self, text='Client', anchor='w').grid(row=3, column=0, sticky='ew')
        user_selector_container = tk.Frame(self)
        self.user_selector = ttk.Combobox(user_selector_container, values=user_names, textvariable=self.user_name_var, state='disabled' if booking else 'readonly')
        self.user_selector.grid(row=0, column=0, sticky='ew')
        ttk.Button(user_selector_container, text='+', command=self.add_user, state='disabled' if booking else 'normal').grid(row=0, column=1, sticky='ew')
        user_selector_container.grid(row=3, column=1, sticky='ew')

        self.persons_var = tk.IntVar()
        tk.Label(self, text='Persons', anchor='w').grid(row=4, column=0, sticky='ew')
        tk.Entry(self, textvariable=self.persons_var).grid(row=4, column=1, sticky='ew')

        tk.Label(self, text='DateTime', anchor='w').grid(row=5, column=0, sticky='ew')
        self.calendar = DateEntry(
            self,
            selectmode='day',
            date_pattern='dd.mm.yyyy',
            year=booking.date.year if booking else now.year,
            month=booking.date.month if booking else now.month,
            day=booking.date.day if booking else now.day
        )
        self.calendar.grid(row=5, column=1, sticky='ew')

        hours_var = tk.IntVar(value=now.hour)
        minutes_var = tk.IntVar(value=now.minute)
        self.timepicker = SpinTimePickerOld(
            self
        )
        self.timepicker.addAll(constants.HOURS24)
        self.timepicker._24HrsTime.config(textvariable=hours_var)
        self.timepicker._minutes.config(textvariable=minutes_var)
        self.timepicker.grid(row=6, column=1, sticky='ew')

        self.comment_var = tk.StringVar()
        tk.Label(self, text='Comment', anchor='w').grid(row=7, column=0, columnspan=2, sticky='ew')
        tk.Entry(self, textvariable=self.comment_var).grid(row=8, column=0, columnspan=2, sticky='ew')

        tk.Button(self, text='Save', command=self.save).grid(row=9, column=0, columnspan=2, sticky='ew')

        if booking:
            user = booking.get_user()

            self.table_id_var.set(booking.get_table().id)
            self.user_name_var.set(f'{user.first_name} {user.last_name}')
            self.persons_var.set(booking.persons)
            hours_var.set(booking.date.hour)
            minutes_var.set(booking.date.minute)
            self.comment_var.set(booking.comment)
            
    def get_users_list(self):
        self.user_map = list(map(lambda u: (u, f'{u.first_name} {u.last_name}'), filter(lambda u: u.role == 'client', self.app.hrms.users)))
        return list(map(lambda u: u[1], self.user_map))

    def refresh_user_list(self):
        user_names = self.get_users_list()
        self.user_selector.config(values=user_names)

    def add_user(self):
        popup = AddEditUserPopup(self)
        self.wait_window(popup)

    def save(self):
        if self.booking:
            if self.persons_var.get() != self.booking.persons:
                self.booking.set_persons(self.persons_var.get())
            dt = datetime.combine(self.calendar.get_date(), time(*self.timepicker.time()[:2]))
            if dt != self.booking.date:
                self.booking.set_date(dt)
            if self.comment_var.get() != self.booking.comment:
                self.booking.set_comment(self.comment_var.get())
        else:
            table = self.restaurant.get_table(self.table_id_var.get())
            user = next(user[0] for user in self.user_map if user[1] == self.user_name_var.get())
            table.add_booking(Booking(
                self.app.hrms,
                user=user,
                table=table,
                persons=self.persons_var.get(),
                date=datetime.combine(self.calendar.get_date(), time(*self.timepicker.time()[:2])),
                comment=self.comment_var.get()
            ))
        self.parent.refresh()
        self.destroy()