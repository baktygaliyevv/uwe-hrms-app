import tkinter as tk
from tkinter import messagebox
from orm.user import User

class DeleteUserPopup(tk.Toplevel):
    def __init__(self, parent, app, user=None):
        tk.Toplevel.__init__(self, parent)
        self.title("Delete User")
        self.app = app
        self.user = user

        if not user:
            messagebox.showerror("Error", "No user data provided.")
            self.destroy()
            return

        message = f"Are you sure you want to delete {user.first_name} {user.last_name}?"
        tk.Label(self, text=message).grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        yes_button = tk.Button(self, text="Yes", command=self.confirm_delete)
        yes_button.grid(row=1, column=0, padx=10, pady=10)

        no_button = tk.Button(self, text="No", command=self.cancel_delete)
        no_button.grid(row=1, column=1, padx=10, pady=10)

    def confirm_delete(self):
        if self.user:
            try:
                self.app.hrms.delete_user(self.user)
                messagebox.showinfo("Success", "User deleted successfully.")
                self.app.refresh_user_list()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        self.master.refresh_user_list()
        self.destroy()

    def cancel_delete(self):
        self.destroy()
