import tkinter as tk
from tkinter import ttk
from orm.user import User
from constants.constants import ROLE_OPTIONS

class AddEditUserPopup(tk.Toplevel):
    def __init__(self, parent, user=None):
        tk.Toplevel.__init__(self, parent)
        self.title("Add/Edit User")
        self.parent = parent
        self.app = parent.app
        self.user = user
        
        self.first_name_var = tk.StringVar()
        self.last_name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.role_var = tk.StringVar()

        if user:
            self.first_name_var.set(user.first_name)
            self.last_name_var.set(user.last_name)
            self.phone_var.set(user.phone)
            self.role_var.set(user.role)
        else:
            self.role_var.set('staff')

        tk.Label(self, text="First Name:").grid(row=0, column=0, padx=10, pady=5)
        tk.Entry(self, textvariable=self.first_name_var).grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(self, text="Last Name:").grid(row=0, column=2, padx=10, pady=5)
        tk.Entry(self, textvariable=self.last_name_var).grid(row=0, column=3, padx=10, pady=5)
        
        tk.Label(self, text="Phone:").grid(row=1, column=0, padx=10, pady=5)
        tk.Entry(self, textvariable=self.phone_var).grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self, text="Password:" if not user else "Password (leave empty if unchanged):").grid(row=2, column=0, padx=10, pady=5)
        tk.Entry(self, textvariable=self.password_var).grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self, text="Role:").grid(row=3, column=0, padx=10, pady=5)
        role_dropdown = ttk.Combobox(self, textvariable=self.role_var, values=ROLE_OPTIONS)
        role_dropdown.grid(row=3, column=1, padx=10, pady=5)

        save_button = tk.Button(self, text="Save", command=self.save_user)
        save_button.grid(row=4, column=0, columnspan=4, pady=10)

    def save_user(self):
        first_name = self.first_name_var.get()
        last_name = self.last_name_var.get()
        phone = self.phone_var.get()
        password = self.password_var.get()
        role = self.role_var.get()

        if self.user:
            if first_name != self.user.first_name or last_name != self.user.last_name:
                self.user.set_name(first_name, last_name)
            if phone != self.user.phone:
                self.user.set_phone(phone)
            if password:
                self.user.set_password(password)
            if role != self.user.role:
                self.user.set_role(role)
        else:
            self.app.hrms.add_user(User(
                first_name,
                last_name,
                phone,
                password,
                role
            ))

        self.parent.refresh_user_list()
        self.destroy()