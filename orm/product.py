# @n2-baktygaliye @y2-bugenov @d2-zhmurenko
from datetime import date
from orm.db import session
from orm.entities.entities import Product as ProductEntity

class Product:
    def __init__(self, hrms, id=None, name=None, vegan=False, vegetarian=False, gluten_free=False, product_entity: ProductEntity=None):
        if product_entity:
            self.__entity = product_entity
        else:
            self.__entity = ProductEntity(
                id=id,
                name=name,
                vegan=vegan,
                vegetarian=vegetarian,
                gluten_free=gluten_free
            )
            session.add(self.__entity)
            session.commit()

        self.id = self.__entity.id
        self.name = self.__entity.name
        self.vegan = self.__entity.vegan
        self.vegetarian = self.__entity.vegetarian
        self.gluten_free = self.__entity.gluten_free

    def set_vegan(self, vegan):
        self.vegan = vegan
        self.__entity.vegan = vegan
        session.commit()

    def set_vegetarian(self, vegetarian):
        self.vegetarian = vegetarian
        self.__entity.vegetarian = vegetarian
        session.commit()

    def set_gluten_free(self, gluten_free):
        self.gluten_free = gluten_free
        self.__entity.gluten_free = gluten_free
        session.commit()

    def delete(self):
        session.delete(self.__entity)
        session.commit()

    def increment_count(self, amount=1):
        self.count += amount
        self.save()

    def decrement_count(self, amount=1):
        if self.count >= amount:
            self.count -= amount
            self.save()
        else:
            raise ValueError("Not enough stock to decrement.")

    def save(self):
        session.commit()
