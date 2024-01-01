from datetime import date 
from orm.db import session
from orm.entities.promocode import Promocode as PromocodeEntity

class Promocode:
    '''Pass either promocode_entity to create a Promocode from PromocodeEntity or all other parameters to create an entirely new Promocode'''
    def __init__(self, id = None, discount = None, valid_till = None, promocode_entity: PromocodeEntity = None):
        if promocode_entity:
            self.__entity = promocode_entity
        else: 
            self.__entity = PromocodeEntity(
                id=id,
                discount=discount,
                valid_till=valid_till
            )
            session.add(self.__entity)
            session.commit()
        
        self.id = self.__entity.id
        self.discount = self.__entity.discount
        self.valid_till = self.__entity.valid_till

    def set_discount(self, discount):
        self.discount = discount
        self.__entity.discount = discount
        session.commit()

    def set_valid_till(self, valid_till):
        self.valid_till = valid_till
        self.__entity.valid_till = valid_till
        session.commit()

    def delete(self):
        session.delete(self.__entity)
        session.commit()

    def is_valid(self):
        return date.today() <= self.valid_till