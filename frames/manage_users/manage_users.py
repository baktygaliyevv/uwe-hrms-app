# @d2-zhmurenko @n2-baktygaliye @a2-kaluhin
import tkinter as tk
from tkinter import ttk
from orm.base import HRMS
from frames.manage_users.popups.add_edit_user import AddEditUserPopup
from frames.manage_users.popups.delete_user import DeleteUserPopup
from constants.constants import ROLE_OPTIONS 
from components.table import TableComponent

class ManageUsersFrame(tk.Frame):
    __allowed_roles__ = ['admin']

    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent)
        self.app = app

        self.grid_columnconfigure(tuple(range(2)), weight=1)
        tk.Label(self, text="Users", font=self.app.title_font).grid(row=0, column=0, sticky="w")
        tk.Button(self, text="Add User", command=self.add_user, font=self.app.base_font, bg="blue", fg="white").grid(row=0, column=1, sticky='e')

        self.table = TableComponent(
            self,
            headings = ['Name', 'Phone', 'Role', 'Actions'],
            data=self.app.hrms.users,
            get_row=self.get_row
        )
        self.table.grid(row=1, column=0, columnspan=2, sticky='ew')
        back_to_main_screen_button = tk.Button(self, text="Back to main", command=lambda: self.app.show_frame('MainFrame'))
        back_to_main_screen_button.grid(row=10, column=0, sticky="sw")
        
    def get_row(self, table, row, user):
        tk.Label(table, text=f"{user.first_name} {user.last_name}", anchor='w', font=self.app.base_font).grid(row=row, column=0, sticky='ew')
        tk.Label(table, text=user.phone, anchor='w', font=self.app.base_font).grid(row=row, column=1, sticky='ew')
        cb = ttk.Combobox(table, values=ROLE_OPTIONS)
        cb.set(user.role)
        cb.bind('<<ComboboxSelected>>', lambda e, user=user: self.role_changed(user, e.widget.get()))   
        cb.grid(row=row, column=2, sticky='ew')
        actions_frame = tk.Frame(table)
        actions_frame.grid(row=row, column=3, sticky='ew')
        actions_frame.grid_columnconfigure(tuple(range(2)), weight=1)
        tk.Button(actions_frame, text='✎', command=lambda user=user: self.edit_user(user)).grid(row=0, column=0, sticky='ew')
        tk.Button(actions_frame, text='✖', command=lambda user=user: self.delete_user(user)).grid(row=0, column=1, sticky='ew')

    def refresh_user_list(self):
        self.table.update_data(self.app.hrms.users)

    def role_changed(self, user, role):
        if user.role != role:
            user.set_role(role)

    def add_user(self):
        popup = AddEditUserPopup(self)
        self.wait_window(popup)

    def edit_user(self, user):
        popup = AddEditUserPopup(self, user)
        self.wait_window(popup)
    
    def delete_user(self, user):
        popup = DeleteUserPopup(self, user)
        self.wait_window(popup)