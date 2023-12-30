from orm.db import session
from orm.entities.table import TableEntity

class Table:
    """Pass either table_entity to create a Table from TableEntity or all other parameters to create an entirely new Table"""
    def __init__(self, number=None, capacity=None, table_entity: TableEntity = None):
        if table_entity:
            self.__entity = table_entity
        else:
            self.__entity = TableEntity(
                number=number,
                capacity=capacity
            )
            session.add(self.__entity)
            session.commit()
        
        self.__id = self.__entity.id
        self.number = self.__entity.number
        self.capacity = self.__entity.capacity

    def delete(self):
        session.delete(self.__entity)
        session.commit()
