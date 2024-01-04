from orm.db import session
from orm.entities.entities import Table as TableEntity
from orm.booking import Booking

class Table:
    """Pass either table_entity to create a Table from TableEntity or all other parameters to create an entirely new Table"""
    def __init__(self, hrms, capacity = None, restaurant = None, table_entity: TableEntity = None):
        self.__hrms = hrms

        if table_entity:
            self.__entity = table_entity
        else:
            self.__entity = TableEntity(
                capacity=capacity,
                restaurant_id=restaurant.id
            )
            session.add(self.__entity)
            session.commit()
        
        self.id = self.__entity.id
        self.capacity = self.__entity.capacity
        self.__restaurant_id = self.__entity.restaurant_id

    def get_restaurant(self):
        return self.__hrms.get_restaurant(self.__restaurant_id)

    def delete(self):
        session.delete(self.__entity)
        session.commit()

    def get_bookings(self):
        return list(filter(lambda b, table=self: b.get_table() == table, self.__hrms.__bookings__))

    def add_booking(self, booking: Booking):
        self.__hrms.__bookings__.append(booking)

    def delete_booking(self, booking: Booking):
        booking.delete() 
        self.__hrms.__bookings__.remove(booking)

