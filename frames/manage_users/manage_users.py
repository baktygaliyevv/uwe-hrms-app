import tkinter as tk
from tkinter import ttk
from orm.base import HRMS
from frames.manage_users.popups.add_edit_user import AddEditUserPopup
from frames.manage_users.popups.delete_user import DeleteUserPopup

class ManageUsersFrame(tk.Frame):
    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent)
        self.app = app
        self.hrms = HRMS()

        title_label = tk.Label(self, text="Users", font=("Arial", 24))
        title_label.grid(row=0, column=0, sticky="w")

        self.add_user_button = tk.Button(self, text="Add User", command=self.add_user, font=('Arial', 12), bg="blue", fg="white")
        self.add_user_button.grid(row=0, column=1, sticky='e', padx=(0, 10), pady=(10, 0))

        self.create_table()
        self.load_data_from_db()

    def create_table(self):
        columns = ('name', 'phone', 'role', 'actions')
        self.tree = ttk.Treeview(self, columns=columns, show='headings')

        self.tree.heading('name', text='Name')
        self.tree.heading('phone', text='Phone')
        self.tree.heading('role', text='Role')
        self.tree.heading('actions', text='Actions')

        self.tree.column('name', width=200)
        self.tree.column('phone', width=200)
        self.tree.column('role', width=200, anchor='center')
        self.tree.column('actions', width=200)

        self.tree.grid(row=1, column=0, sticky='nsew')

        self.role_options = ['admin', 'manager', 'chef', 'staff', 'courier', 'client']
        self.role_combobox = ttk.Combobox(self, values=self.role_options)
        self.role_combobox.bind('<<ComboboxSelected>>', self.on_role_selected)

        self.tree.bind('<Button-1>', self.on_click)

        self.edit_button = tk.Button(self, text="✎", command=self.edit_selected_user, state='disabled')
        self.edit_button.grid(row=2, column=0, sticky='ew', padx=10, pady=10)

        self.delete_button = tk.Button(self, text="✖", command=self.delete_selected_user, state='disabled')
        self.delete_button.grid(row=2, column=1, sticky='ew', padx=10, pady=10)

        self.tree.bind('<<TreeviewSelect>>', self.on_item_selected)
    
    def on_item_selected(self, event):
        selected_items = self.tree.selection()
        if selected_items: 
            self.edit_button['state'] = 'normal'
            self.delete_button['state'] = 'normal'
        else: 
            self.edit_button['state'] = 'disabled'
            self.delete_button['state'] = 'disabled'

    def edit_selected_user(self):
        selected_item = self.tree.selection()[0]
        user = self.get_user_from_item(selected_item)
        if user:
            self.edit_user(user)

    def delete_selected_user(self):
        selected_item = self.tree.selection()[0]
        user = self.get_user_from_item(selected_item)
        if user:
            self.delete_user(user)

    def get_user_from_item(self, item):
        values = self.tree.item(item, 'values')
        phone = values[1]
        return self.hrms.find_user(phone)
    
    def on_role_selected(self, event):
        selected_role = self.role_combobox.get()
        selected_item = self.tree.selection()[0]

        self.tree.set(selected_item, 'role', selected_role)

        user_phone = self.tree.item(selected_item, 'values')[1]
        user = self.hrms.find_user(user_phone)
        if user:
            user.set_role(selected_role)
            # TODO: error handling
    def load_data_from_db(self):
        for user in self.hrms.users:
            user_id = self.tree.insert('', tk.END, values=(
                f"{user.first_name} {user.last_name}", user.phone, user.role
            ))
            self.add_action_buttons(user_id, user)

    def add_action_buttons(self, item, user):
            bbox = self.tree.bbox(item, column="actions")
            if bbox:
                x, y, width, height = bbox

                action_frame = tk.Frame(self)
                edit_button = tk.Button(action_frame, text="✎", command=lambda u=user: self.edit_user(u), width=2, height=2)
                delete_button = tk.Button(action_frame, text="✖", command=lambda u=user: self.delete_user(u), width=2, height=2)
                
                edit_button.place(x=x, y=y, width=width//2, height=height)
                delete_button.place(x=x+width//2, y=y, width=width//2, height=height)

    def on_click(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region == "cell":
            row_id = self.tree.identify_row(event.y)
            column = self.tree.identify_column(event.x)
            if self.tree.heading(column, 'text') == 'Role':
                self.show_combobox(row_id, column)

    def create_role_combobox(self):
        combobox = ttk.Combobox(self, values=self.role_options)
        combobox.state(['readonly']) 
        return combobox

    def show_combobox(self, item, column):
        x, y, width, height = self.tree.bbox(item, column)
        treeview_height_offset = self.tree.winfo_height() - self.tree.winfo_reqheight()
        combobox_y = y + treeview_height_offset
        self.role_combobox.place(x=x, y=combobox_y, width=width, height=height)
        self.role_combobox.focus()

        current_role = self.tree.item(item, 'values')[2]
        self.role_combobox.set(current_role)

        self.role_combobox.bind('<<ComboboxSelected>>', lambda e: self.update_role(item))

    def update_role(self, item):
        new_role = self.role_combobox.get()
        self.tree.set(item, 'role', new_role)
        user_phone = self.tree.item(item, 'values')[1]
        user = self.hrms.find_user(user_phone)
        if user:
            user.set_role(new_role)
        self.role_combobox.place_forget()

    def add_user(self):
        popup = AddEditUserPopup(self, self.app)
        self.wait_window(popup)

    def edit_user(self, user):
        popup = AddEditUserPopup(self, self.app, user)
        self.wait_window(popup)
    
    def delete_user(self, user):
        popup = DeleteUserPopup(self, self.app, user)
        self.wait_window(popup)