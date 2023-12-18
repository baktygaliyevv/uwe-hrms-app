from sqlalchemy import select
from orm.db import sessionFactory

from orm.user import User
from orm.entities.user import UserEntity

class HRMS:
    users = []

    def __init__(self):
        with sessionFactory() as session:
            self.users = [User(user_entity=user_entity) for user_entity in session.scalars(select(UserEntity))]

    def find_user(self, phone):
        return next(user for user in self.users if user.phone == phone)

    def add_user(self, user: User):
        self.users.append(user)
    