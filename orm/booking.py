from orm.db import session
from orm.entities.entities import Booking as BookingEntity

class Booking:
    """Pass either booking_entity to create a Booking from BookingEntity or all other parameters to create an entirely new Booking"""
    def __init__(self, hrms, user = None, table = None, persons = None, date = None, comment = None, booking_entity: BookingEntity = None):
        self.__hrms = hrms

        if booking_entity:
            self.__entity = booking_entity
        else:
            self.__entity = BookingEntity(
                user_id = user.id,
                table_id = table.id,
                persons = persons, 
                date = date,
                comment = comment
            )
            session.add(self.__entity)
            session.commit()

        self.id = self.__entity.id
        self.__user_id = self.__entity.user_id
        self.__table_id = self.__entity.table_id
        self.persons = self.__entity.persons
        self.date = self.__entity.date
        self.comment = self.__entity.comment

    def get_user(self):
        return self.__hrms.get_user(id = self.__user_id)
    
    def get_table(self):
        return next(table for table in self.__hrms.__tables__ if table.id == self.__table_id)

    def set_persons(self, persons):
        self.persons = persons
        self.__entity.persons = persons
        session.commit()

    def set_date(self, date):
        self.date = date
        self.__entity.date = date
        session.commit()

    def set_comment(self, comment):
        self.comment = comment
        self.__entity.comment = comment
        session.commit()

    def delete(self):
        session.delete(self.__entity)
        session.commit()