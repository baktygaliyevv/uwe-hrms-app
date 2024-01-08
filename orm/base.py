# @d2-zhmurenko @n2-baktygaliye @y2-bugenov
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from orm.db import session

from orm.user import User, UserEntity
from orm.restaurant import Restaurant, RestaurantEntity
from orm.table import Table, TableEntity
from orm.promocode import Promocode, PromocodeEntity
from orm.product import Product, ProductEntity
from orm.booking import Booking, BookingEntity
from orm.menu_category import MenuCategory, MenuCategoryEntity
from orm.menu_item import MenuItem, MenuEntity
from orm.order import Order, OrderEntity
from orm.delivery import Delivery, DeliveryEntity   

class HRMS:
    users: list[User] = []
    restaurants: list[Restaurant] = []
    promocodes: list[Promocode] = []
    products: list[Product] = []
    menu_categories: list[MenuCategory] = []
    menu_items: list[MenuItem] = []

    __tables__: list[Table] = []
    __bookings__: list[Booking] = []
    __orders__: list[Order] = []
    __deliveries__: list[Delivery] = []

    def __init__(self):
        self.users = [User(self, user_entity=user_entity) for user_entity in session.scalars(select(UserEntity))]
        self.restaurants = [Restaurant(self, restaurant_entity=restaurant_entity) for restaurant_entity in session.scalars(select(RestaurantEntity))]
        self.promocodes = [Promocode(self, promocode_entity=promocode_entity) for promocode_entity in session.scalars(select(PromocodeEntity))]
        self.products = [Product(self, product_entity=product_entity) for product_entity in session.scalars(select(ProductEntity))]
        self.menu_categories = [MenuCategory(self, menu_category_entity=menu_category_entity) for menu_category_entity in session.scalars(select(MenuCategoryEntity))]
        self.menu_items = [MenuItem(self, menu_entity=menu_entity) for menu_entity in session.scalars(select(MenuEntity))]

        self.__tables__ = [Table(self, table_entity=table_entity) for table_entity in session.scalars(select(TableEntity))]
        self.__bookings__ = [Booking(self, booking_entity=booking_entity) for booking_entity in session.scalars(select(BookingEntity))]
        self.__orders__ = [Order(self, order_entity=order_entity) for order_entity in session.scalars(select(OrderEntity))]
        self.__deliveries__ = [Delivery(self, delivery_entity=delivery_entity) for delivery_entity in session.scalars(select(DeliveryEntity))]

    def get_user(self, id = None, phone = None):
        if id:
            return next((user for user in self.users if user.id == id), None)
        if phone:
            return next((user for user in self.users if user.phone == phone), None)

    def add_user(self, user: User):
        self.users.append(user)
        
    def delete_user(self, user: User):
        user.delete()
        self.users.remove(user)

    def get_restaurant(self, id = None, city = None):
        if id:
            return next(restaurant for restaurant in self.restaurants if restaurant.id == id)
        if city:
            return next(restaurant for restaurant in self.restaurants if restaurant.city == city)

    def add_restaurant(self, restaurant: Restaurant):
        self.restaurants.append(restaurant)

    def delete_restaurant(self, restaurant: Restaurant):
        restaurant.delete()
        self.restaurants.remove(restaurant)

    def get_promocode(self, id):
        return next(promocode for promocode in self.promocodes if promocode.id == id)
    
    def add_promocode(self, promocode: Promocode):
        self.promocodes.append(promocode)

    def delete_promocode(self, promocode: Promocode):
        promocode.delete()
        self.promocodes.remove(promocode)

    def get_product(self, id):
        return next(product for product in self.products if product.id == id)
    
    def add_product(self, product: Product):
        self.products.append(product)

    def delete_product(self, product: Product):
        product.delete()
        self.products.remove(product)

    def get_menu_category(self, id):
        return next(menu_category for menu_category in self.menu_categories if menu_category.id == id)
    
    def add_menu_category(self, menu_category):
        self.menu_categories.append(menu_category)

    def delete_menu_category(self, menu_category):
        menu_category.delete()
        self.menu_categories.remove(menu_category)

    def get_menu_item(self, id):
        return next(menu_item for menu_item in self.menu_items if menu_item.id == id)
    
    def add_menu_item(self, menu_item):
        self.menu_items.append(menu_item)

    def delete_menu_item(self, menu_item):
        menu_item.delete()
        self.menu_items.remove(menu_item)