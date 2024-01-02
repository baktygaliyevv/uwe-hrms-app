from sqlalchemy import select
from sqlalchemy.orm import selectinload
from orm.db import session
from orm.entities.entities import User as UserEntity, Restaurant as RestaurantEntity, Table as TableEntity, Promocode as PromocodeEntity, Product as ProductEntity

from orm.user import User
from orm.restaurant import Restaurant
from orm.table import Table
from orm.promocode import Promocode
from orm.product import Product 

class HRMS:
    users: list[User] = []
    restaurants: list[Restaurant] = []
    promocodes: list[Promocode] = []

    products: list[Product] = []

    __tables__: list[Table] = []

    def __init__(self):
        self.users = [User(self, user_entity=user_entity) for user_entity in session.scalars(select(UserEntity))]
        self.restaurants = [Restaurant(self, restaurant_entity=restaurant_entity) for restaurant_entity in session.scalars(select(RestaurantEntity))]
        self.promocodes = [Promocode(self, promocode_entity=promocode_entity) for promocode_entity in session.scalars(select(PromocodeEntity))]

        self.products = [Product(product_entity=product_entity) for product_entity in session.scalars(select(ProductEntity))]

        self.__tables__ = [Table(self, table_entity=table_entity) for table_entity in session.scalars(select(TableEntity))]

    def get_user(self, id = None, phone = None):
        if id:
            return next(user for user in self.users if user.id == id)
        if phone:
            return next(user for user in self.users if user.phone == phone)

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

    def find_promocode(self, id):
        return next(promocode for promocode in self.promocodes if promocode.id == id)
    
    def add_promocode(self, promocode: Promocode):
        self.promocodes.append(promocode)

    def delete_promocode(self, promocode: Promocode):
        promocode.delete()
        self.promocodes.remove(promocode)
        
    def find_product(self, id):
        return next(product for product in self.products if product.id == id)
    
    def add_product(self, product: Product):
        self.products.append(product)
        
    def update_product(self, product: Product, data: dict):
        product.set_name(data['name'])
        product.set_is_vegan(data['vegan'])
        product.set_is_vegetarian(data['vegetarian'])
        product.set_is_gluten_free(data['gluten_free'])

    def delete_product(self, product: Product):
        product.delete()
        self.products.remove(product)