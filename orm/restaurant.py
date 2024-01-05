from orm.db import session
from orm.entities.entities import Restaurant as RestaurantEntity
from orm.table import Table

class Restaurant:
    '''Pass either restaurant_entity to create a Restaurant from RestaurantEntity or all other parameters to create an entirely new Restaurant'''
    def __init__(self, hrms, city = None, restaurant_entity: RestaurantEntity = None):
        self.__hrms = hrms

        if restaurant_entity:
            self.__entity = restaurant_entity
        else: 
            self.__entity = RestaurantEntity(
                city=city
            )
            session.add(self.__entity)
            session.commit()
        
        self.id = self.__entity.id
        self.city = self.__entity.city

    def delete(self):
        session.delete(self.__entity)
        session.commit()

    def get_tables(self):
        return list(filter(lambda t, restaurant=self: t.get_restaurant() == restaurant, self.__hrms.__tables__))
    
    def get_table(self, id):
        return next(table for table in self.get_tables() if table.id == id)

    def add_table(self, table: Table):
        self.__hrms.__tables__.append(table)

    def delete_table(self, table: Table):
        table.delete() 
        self.__hrms.__tables__.remove(table)

    def get_orders(self):
        orders = []
        for table in self.get_tables():
            orders.extend(table.get_orders())
        return orders
    
    def get_deliveries(self):
        return list(filter(lambda d, restaurant=self: d.get_restaurant() == restaurant, self.__hrms.__deliveries__))
    
    def add_delivery(self, delivery):
        self.__hrms.__deliveries__.append(delivery)

    def delete_delivery(self, delivery):
        delivery.delete()
        self.__hrms.__deliveries__.remove(delivery)