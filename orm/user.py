from orm.db import session
from orm.entities.entities import User as UserEntity
from utils.random_string import get_random_string
from utils.hash_password import hash_password

class User:
    '''Pass either user_entity to create a User from UserEntity or all other parameters to create an entirely new User'''
    def __init__(self, first_name=None, last_name=None, phone=None, password=None, role=None, user_entity=None):
        if user_entity:
            self.__entity = user_entity
        else:
            salt = get_random_string(32)
            hash = hash_password(password, salt)
            self.__entity = UserEntity(
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                hash=hash,
                salt=salt,
                role=role
            )
            session.add(self.__entity)
            session.commit()

        self.__id = self.__entity.id
        self.first_name = self.__entity.first_name
        self.last_name = self.__entity.last_name
        self.phone = self.__entity.phone
        self.__hash = self.__entity.hash
        self.__salt = self.__entity.salt
        self.role = self.__entity.role

    def set_name(self, first_name=None, last_name=None):
        if first_name:
            self.first_name = first_name
            self.__entity.first_name = first_name
            session.commit()
        if last_name:
            self.last_name = last_name
            self.__entity.last_name = last_name
            session.commit()

    def set_phone(self, phone):
        self.phone = phone
        self.__entity.phone = phone
        session.commit()

    def set_password(self, password):
        salt = get_random_string(32)
        hash = hash_password(password, salt)
        self.__hash = hash
        self.__salt = salt
        self.__entity.hash = hash
        self.__entity.salt = salt
        session.commit()
    
    def set_role(self, role):
        self.role = role
        self.__entity.role = role
        session.commit()

    
    def check_password(self, password):
        hash = hash_password(password, self.__salt)
        return hash == self.__hash
    

    def delete(self):
        session.delete(self.__entity)
        session.commit()