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
        
    # def delete_user(self, user: User):
    #     self.users.remove(user)
    def delete_user(self, user_phone):
        user_to_remove = None
        for user in self.users:
            if user.phone == user_phone:
                user_to_remove = user
                break
        if user_to_remove:
            self.users.remove(user_to_remove)
            session.delete(user_to_remove.__entity)
            session.commit()
