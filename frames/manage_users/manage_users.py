import tkinter as tk
from frames.manage_users.popups.add_edit_user import AddEditUserPopup

class ManageUsersFrame(tk.Frame):
    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent)
        self.app = app

        # TODO remove debug buttons
        temp_add_user = tk.Button(self, text="Call popup (add)", command=self.add_user, font=app.base_font, bg=app.button_color, fg="white", width=20, height=2)
        temp_add_user.pack()

        temp_edit_user = tk.Button(self, 
                                   text="Call popup (edit user #1)", 
                                   command=lambda: self.edit_user(app.hrms.find_user('7442149457')), 
                                   font=app.base_font, bg=app.button_color, fg="white", width=20, height=2
                                )
        temp_edit_user.pack()

    def add_user(self):
        popup = AddEditUserPopup(self, self.app)
        self.wait_window(popup)

    def edit_user(self, user):
        popup = AddEditUserPopup(self, self.app, user)
        self.wait_window(popup)