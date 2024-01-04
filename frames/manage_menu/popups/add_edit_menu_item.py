import tkinter as tk
from tkinter import ttk
from frames.manage_menu.popups.add_menu_category import AddMenuCategoryPopup
from orm.menu_item import MenuItem

class AddEditMenuItemPopup(tk.Toplevel):
    def __init__(self, parent, menu_item = None):
        tk.Toplevel.__init__(self, parent)
        self.title(f"Edit {menu_item.name}" if menu_item else "Add menu item")
        self.parent = parent
        self.app = parent.app
        self.menu_item = menu_item

        self.name_var = tk.StringVar()

        tk.Label(self, text='Name', anchor='w', font=self.app.base_font).grid(row=0, column=0, columnspan=2, sticky='ew')
        tk.Entry(self, textvariable=self.name_var, state='disabled' if menu_item else 'normal').grid(row=1, column=0, columnspan=2, sticky='ew')

        tk.Label(self, text='Category', anchor='w', font=self.app.base_font).grid(row=2, column=0, sticky='ew')
        category_selector_frame = tk.Frame(self)
        category_selector_frame.grid(row=2, column=1, sticky='ew')

        categories_names = self.get_categories_names()
        self.category_var = tk.StringVar(value=categories_names[0])
        self.category_combobox = ttk.Combobox(category_selector_frame, values=categories_names, textvariable=self.category_var)
        self.category_combobox.grid(row=0, column=0, sticky='ew')

        tk.Button(category_selector_frame, text='+', command=self.add_category).grid(row=0, column=1, sticky='ew')

        tk.Label(self, text='Price', anchor='w', font=self.app.base_font).grid(row=3, column=0, sticky='ew')
        price_entry_frame = tk.Frame(self)
        price_entry_frame.grid(row=3, column=1, sticky='ew')

        self.price_var = tk.IntVar()
        tk.Entry(price_entry_frame, textvariable=self.price_var).grid(row=0, column=0, sticky='ew')
        tk.Label(price_entry_frame, text='£', anchor='w', font=self.app.base_font).grid(row=0, column=1, sticky='ew')

        tk.Label(self, text='Products', anchor='w', font=self.app.base_font).grid(row=4, column=0, sticky='ew')

        self.products = list(map(lambda p: (p, p.name), self.app.hrms.products))
        products_names = list(map(lambda p: p[1], self.products))
        self.products_listbox = tk.Listbox(self, selectmode='multiple', exportselection=0)
        self.products_listbox.insert(tk.END, *products_names)
        self.products_listbox.grid(row=4, column=1, sticky='ew')

        tk.Button(self, text='Save', command=self.save).grid(row=5, column=0, columnspan=2, sticky='ew')

        if menu_item:
            self.name_var.set(menu_item.name)
            self.category_var.set(menu_item.get_menu_category().name)
            self.price_var.set(menu_item.price)
            products = menu_item.get_products()
            for i, product in enumerate(self.products):
                if product[0] in products:
                    self.products_listbox.selection_set(i)
                    self.products_listbox.see(i)
                    self.products_listbox.activate(i)
                    self.products_listbox.selection_anchor(i)

    def get_categories_names(self):
        self.categories = list(map(lambda c: (c, c.name), self.app.hrms.menu_categories))
        return list(map(lambda c: c[1], self.categories))
    
    def refresh(self):
        self.parent.refresh()
        self.category_combobox.config(values=self.get_categories_names())

    def add_category(self):
        popup = AddMenuCategoryPopup(self)
        self.wait_window(popup)
    
    def save(self):
        if self.menu_item:
            return # TODO
        else:
            menu_item = MenuItem(
                self.app.hrms,
                name=self.name_var.get(),
                price=self.price_var.get(),
                menu_category=next(c[0] for c in self.categories if c[1] == self.category_var.get())
            )
            self.app.hrms.add_menu_item(menu_item)
            for selected_prod in [self.products_listbox.get(idx) for idx in self.products_listbox.curselection()]:
                menu_item.add_product(next(p[0] for p in self.products if p[1] == selected_prod))
        self.parent.refresh()
        self.destroy()