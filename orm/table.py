from orm.db import session
from orm.entities.entities import Table as TableEntity

class Table:
    """Pass either table_entity to create a Table from TableEntity or all other parameters to create an entirely new Table"""
    def __init__(self, id=None, capacity=None, restaurant_id=None, table_entity: TableEntity = None):
        if table_entity:
            self.entity = table_entity
        else:
            self.entity = TableEntity(
                id=id,
                capacity=capacity,
                restaurant_id=restaurant_id
            )
            session.add(self.entity)
            session.commit()
        
        self.id = self.entity.id
        self.capacity = self.entity.capacity
        self.restaurant_id = self.entity.restaurant_id

    def delete(self):
        session.delete(self.entity)
        session.commit()
