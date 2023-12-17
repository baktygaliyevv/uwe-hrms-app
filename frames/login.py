import tkinter as tk
from tkinter import messagebox
import hashlib
import secrets
from datetime import datetime, timedelta
from entities.user_tokens import UserToken
from entities.user import User

from session import Session

class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)  

        title_label = tk.Label(self, text="Log in", font=controller.base_font, bg=self['background'])
        title_label.pack()

        signup_prompt = tk.Label(self, text="New to our app? Sign up", fg="blue", cursor="hand2", font=controller.base_font, bg=self['background'])
        signup_prompt.pack()
        signup_prompt.bind("<Button-1>", lambda _: controller.show_frame('SignupFrame'))

        self.phone_label = tk.Label(self, text="Phone Number", font=controller.base_font, bg=self['background'])
        self.phone_label.pack()
        self.phone_entry = tk.Entry(self, font=controller.base_font)
        self.phone_entry.pack()

        self.password_label = tk.Label(self, text="Password", font=controller.base_font, bg=self['background'])
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show="*", font=controller.base_font)
        self.password_entry.pack()

        self.login_button = tk.Button(self, text="LOGIN", command=self.login_validation, font=controller.base_font, bg=controller.button_color, fg="white", width=20, height=2)
        self.login_button.pack(pady=10)

        self.phone_entry.focus_set()

    def login_validation(self):
        # FIXME вот эта хуйня плохо работает потом пофиксим когда над логикой будем работать
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
            # controller.show_frame(MainFrame)