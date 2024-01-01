from sqlalchemy import select
from sqlalchemy.orm import selectinload
from orm.db import session
from orm.entities.entities import User as UserEntity, Restaurant as RestaurantEntity, Table as TableEntity

from orm.user import User
from orm.restaurant import Restaurant
from orm.table import Table

class HRMS:
    users: list[User] = []
    restaurants: list[Restaurant] = []
    tables: list[Table] = []

    def __init__(self):
        self.users = [User(user_entity=user_entity) for user_entity in session.scalars(select(UserEntity))]
        self.restaurants = [Restaurant(restaurant_entity=restaurant_entity) for restaurant_entity in session.scalars(select(RestaurantEntity))]
        self.tables = [Table(table_entity=table_entity) for table_entity in session.scalars(select(TableEntity))]
 
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

    def add_table(self, table: Table):
        session.add(table.entity)
        session.commit()

    def delete_table(self, table: Table):
        table.delete() 
        self.tables.remove(table)

    def reload_tables(self):
        self.tables = [Table(table_entity=table_entity) for table_entity in session.query(TableEntity).options(selectinload(TableEntity.restaurant)).all()]