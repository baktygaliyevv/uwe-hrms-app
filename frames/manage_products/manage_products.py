import tkinter as tk
from components.table import TableComponent
from frames.manage_products.popups.add_edit_products import AddEditProductPopup

class ManageProductsListFrame(tk.Frame):
    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent)
        self.app = app

        self.grid_columnconfigure(tuple(range(2)), weight=1)
        tk.Label(self, text="Products", font=self.app.title_font).grid(row=0, column=0, sticky="w")
        tk.Button(self, text="Add Product", command=self.add_product, font=self.app.base_font, bg="blue", fg="white").grid(row=0, column=1, sticky='e')

        self.table = TableComponent(
            self,
            headings=['Name', 'Vegan', 'Vegetarian', 'Gluten Free', 'Actions'],
            data=self.app.hrms.products,
            get_row=self.get_row
        )
        self.table.grid(row=1, column=0, columnspan=2, sticky='ew')
        back_to_main_screen_button = tk.Button(self, text="Back to main", command=lambda: self.app.show_frame('MainFrame'))
        back_to_main_screen_button.grid(row=10, column=0, sticky="sw")
        
    def get_row(self, table, row, product):
        tk.Label(table, text=product.name, anchor='w', font=self.app.base_font).grid(row=row, column=0, sticky='ew')
        tk.Label(table, text='Yes' if product.vegan else 'No', anchor='w', font=self.app.base_font).grid(row=row, column=1, sticky='ew')
        tk.Label(table, text='Yes' if product.vegetarian else 'No', anchor='w', font=self.app.base_font).grid(row=row, column=2, sticky='ew')
        tk.Label(table, text='Yes' if product.gluten_free else 'No', anchor='w', font=self.app.base_font).grid(row=row, column=3, sticky='ew')
        actions_frame = tk.Frame(table)
        actions_frame.grid(row=row, column=4, sticky='ew')
        actions_frame.grid_columnconfigure(tuple(range(2)), weight=1)
        tk.Button(actions_frame, text='✎', command=lambda product=product: self.edit_product(product)).grid(row=0, column=0, sticky='ew')
        tk.Button(actions_frame, text='✖', command=lambda product=product: self.delete_product(product)).grid(row=0, column=1, sticky='ew')

    def refresh(self):
        self.table.update_data(self.app.hrms.products)

    def add_product(self):
        popup = AddEditProductPopup(self)
        self.wait_window(popup)

    def edit_product(self, product):
        popup = AddEditProductPopup(self, product)
        self.wait_window(popup)

    def delete_product(self, product):
        action = tk.messagebox.askquestion('Delete product', f'Are you sure you want to delete "{product.name}"?', icon='warning')
        if action == 'yes':
            self.app.hrms.delete_product(product)
            self.refresh()