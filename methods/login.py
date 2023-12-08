import tkinter as tk
from tkinter import messagebox, font
import hashlib
import secrets
from datetime import datetime, timedelta
import sys
from pathlib import Path

project_directory = Path(__file__).resolve().parent.parent
sys.path.append(str(project_directory))

from entities.user_tokens import UserToken
from entities.user import User
from session import Session

class LoginApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Login Screen')
        self.geometry('800x600')  # Set the window size

        # Styling constants
        entry_font = font.Font(size=14)
        button_color = '#2F9AB1'

        # Create a frame for the login widgets and center it
        login_frame = tk.Frame(self, bd=2)
        login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Phone label and entry
        self.phone_label = tk.Label(login_frame, text="Phone", font=entry_font)
        self.phone_label.pack(pady=5)
        self.phone_entry = tk.Entry(login_frame, font=entry_font)
        self.phone_entry.pack(pady=5)

        # Password label and entry
        self.password_label = tk.Label(login_frame, text="Password", font=entry_font)
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(login_frame, show="*", font=entry_font)
        self.password_entry.pack(pady=5)

        # Login button
        self.login_button = tk.Button(login_frame, text="Login", command=self.login, font=entry_font, bg=button_color, fg="white")
        self.login_button.pack(pady=10)

        # Set the focus on the phone entry
        self.phone_entry.focus_set()

    def login(self):
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

    def redirect_to_main_app(self):
        # here will be the logic to open main window
        self.destroy() 

if __name__ == "__main__":
    app = LoginApplication()
    app.mainloop()
