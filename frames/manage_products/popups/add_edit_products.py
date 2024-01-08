# @y2-bugenov
import tkinter as tk
from tkinter import messagebox
from orm.product import Product

class AddEditProductPopup(tk.Toplevel):
    def __init__(self, parent, product=None):
        tk.Toplevel.__init__(self, parent)
        self.title(f"Edit Product {product.name}" if product else "Add Product")
        self.parent = parent
        self.app = parent.app
        self.product = product

        self.product_name = tk.StringVar()
        self.vegan = tk.BooleanVar(value=False)
        self.vegetarian = tk.BooleanVar(value=False)
        self.gluten_free = tk.BooleanVar(value=False)

        tk.Label(self, text='Add/Edit Product', font=self.app.base_font).grid(row=0, column=0, columnspan=2, sticky='ew')

        # Product Name Field
        tk.Label(self, text='Name:', font=self.app.base_font).grid(row=1, column=0, sticky='w')
        tk.Entry(self, textvariable=self.product_name, state='disabled' if product else 'normal').grid(row=1, column=1, sticky='ew')

        # Checkboxes
        tk.Checkbutton(self, text="Vegan", variable=self.vegan).grid(row=2, column=0, sticky='w')
        tk.Checkbutton(self, text="Vegetarian", variable=self.vegetarian).grid(row=3, column=0, sticky='w')
        tk.Checkbutton(self, text="Gluten Free", variable=self.gluten_free).grid(row=4, column=0, sticky='w')

        # Save Button
        tk.Button(self, text='Save', command=self.save).grid(row=5, column=0, columnspan=2, sticky='ew')

        if product:
            self.product_name.set(product.name)
            self.vegan.set(product.vegan)
            self.vegetarian.set(product.vegetarian)
            self.gluten_free.set(product.gluten_free)

    def save(self):
        product_name = self.product_name.get()
        if not product_name:
            return messagebox.showerror("Error", "Product name cannot be empty.")

        if self.product:
            if self.vegan.get() != self.product.vegan:
                self.product.set_vegan(self.vegan.get())
            if self.vegetarian.get() != self.product.vegetarian:
                self.product.set_vegetarian(self.vegetarian.get)
            if self.gluten_free.get() != self.product.gluten_free:
                self.product.set_gluten_free(self.gluten_free.get())
        else:
            self.app.hrms.add_product(Product(
                self.app.hrms,
                name=product_name,
                vegan=self.vegan.get(),
                vegetarian=self.vegetarian.get(),
                gluten_free=self.gluten_free.get()
            ))

        messagebox.showinfo("Success", "Product details saved successfully.")
        self.parent.refresh()
        self.destroy()
