from sqlalchemy import select
from orm.db import session

from orm.user import User
from orm.entities.user import UserEntity

class HRMS:
    users = []

    def __init__(self):
        self.users = [User(user_entity=user_entity) for user_entity in session.scalars(select(UserEntity))]

    def find_user(self, phone):
        return next(user for user in self.users if user.phone == phone)

    def add_user(self, user: User):
        self.users.append(user)
        
    def delete_user(self, user: User):
        session.delete(user.__entity)
        session.commit()
        self.users.remove(user)