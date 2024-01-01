from orm.db import session
from orm.entities.entities import Restaurant as RestaurantEntity

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
        
    @property
    def id(self):
        return self.__entity.id

    def delete(self):
        session.delete(self.__entity)
        session.commit()