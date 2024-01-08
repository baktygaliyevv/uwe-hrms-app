# @d2-zhmurenko
from datetime import datetime
from sqlalchemy.sql import select
from orm.db import session
from orm.entities.entities import Delivery as DeliveryEntity, DeliveryMenu as DeliveryMenuEntity

class Delivery:
    def __init__(self, hrms, user=None, restaurant=None, promocode=None, address=None, delivery_entity: DeliveryEntity=None):
        self.__hrms = hrms

        if delivery_entity:
            self.__entity = delivery_entity
        else:
            self.__entity = DeliveryEntity(
                user_id=user.id,
                restaurant_id=restaurant.id,
                promocode_id=promocode.id if promocode else None,
                address=address,
                created_at=datetime.now(),
                status='new'
            )
            session.add(self.__entity)
            session.commit()

        self.id = self.__entity.id
        self.__user_id = self.__entity.user_id
        self.__restaurant_id = self.__entity.restaurant_id
        self.__promocode_id = self.__entity.promocode_id
        self.address = self.__entity.address
        self.created_at = self.__entity.created_at
        self.status = self.__entity.status

    def set_status(self, status):
        self.status = status
        self.__entity.status = status
        session.commit()

    def set_promocode(self, promocode):
        self.__promocode_id = promocode.id
        self.__entity.promocode_id = promocode.id
        session.commit()

    def get_user(self):
        return self.__hrms.get_user(id = self.__user_id)

    def get_restaurant(self):
        return self.__hrms.get_restaurant(id = self.__restaurant_id)
    
    def get_promocode(self):
        if not self.__promocode_id:
            return None
        return self.__hrms.get_promocode(self.__promocode_id)
    
    def get_menu_items(self):
        stmt = select([DeliveryMenuEntity]).where(DeliveryMenuEntity.delivery_id == self.id)
        result = session.execute(stmt)
        return [(self.__hrms.get_menu_item(row[0].menu_id), row[0].quantity) for row in result]
    
    def delete(self):
        session.delete(self.__entity)
        session.commit()

    def add_menu_item(self, menu_item, quantity):
        session.add(DeliveryMenuEntity(
            delivery_id=self.id,
            menu_id=menu_item.id,
            quantity=quantity
        ))
        session.commit()

    def set_menu_item_quantity(self, menu_item, new_quantity):
        stmt = select([DeliveryMenuEntity]).where(DeliveryMenuEntity.delivery_id == self.id, DeliveryMenuEntity.menu_id == menu_item.id)
        result = session.execute(stmt).first()
        if result:
            order_menu = result[0]
            order_menu.quantity = new_quantity
            session.commit()

    def delete_menu_item(self, menu_item):
        stmt = select([DeliveryMenuEntity]).where(DeliveryMenuEntity.delivery_id == self.id, DeliveryMenuEntity.menu_id == menu_item.id)
        result = session.execute(stmt).first()
        if result:
            session.delete(result[0])
            session.commit()