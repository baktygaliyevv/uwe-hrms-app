from sqlalchemy import select
from orm.db import session

from orm.user import User
from orm.entities.user import UserEntity
from orm.restaurant import Restaurant
from orm.entities.restaurant import RestaurantEntity

class HRMS:
    users: list[User] = []
    restaurants: list[Restaurant] = []

    def __init__(self):
        self.users = [User(user_entity=user_entity) for user_entity in session.scalars(select(UserEntity))]
        self.restaurants = [Restaurant(restaurant_entity=restaurant_entity) for restaurant_entity in session.scalars(select(RestaurantEntity))]

    def find_user(self, phone):
        return next(user for user in self.users if user.phone == phone)

    def add_user(self, user: User):
        self.users.append(user)
        
    def delete_user(self, user: User):
        user.delete()
        session.commit()
        self.users.remove(user)

    def add_restaurant(self, restaurant: Restaurant):
        self.restaurants.append(restaurant)

    def delete_restaurant(self, restaurant: Restaurant):
        restaurant.delete()
        session.commit()
        self.restaurants.remove(restaurant)
