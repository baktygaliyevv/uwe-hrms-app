import tkinter as tk
from components.table import TableComponent
from frames.manage_menu.popups.add_menu_category import AddMenuCategoryPopup
from frames.manage_menu.popups.add_edit_menu_item import AddEditMenuItemPopup
from frames.manage_menu.popups.menu_products import MenuProductsPopup

class ManageMenuFrame(tk.Frame):
    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent)
        self.app = app

        self.grid_columnconfigure(tuple(range(2)), weight=1)
        tk.Label(self, text="Menu", font=self.app.title_font).grid(row=0, column=0, sticky="w")
        title_actions_frame = tk.Frame(self)
        title_actions_frame.grid(row=0, column=1, sticky='e')
        tk.Button(title_actions_frame, text="Add menu item", command=self.add_menu_item, font=self.app.base_font, bg="blue", fg="white").grid(row=0, column=0, sticky='ew')
        tk.Button(title_actions_frame, text="Add menu category", command=self.add_menu_category, font=self.app.base_font, bg="blue", fg="white").grid(row=0, column=1, sticky='ew')

        tables_frame = tk.Frame(self)
        tables_frame.app = app
        tables_frame.grid(row=1, column=0, columnspan=2, sticky='ew')
        tables_frame.grid_columnconfigure(tuple(range(3)), weight=1)

        self.menu_items_table = TableComponent(
            tables_frame, 
            headings=['Name', 'Category', 'Price', 'Products', 'Actions'],
            data=self.app.hrms.menu_items,
            get_row=self.get_row_menu_items
        )
        self.menu_items_table.grid(row=0, column=0, columnspan=2, sticky='new')
        
        self.menu_categories_table = TableComponent(
            tables_frame,
            headings=['Menu category', 'Delete'],
            data=self.app.hrms.menu_categories,
            get_row=self.get_row_menu_categories
        )
        self.menu_categories_table.grid(row=0, column=2, sticky='new')
        back_to_main_screen_button = tk.Button(self, text="Back to main", command=lambda: self.app.show_frame('MainFrame'))
        back_to_main_screen_button.grid(row=10, column=0, sticky="sw")
        
    def refresh(self):
        self.menu_items_table.update_data(self.app.hrms.menu_items)
        self.menu_categories_table.update_data(self.app.hrms.menu_categories)

    def get_row_menu_items(self, table, row, menu_item):
        tk.Label(table, text=menu_item.name, anchor='w', font=self.app.base_font).grid(row=row, column=0, sticky='ew')
        tk.Label(table, text=menu_item.get_menu_category().name, anchor='w', font=self.app.base_font).grid(row=row, column=1, sticky='ew')
        tk.Label(table, text=f'{menu_item.price}£', anchor='w', font=self.app.base_font).grid(row=row, column=2, sticky='ew')
        products_len = len(menu_item.get_products())
        products_label = tk.Label(table, text=str(products_len), anchor='w', font=self.app.base_font)
        products_label.grid(row=row, column=3, sticky='ew')
        if products_len:
            products_label.config(fg="blue", cursor="hand2")
            products_label.bind('<Button-1>', lambda _, menu_item=menu_item: self.show_menu_products(menu_item))
        actions_frame = tk.Frame(table)
        actions_frame.grid(row=row, column=4, sticky='ew')
        tk.Button(actions_frame, text='✎', command=lambda menu_item=menu_item: self.edit_menu_item(menu_item)).grid(row=0, column=0, sticky='ew')
        tk.Button(actions_frame, text='✖', command=lambda menu_item=menu_item: self.delete_menu_item(menu_item)).grid(row=0, column=1, sticky='ew')
    
    def get_row_menu_categories(self, table, row, menu_category):
        tk.Label(table, text=menu_category.name, anchor='w', font=self.app.base_font).grid(row=row, column=0, sticky='ew')
        tk.Button(table, text='✖', command=lambda menu_category=menu_category: self.delete_menu_category(menu_category)).grid(row=row, column=1, sticky='ew')

    def add_menu_category(self):
        popup = AddMenuCategoryPopup(self)
        self.wait_window(popup)

    def delete_menu_category(self, menu_category):
        action = tk.messagebox.askquestion('Delete menu category', f'Are you sure you want to delete "{menu_category.name}"?', icon='warning')
        if action == 'yes':
            self.app.hrms.delete_menu_category(menu_category)
            self.refresh()

    def show_menu_products(self, menu_item):
        popup = MenuProductsPopup(self, menu_item)
        self.wait_window(popup)
    
    def add_menu_item(self):
        popup = AddEditMenuItemPopup(self)
        self.wait_window(popup)

    def edit_menu_item(self, menu_item):
        popup = AddEditMenuItemPopup(self, menu_item)
        self.wait_window(popup)

    def delete_menu_item(self, menu_item):
        action = tk.messagebox.askquestion('Delete menu item', f'Are you sure you want to delete "{menu_item.name}"?', icon='warning')
        if action == 'yes':
            self.app.hrms.delete_menu_item(menu_item)
            self.refresh()