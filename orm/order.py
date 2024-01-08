# @d2-zhmurenko
from datetime import datetime
from sqlalchemy.sql import select
from orm.db import session
from orm.entities.entities import Order as OrderEntity, OrderMenu as OrderMenuEntity

class Order:
    def __init__(self, hrms, user=None, table=None, promocode=None, order_entity: OrderEntity=None):
        self.__hrms = hrms

        if order_entity:
            self.__entity = order_entity
        else:
            self.__entity = OrderEntity(
                user_id=user.id if user else None,
                table_id=table.id,
                promocode_id=promocode.id if promocode else None,
                created_at=datetime.now()
            )
            session.add(self.__entity)
            session.commit()

        self.id = self.__entity.id
        self.__user_id = self.__entity.user_id
        self.__table_id = self.__entity.table_id
        self.__promocode_id = self.__entity.promocode_id
        self.created_at = self.__entity.created_at
        self.complete_at = self.__entity.complete_at

    def set_complete(self):
        self.complete_at = datetime.now()
        self.__entity.complete_at = self.complete_at
        session.commit()

    def set_promocode(self, promocode):
        self.__promocode_id = promocode.id
        self.__entity.promocode_id = promocode.id
        session.commit()

    def get_user(self):
        if not self.__user_id:
            return None
        return self.__hrms.get_user(id = self.__user_id)

    def get_table(self):
        return next(table for table in self.__hrms.__tables__ if table.id == self.__table_id)
    
    def get_promocode(self):
        if not self.__promocode_id:
            return None
        return self.__hrms.get_promocode(self.__promocode_id)
    
    def get_menu_items(self):
        stmt = select([OrderMenuEntity]).where(OrderMenuEntity.order_id == self.id)
        result = session.execute(stmt)
        return [(self.__hrms.get_menu_item(row[0].menu_id), row[0].quantity) for row in result]
    
    def delete(self):
        session.delete(self.__entity)
        session.commit()

    def add_menu_item(self, menu_item, quantity):
        session.add(OrderMenuEntity(
            order_id=self.id,
            menu_id=menu_item.id,
            quantity=quantity
        ))
        session.commit()

    def set_menu_item_quantity(self, menu_item, new_quantity):
        stmt = select([OrderMenuEntity]).where(OrderMenuEntity.order_id == self.id, OrderMenuEntity.menu_id == menu_item.id)
        result = session.execute(stmt).first()
        if result:
            order_menu = result[0]
            order_menu.quantity = new_quantity
            session.commit()

    def delete_menu_item(self, menu_item):
        stmt = select([OrderMenuEntity]).where(OrderMenuEntity.order_id == self.id, OrderMenuEntity.menu_id == menu_item.id)
        result = session.execute(stmt).first()
        if result:
            session.delete(result[0])
            session.commit()