import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
from orm.order import Order

def calculate_subtotal(menu_items):
    sm = 0
    for item, quantity in menu_items:
        sm += item.price * quantity
    return sm

def generate_bill(order: Order):
    if order.complete_at is None:
        return False

    filename = f"Order_{order.id}_Bill_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    file_path = os.path.join(os.getcwd(), filename)

    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    c.drawString(100, height - 100, f"Order #{order.id}")

    user = order.get_user()
    promocode = order.get_promocode()
    c.drawString(100, height - 120, "Placed by " + f'{user.first_name} {user.last_name}' if user else 'Guest')
    c.drawString(100, height - 140, f"Table: {order.get_table().id}")
    if promocode:
        c.drawString(100, height - 160, f"Promocode: {promocode.id}")

    menu_items = order.get_menu_items()

    y_position = height - 200
    for item, quantity in menu_items:
        c.drawString(100, y_position, f"{quantity} - {item.name} ({item.price}£) - {item.price * quantity}£")
        y_position -= 20

    subtotal = calculate_subtotal(menu_items)
    total = subtotal * (1 - (promocode.discount / 100)) if promocode else subtotal
    c.drawString(100, y_position - 20, f'Subtotal: {subtotal}£')
    c.drawString(100, y_position - 40, f'Total: {total}£ ' + f' ({promocode.id} applied)' if promocode else '')

    c.save()
    os.system(f"open '{file_path}'")

    return True