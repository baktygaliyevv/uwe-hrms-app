# @d2-zhmurenko
import tkinter as tk

class PromocodeInfoPopup(tk.Toplevel):
    def __init__(self, parent, promocode):
        tk.Toplevel.__init__(self, parent)
        self.title(f'Promocode: {promocode.id}')
        self.parent = parent

        frame = tk.Frame(self)
        tk.Label(frame, text=promocode.id, anchor='w', font=parent.app.base_font).grid(row=0, column=0, sticky='ew')
        tk.Label(frame, text=f'Discount: {promocode.discount}%', anchor='w', font=parent.app.base_font).grid(row=1, column=0, sticky='ew')
        tk.Label(frame, text=f'Valid till: {promocode.valid_till.strftime("%d.%m.%Y")}', anchor='w', font=parent.app.base_font).grid(row=2, column=0, sticky='ew')
        frame.pack(padx=20, pady=20)