import tkinter as tk
from tkinter import messagebox, font
import hashlib
import secrets
from datetime import datetime, timedelta
from standard import StandardWindow
from config import PROJECT_DIRECTORY
from entities.user_tokens import UserToken
from entities.user import User

from session import Session
from signup import SignupForm

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

            print(f"User logged in with token: {token}")
            
            # redirect to the main application or another window as needed
            self.redirect_to_main_app()

    def open_signup_form(self):
        signup_window = SignupForm(self)
        self.wait_window(signup_window) 

    def redirect_to_main_app(self):
        # here will be the logic to open main window
        self.destroy() 