import tkinter as tk
from tkinter import messagebox
from orm.user import User

class DeleteUserPopup(tk.Toplevel):
    def __init__(self, parent, app, user=None):
        tk.Toplevel.__init__(self, parent)
        self.title("Delete User")
        self.app = app
        self.user = user

        # Check if user data is provided
        if not user:
            messagebox.showerror("Error", "No user data provided.")
            self.destroy()
            return

        # Setup the confirmation message
        message = f"Are you sure you want to delete {user.first_name} {user.last_name}?"
        tk.Label(self, text=message).grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Yes button to confirm deletion
        yes_button = tk.Button(self, text="Yes", command=self.confirm_delete)
        yes_button.grid(row=1, column=0, padx=10, pady=10)

        # No button to cancel deletion
        no_button = tk.Button(self, text="No", command=self.cancel_delete)
        no_button.grid(row=1, column=1, padx=10, pady=10)

    def confirm_delete(self):
        # Perform deletion logic here
        if self.user:
            try:
                # Assuming delete_user is a method in HRMS to delete a user
                self.app.hrms.delete_user(self.user)
                messagebox.showinfo("Success", "User deleted successfully.")
                # Call a method to refresh the user list if necessary
                self.app.refresh_user_list()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        self.destroy()

    def cancel_delete(self):
        self.destroy()
