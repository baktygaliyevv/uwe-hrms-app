import tkinter as tk
from tkinter import ttk
from orm.base import HRMS
from frames.manage_users.popups.add_edit_user import AddEditUserPopup
from frames.manage_users.popups.delete_user import DeleteUserPopup
from constants.constants import ROLE_OPTIONS

class ManageUsersFrame(tk.Frame):
    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent)
        self.app = app
        self.hrms = HRMS()

        self.grid_columnconfigure(tuple(range(2)), weight=1)
        tk.Label(self, text="Users", font=app.title_font).grid(row=0, column=0, sticky="w")
        tk.Button(self, text="Add User", command=self.add_user, font=app.base_font, bg="blue", fg="white").grid(row=0, column=1, sticky='e')

        table = tk.Frame(self)
        table.grid(row=1, column=0, columnspan=2, sticky='ew')
        table.grid_columnconfigure(tuple(range(4)), weight=1)
        tk.Label(table, text="Name", anchor="w", font=app.base_font_bold).grid(row=0, column=0, sticky="ew")
        tk.Label(table, text="Phone", anchor="w", font=app.base_font_bold).grid(row=0, column=1, sticky="ew")
        tk.Label(table, text="Role", anchor="w", font=app.base_font_bold).grid(row=0, column=2, sticky="ew")
        tk.Label(table, text="Actions", anchor="w", font=app.base_font_bold).grid(row=0, column=3, sticky="ew")

        for row, user in enumerate(self.hrms.users):
            row += 1
            tk.Label(table, text=f"{user.first_name} {user.last_name}", anchor='w', font=app.base_font).grid(row=row, column=0, sticky='ew')
            tk.Label(table, text=user.phone, anchor='w', font=app.base_font).grid(row=row, column=1, sticky='ew')
            cb = ttk.Combobox(table, values=ROLE_OPTIONS)
            cb.set(user.role)
            cb.bind('<<ComboboxSelected>>', lambda e, user=user: self.role_changed(user, e.widget.get()))   
            cb.grid(row=row, column=2, sticky='ew')
            actions_frame = tk.Frame(table)
            actions_frame.grid(row=row, column=3, sticky='ew')
            actions_frame.grid_columnconfigure(tuple(range(2)), weight=1)
            tk.Button(actions_frame, text='✎', command=lambda user=user: self.edit_user(user)).grid(row=0, column=0, sticky='ew')
            tk.Button(actions_frame, text='✖', command=lambda user=user: self.delete_user(user)).grid(row=0, column=1, sticky='ew')

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