from orm.db import session
from orm.entities.restaurant import RestaurantEntity

class Restaurant:
    '''Pass either restaurant_entity to create a Restaurant from RestaurantEntity or all other parameters to create an entirely new Restaurant'''
    def __init__(self, city = None, restaurant_entity: RestaurantEntity = None):
        if restaurant_entity:
            self.__entity = restaurant_entity
        else: 
            self.__entity = RestaurantEntity(
                city=city
            )
            session.add(self.__entity)
            session.commit()
        
        self.__id = self.__entity.id
        self.city = self.__entity.city

    def delete(self):
        session.delete(self.__entity)
        session.commit()