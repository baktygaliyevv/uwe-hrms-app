import tkinter as tk
from tkinter import messagebox, font
import hashlib
import secrets
from datetime import datetime, timedelta
import sys
from pathlib import Path
from standard import StandardWindow

project_directory = Path(__file__).resolve().parent.parent
sys.path.append(str(project_directory))

from entities.user_tokens import UserToken
from entities.user import User
from session import Session
class LoginApplication(StandardWindow):
    def __init__(self):
        super().__init__(title='Login Screen', window_size='800x600')

        login_frame = tk.Frame(self, bg=self['background'])
        login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        title_label = tk.Label(login_frame, text="Log in", font=self.standard_font, bg=self['background'])
        title_label.pack()

        signup_prompt = tk.Label(login_frame, text="New to our app? Sign up", fg="blue", cursor="hand2", font=self.standard_font, bg=self['background'])
        signup_prompt.pack()
        signup_prompt.bind("<Button-1>", lambda e: self.open_signup_form())

        self.phone_label = tk.Label(login_frame, text="Phone Number", font=self.standard_font, bg=self['background'])
        self.phone_label.pack()
        self.phone_entry = tk.Entry(login_frame, font=self.standard_font)
        self.phone_entry.pack()

        self.password_label = tk.Label(login_frame, text="Password", font=self.standard_font, bg=self['background'])
        self.password_label.pack()
        self.password_entry = tk.Entry(login_frame, show="*", font=self.standard_font)
        self.password_entry.pack()

        self.login_button = tk.Button(login_frame, text="LOGIN", command=self.login_validation, font=self.standard_font, bg=self.button_color, fg="white", width=20, height=2)
        self.login_button.pack(pady=10)

        self.phone_entry.focus_set()

    def login_validation(self):
        # вот эта хуйня плохо работает потом пофиксим когда над логикой будем работать
        phone = self.phone_entry.get()
        password = self.password_entry.get()

        with Session() as session:
            user = session.query(User).filter_by(phone=phone).first()

            if not user or user.hash != hashlib.sha1((password + user.salt).encode('utf-8')).hexdigest():
                messagebox.showerror("Login Failed", "Incorrect phone number or password.")
                return

            token = secrets.token_hex(32)
            expiration_duration = 60  # 60 days
            expiration_date = datetime.now() + timedelta(days=expiration_duration)

            user_token = UserToken(user_id=user.id, token=token, expiration_date=expiration_date)
            session.add(user_token)
            session.commit()

            # Here you would manage user roles and proceed with the application
            print(f"User logged in with token: {token}")
            
            # redirect to the main application or another window as needed
            self.redirect_to_main_app()

    def open_signup_form(self):
        signup_window = SignupForm(self)
        self.wait_window(signup_window) 

    def redirect_to_main_app(self):
        # here will be the logic to open main window
        self.destroy() 

class SignupForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Sign Up")
        self.geometry('800x600') 
        standard = StandardWindow()  

        self.configure(bg=standard['background'])  

        title_font = standard.standard_font  
        entry_font = standard.entry_font

        title_label = tk.Label(self, text="Create your account", font=title_font, bg=standard['background'])
        title_label.pack(pady=(10, 5))

        login_prompt = tk.Label(self, text="Already have one?", fg="blue", cursor="hand2", bg=standard['background'])
        login_prompt.pack()
        login_prompt.bind("<Button-1>", lambda e: parent.deiconify() or self.destroy()) 

        fields = ["First Name", "Last Name", "Phone Number", "Password", "Confirm Password"]
        for field in fields:
            tk.Label(self, text=field, font=entry_font, bg=standard['background']).pack(pady=(5, 0))
            entry = tk.Entry(self, font=entry_font)
            entry.pack(pady=(0, 5))
            setattr(self, f"{field.lower().replace(' ', '_')}_entry", entry)

        self.password_entry.config(show="*")
        self.confirm_password_entry.config(show="*")

        self.signup_button = tk.Button(self, text="CREATE YOUR ACCOUNT", command=self.register,bg=standard.button_color, fg="white", font=entry_font)
        self.signup_button.pack(pady=10)

    def signup_validation(self):
        fname = self.first_name_entry.get()
        lname = self.last_name_entry.get()
        phone = self.phone_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Add validation logic here
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        # Placeholder for account creation logic
        with Session() as session:
            new_user = User(first_name=fname, last_name=lname, phone=phone, password_hash=hashlib.sha256(password.encode()).hexdigest())
            session.add(new_user)
            session.commit()

        messagebox.showinfo("Success", "Account created successfully, please log in.")

        self.destroy()

if __name__ == "__main__":
    app = LoginApplication()
    app.mainloop()