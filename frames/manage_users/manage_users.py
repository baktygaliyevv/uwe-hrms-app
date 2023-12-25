import tkinter as tk
from tkinter import ttk
from orm.base import HRMS
from frames.manage_users.popups.add_edit_user import AddEditUserPopup
from frames.manage_users.popups.delete_user import DeleteUserPopup
from constants.constants import ROLE_OPTIONS, TableComponent

class ManageUsersFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.hrms = HRMS()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) 
        tk.Label(self, text="Users", font=self.app.title_font).grid(row=0, column=0, sticky="w")
        tk.Button(self, text="Add User", command=self.add_user, font=self.app.base_font, bg="blue", fg="white").grid(row=0, column=1, sticky='e')

        headings = ['First Name', 'Last Name', 'Phone', 'Role', 'Edit', 'Delete']
        self.table_component = TableComponent(
            self,
            headings=headings,
            data=self.hrms.users,
            action_callbacks={
                'edit': self.edit_user,
                'delete': self.delete_user
            }
        )
        self.table_component.grid(row=1, column=0, columnspan=2, sticky='nsew')
        self.populate_users()

    def populate_users(self):
        for row, user in enumerate(self.hrms.users, start=1):
            first_name = f"{user.first_name}"
            last_name = f"{user.last_name}"
            phone = user.phone
            role = user.role

            tk.Label(self.table_component, text=first_name, anchor='center', font=self.app.base_font).grid(row=row, column=0, sticky='nsew')
            tk.Label(self.table_component, text=last_name, anchor='center', font=self.app.base_font).grid(row=row, column=1, sticky='nsew')
            tk.Label(self.table_component, text=phone, anchor='center', font=self.app.base_font).grid(row=row, column=2, sticky='nsew')

            cb = ttk.Combobox(self.table_component, values=ROLE_OPTIONS)
            cb.set(role)
            cb.bind('<<ComboboxSelected>>', lambda e, user=user: self.role_changed(user, e.widget.get()))   
            cb.grid(row=row, column=3, sticky='nsew')

    def role_changed(self, user, role):
        if user.role != role:
            user.set_role(role)

    def add_user(self):
        popup = AddEditUserPopup(self, self.app)
        self.wait_window(popup)

    def edit_user(self, user):
        popup = AddEditUserPopup(self, self.app, user)
        self.wait_window(popup)
    
    def delete_user(self, user):
        popup = DeleteUserPopup(self, self.app, user)
        self.wait_window(popup)
    
    def refresh_user_list(self):
        self.hrms = HRMS()
        self.populate_users()

