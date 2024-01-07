import tkinter as tk
from tkinter import messagebox
from components.table import TableComponent
from frames.manage_promocodes.popups.add_edit_promocode import AddEditPromocodePopup

class ManagePromocodesFrame(tk.Frame):
    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent)
        self.app = app

        self.grid_columnconfigure(tuple(range(2)), weight=1)
        tk.Label(self, text="Promocodes", font=self.app.title_font).grid(row=0, column=0, sticky="w")
        tk.Button(self, text="Add Promocode", command=self.add_promocode, font=self.app.base_font, bg="blue", fg="white").grid(row=0, column=1, sticky='e')

        self.table = TableComponent(
            self,
            headings=['Promocodes', 'Discount', 'Valid until', 'Actions'],
            data=self.app.hrms.promocodes,
            get_row=self.get_row
        )
        self.table.grid(row=1, column=0, columnspan=2, sticky='ew')
        back_to_main_screen_button = tk.Button(self, text="Back to main", command=lambda: self.app.show_frame('MainFrame'))
        back_to_main_screen_button.grid(row=10, column=0, sticky="sw")
        
    def get_row(self, table, row, promocode):
        tk.Label(table, text=promocode.id, anchor='w', font=self.app.base_font).grid(row=row, column=0, sticky='ew')
        tk.Label(table, text=f'{promocode.discount}%', anchor='w', font=self.app.base_font).grid(row=row, column=1, sticky='ew')
        tk.Label(table, text=promocode.valid_till.strftime('%d.%m.%Y'), anchor='w', font=self.app.base_font).grid(row=row, column=2, sticky='ew')
        actions_frame = tk.Frame(table)
        actions_frame.grid(row=row, column=3, sticky='ew')
        actions_frame.grid_columnconfigure(tuple(range(2)), weight=1)
        tk.Button(actions_frame, text='✎', command=lambda promocode=promocode: self.edit_promocode(promocode)).grid(row=0, column=0, sticky='ew')
        tk.Button(actions_frame, text='✖', command=lambda promocode=promocode: self.delete_promocode(promocode)).grid(row=0, column=1, sticky='ew')

    def refresh(self):
        self.table.update_data(self.app.hrms.promocodes)

    def add_promocode(self):
        popup = AddEditPromocodePopup(self)
        self.wait_window(popup)

    def edit_promocode(self, promocode):
        popup = AddEditPromocodePopup(self, promocode)
        self.wait_window(popup)

    def delete_promocode(self, promocode):
        action = messagebox.askquestion('Delete promocode', f'Are you sure you want to delete "{promocode.id}"?', icon='warning')
        if action == 'yes':
            self.app.hrms.delete_promocode(promocode)
            self.refresh()