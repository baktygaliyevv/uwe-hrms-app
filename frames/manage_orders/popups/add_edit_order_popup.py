import tkinter as tk
from tkinter import ttk
from frames.manage_users.popups.add_edit_user import AddEditUserPopup
from components.add_order_menu_item_popup import AddOrderMenuItemPopup
from components.table import TableComponent
from orm.order import Order

class AddEditOrderPopup(tk.Toplevel):
    def __init__(self, parent, restaurant, order = None):
        tk.Toplevel.__init__(self, parent)
        self.title(f"Edit order #{order.id}" if order else "Add order")
        self.parent = parent
        self.app = parent.app
        self.restaurant = restaurant
        self.order = order

        tk.Label(self, text='Restaurant', anchor='w').grid(row=0, column=0, columnspan=2, sticky='ew')
        restaurant_city = tk.StringVar(value=restaurant.city)
        tk.Entry(self, textvariable=restaurant_city, state='disabled').grid(row=1, column=0, columnspan=2, sticky='ew')

        table_ids = list(map(lambda t: t.id, restaurant.get_tables()))
        self.table_id_var = tk.IntVar(value=table_ids[0])
        tk.Label(self, text='Table # ', anchor='w').grid(row=2, column=0, sticky='ew')
        ttk.Combobox(self, values=table_ids, textvariable=self.table_id_var, state='disabled' if order else 'readonly').grid(row=2, column=1, sticky='ew')

        user_names = self.get_users_list()
        self.user_name_var = tk.StringVar(value=user_names[0])
        tk.Label(self, text='Client', anchor='w').grid(row=3, column=0, sticky='ew')
        user_selector_container = tk.Frame(self)
        self.user_selector = ttk.Combobox(user_selector_container, values=user_names, textvariable=self.user_name_var, state='disabled' if order else 'readonly')
        self.user_selector.grid(row=0, column=0, sticky='ew')
        ttk.Button(user_selector_container, text='+', command=self.add_user, state='disabled' if order else 'normal').grid(row=0, column=1, sticky='ew')
        user_selector_container.grid(row=3, column=1, sticky='ew')

        promocodes_ids = ['None'] + list(map(lambda p: p.id, self.app.hrms.promocodes))
        self.promocode_var = tk.StringVar(value=promocodes_ids[0])
        tk.Label(self, text='Promocode', anchor='w', font=self.app.base_font).grid(row=4, column=0, sticky='ew')
        ttk.Combobox(self, values=promocodes_ids, textvariable=self.promocode_var).grid(row=4, column=1, sticky='ew')

        tk.Label(self, text='Menu items', anchor='w', font=self.app.base_font).grid(row=5, column=0, sticky='w')
        tk.Button(self, text='Add item', command=self.add_menu_item).grid(row=5, column=1, sticky='e')

        self.menu_items = order.get_menu_items() if order else []
        self.table = TableComponent(
            self,
            headings=['Item', 'Count', 'Delete'],
            data=self.menu_items,
            get_row=self.get_menu_item_row
        )
        self.table.grid(row=6, column=0, columnspan=2, sticky='ew')

        tk.Button(self, text='Save', command=self.save).grid(row=7, column=0, columnspan=2, sticky='ew')

        if order:
            user = order.get_user()
            promocode = order.get_promocode()

            self.table_id_var.set(order.get_table().id)
            self.user_name_var.set(f'{user.first_name} {user.last_name}' if user else 'Guest')
            self.promocode_var.set(promocode.id if promocode else 'None')

    def get_users_list(self):
        self.user_map = list(map(lambda u: (u, f'{u.first_name} {u.last_name}'), filter(lambda u: u.role == 'client', self.app.hrms.users)))
        return ['Guest'] + list(map(lambda u: u[1], self.user_map))
    
    def refresh_user_list(self):
        user_names = self.get_users_list()
        self.user_selector.config(values=user_names)

    def add_user(self):
        popup = AddEditUserPopup(self)
        self.wait_window(popup)

    def add_menu_item(self):
        popup = AddOrderMenuItemPopup(self, self.restaurant)
        self.wait_window(popup)
        self.table.update_data(self.menu_items)

    def delete_menu_item(self, menu_item):
        self.menu_items.remove(menu_item)
        self.table.update_data(self.menu_items)

    def get_menu_item_row(self, table, row, menu_item):
        item, count = menu_item
        tk.Label(table, text=item.name, anchor='w', font=self.app.base_font).grid(row=row, column=0, sticky='ew')
        tk.Label(table, text=count, anchor='w', font=self.app.base_font).grid(row=row, column=1, sticky='ew')
        tk.Button(table, text='✖', command=lambda menu_item=menu_item: self.delete_menu_item(menu_item)).grid(row=row, column=2, sticky='ew')

    def save(self):
        if self.order:
            if self.promocode_var.get() != self.order.get_promocode().id:
                self.order.set_promocode(self.app.hrms.get_promocode(self.promocode_var.get()))
            prev_menu_items = self.order.get_menu_items()
            for actual_menu_item, actual_quantity in self.menu_items:
                prev_menu_item, prev_quantity = next((mi for mi in prev_menu_items if mi[0] == actual_menu_item), (None, None))
                if not prev_menu_item:
                    self.order.add_menu_item(actual_menu_item, actual_quantity)
                    for product in actual_menu_item.get_products():
                        self.restaurant.update_product_count(product, self.restaurant.get_product(product.id)[1] - 1 * actual_quantity)
                elif actual_quantity != prev_quantity:
                    self.order.set_menu_item_quantity(prev_menu_item, actual_quantity)
                    for product in prev_menu_item.get_products():
                        self.restaurant.update_product_count(product, self.restaurant.get_product(product.id)[1] - 1 * actual_quantity)
        else:
            table = self.restaurant.get_table(self.table_id_var.get())
            order = Order(
                self.app.hrms,
                user=None if self.user_name_var.get() == 'Guest' else next(user[0] for user in self.user_map if user[1] == self.user_name_var.get()),
                table=table,
                promocode=None if self.promocode_var.get() == 'None' else self.app.hrms.get_promocode(self.promocode_var.get())
            )
            table.add_order(order)
            for menu_item, quantity in self.menu_items:
                order.add_menu_item(menu_item, quantity)
                for product in menu_item.get_products():
                    self.restaurant.update_product_count(product,
                                                         self.restaurant.get_product(product.id)[1] - 1 * quantity)
        self.parent.refresh()
        self.destroy()