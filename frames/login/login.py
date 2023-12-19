import tkinter as tk
from tkinter import messagebox

class LoginFrame(tk.Frame):
    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent)
        self.app = app

        title_label = tk.Label(self, text="Log in", font=app.base_font, bg=self['background'])
        title_label.pack()

        self.phone_label = tk.Label(self, text="Phone Number", font=app.base_font, bg=self['background'])
        self.phone_label.pack()
        self.phone_entry = tk.Entry(self, font=app.base_font)
        self.phone_entry.pack()

        self.password_label = tk.Label(self, text="Password", font=app.base_font, bg=self['background'])
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show="*", font=app.base_font)
        self.password_entry.pack()

        self.login_button = tk.Button(self, text="LOGIN", command=self.login_validation, font=app.base_font, bg=app.button_color, fg="white", width=20, height=2)
        self.login_button.pack(pady=10)

        self.phone_entry.focus_set()

    def login_validation(self):
        phone = self.phone_entry.get()
        password = self.password_entry.get()

        user = self.app.hrms.find_user(phone)

        if not user or not user.check_password(password):
            return messagebox.showerror("Login Failed", "Incorrect phone number or password.")

        self.app.user = user  

        # self.app.show_frame('MainFrame')