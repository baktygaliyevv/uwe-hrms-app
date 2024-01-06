from orm.db import session
from orm.entities.entities import Restaurant as RestaurantEntity
from orm.table import Table
from orm.restaurant_product import RestaurantProduct

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

    def get_products(self):
        """Return a list of product dictionaries with id, name, and count."""
        return [
            {
                'id': rp.product_id,
                'name': rp.product.name,
                'count': rp.count
            }
            for rp in self.restaurant_products
        ]
    
    def get_unavailable_items(self):
        """Return a list of unavailable items with reasons."""
        return [
            {'name': rp.product.name, 'reason': 'Out of stock'}
            for rp in self.restaurant_products if rp.count == 0
        ]