# @d2-zhmurenko @n2-baktygaliye
import tkinter as tk
from tkcalendar import DateEntry
from datetime import date
from orm.promocode import Promocode

class AddEditPromocodePopup(tk.Toplevel):
    def __init__(self, parent, promocode = None):
        tk.Toplevel.__init__(self, parent)
        self.title(f"Edit promocode {promocode.id}" if promocode else "Add Promocode")
        self.parent = parent
        self.app = parent.app
        self.promocode = promocode

        self.promocode_id = tk.StringVar()
        self.discount = tk.IntVar()

        tk.Label(self, text='Promocode', anchor='w', font=self.app.base_font).grid(row=0, column=0, columnspan=2, sticky='ew')
        promocode_entry = tk.Entry(self, textvariable=self.promocode_id)
        promocode_entry.grid(row=1, column=0, columnspan=2, sticky='ew')
        tk.Label(self, text='Discount %', anchor='w', font=self.app.base_font).grid(row=2, column=0, sticky='ew')
        tk.Entry(self, textvariable=self.discount).grid(row=2, column=1, sticky='ew')
        tk.Label(self, text='Valid till', anchor='w', font=self.app.base_font).grid(row=3, column=0, sticky='ew')
        today = date.today()
        self.calendar = DateEntry(
            self,
            selectmode='day',
            date_pattern='dd.mm.yyyy',
            year=promocode.valid_till.year if promocode else today.year,
            month=promocode.valid_till.month if promocode else today.month,
            day=promocode.valid_till.day if promocode else today.day
        )
        self.calendar.grid(row=3, column=1, sticky='ew')
        tk.Button(self, text='Save', command=self.save).grid(row=4, column=0, columnspan=2, sticky='ew')

        if promocode:
            self.promocode_id.set(promocode.id)
            self.discount.set(promocode.discount)
            promocode_entry.config(state='disabled')

    def save(self):
        if self.promocode:
            if self.discount.get() != self.promocode.discount:
                self.promocode.set_discount(self.discount.get())
            if self.calendar.get_date() != self.promocode.valid_till:
                self.promocode.set_valid_till(self.calendar.get_date())
        else:
            self.app.hrms.add_promocode(Promocode(
                self.app.hrms,
                id=self.promocode_id.get(),
                discount=self.discount.get(),
                valid_till=self.calendar.get_date()
            ))
        self.parent.refresh()
        self.destroy()