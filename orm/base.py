from sqlalchemy import select
from orm.db import session

from orm.user import User
from orm.entities.user import UserEntity
from orm.restaurant import Restaurant
from orm.entities.restaurant import RestaurantEntity
from orm.promocode import Promocode
from orm.entities.promocode import Promocode as PromocodeEntity

class HRMS:
    users: list[User] = []
    restaurants: list[Restaurant] = []
    promocodes: list[Promocode] = []

    def __init__(self):
        self.users = [User(user_entity=user_entity) for user_entity in session.scalars(select(UserEntity))]
        self.restaurants = [Restaurant(restaurant_entity=restaurant_entity) for restaurant_entity in session.scalars(select(RestaurantEntity))]
        self.promocodes = [Promocode(promocode_entity=promocode_entity) for promocode_entity in session.scalars(select(PromocodeEntity))]

    def find_user(self, phone):
        return next(user for user in self.users if user.phone == phone)

    def add_user(self, user: User):
        self.users.append(user)
        
    def delete_user(self, user: User):
        user.delete()
        self.users.remove(user)

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
