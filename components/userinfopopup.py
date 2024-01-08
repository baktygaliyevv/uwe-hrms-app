# @d2-zhmurenko
import tkinter as tk
from orm.user import User

class UserInfoPopupComponent(tk.Toplevel):
    def __init__(self, parent, user: User):
        tk.Toplevel.__init__(self, parent)
        self.title(f'User: {user.first_name} {user.last_name}')
        self.parent = parent

        frame = tk.Frame(self)
        tk.Label(frame, text=f'{user.first_name} {user.last_name}', anchor='w', font=parent.app.base_font).grid(row=0, column=0, sticky='ew')
        tk.Label(frame, text=f'Tel: +44{user.phone}', anchor='w', font=parent.app.base_font).grid(row=1, column=0, sticky='ew')
        tk.Label(frame, text=f'Password: {"set" if user.has_password() else "unset"}', anchor='w', font=parent.app.base_font).grid(row=2, column=0, sticky='ew')
        tk.Label(frame, text=f'Role: {user.role}', anchor='w', font=parent.app.base_font).grid(row=3, column=0, sticky='ew')
        frame.pack(padx=20, pady=20)