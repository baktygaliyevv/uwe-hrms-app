# @d2-zhmurenko
from sqlalchemy.sql import select
from orm.db import session
from orm.entities.entities import Menu as MenuEntity, t_menu_products

class MenuItem:
    """Create a Menu either from a MenuEntity or new parameters."""
    def __init__(self, hrms, name=None, price=None, menu_category=None, menu_entity: MenuEntity = None):
        self.__hrms = hrms

        if menu_entity:
            self.__entity = menu_entity
        else:
            self.__entity = MenuEntity(
                name=name,
                price=price,
                menu_category_id=menu_category.id
            )
            session.add(self.__entity)
            session.commit()

        self.id = self.__entity.id
        self.name = self.__entity.name
        self.price = self.__entity.price
        self.__menu_category_id = self.__entity.menu_category_id

    def get_menu_category(self):
        return self.__hrms.get_menu_category(self.__menu_category_id)
    
    def set_menu_category(self, menu_category):
        self.__menu_category_id = menu_category.id
        self.__entity.menu_category_id = menu_category.id
        session.commit()
    
    def get_products(self):
        stmt = select([t_menu_products.c.product_id]).where(t_menu_products.c.menu_id == self.id)
        result = session.execute(stmt)
        product_ids = [row[0] for row in result]
        return [self.__hrms.get_product(product_id) for product_id in product_ids]

    def set_price(self, price):
        self.price = price
        self.__entity.price = price
        session.commit()

    def delete(self):
        session.delete(self.__entity)
        session.commit()

    def add_product(self, product):
        stmt = t_menu_products.insert().values(menu_id=self.id, product_id=product.id)
        session.execute(stmt)
        session.commit()

    def remove_product(self, product):
        stmt = t_menu_products.delete().where(t_menu_products.c.menu_id == self.id, t_menu_products.c.product_id == product.id)
        session.execute(stmt)
        session.commit()