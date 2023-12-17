import tkinter as tk
from tkinter import messagebox
import hashlib
from entities.user import User

from session import Session

class SignupFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        title_label = tk.Label(self, text="Create your account", font=controller.base_font, bg=parent['background'])
        title_label.pack(pady=(10, 5))

        login_prompt = tk.Label(self, text="Already have one?", fg="blue", cursor="hand2", bg=parent['background'])
        login_prompt.pack()
        login_prompt.bind("<Button-1>", lambda _: controller.show_frame('LoginFrame')) 

        self.first_name_entry = self.create_entry("First Name", controller.entry_font)
        self.last_name_entry = self.create_entry("Last Name", controller.entry_font)
        self.phone_entry = self.create_entry("Phone Number", controller.entry_font)
        self.password_entry = self.create_entry("Password", controller.entry_font, show="*")
        self.confirm_password_entry = self.create_entry("Confirm Password", controller.entry_font, show="*")

        self.signup_button = tk.Button(self, text="CREATE YOUR ACCOUNT", command=self.signup_validation, bg=controller.button_color, fg="white", font=controller.entry_font)
        self.signup_button.pack(pady=10)

    def create_entry(self, label, font, show=None):
        """Helper function to create labeled entry fields."""
        tk.Label(self, text=label, font=font, bg=self['background']).pack(pady=(5, 0))
        entry = tk.Entry(self, font=font, show=show)
        entry.pack(pady=(0, 5))
        return entry
    
    def signup_validation(self):
        fname = self.first_name_entry.get()
        lname = self.last_name_entry.get()
        phone = self.phone_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not fname or not lname or not phone or not password or not confirm_password:
            messagebox.showerror("Error", "All fields must be filled")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        with Session() as session:
            new_user = User(first_name=fname, last_name=lname, phone=phone, password_hash=hashlib.sha256(password.encode()).hexdigest())
            session.add(new_user)
            session.commit()

        messagebox.showinfo("Success", "Account created successfully, please log in.")

        self.controller.show_frame('LoginFrame')