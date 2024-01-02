from datetime import date
from orm.db import session
from orm.entities.entities import Product as ProductEntity

class Product:
    def __init__(self, id=None, name=None, vegan=False, vegetarian=False, gluten_free=False, product_entity: ProductEntity=None):
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

    def add_product(cls, name, vegan, vegetarian, gluten_free):
        product = ProductEntity(
            name=name,
            vegan=vegan,
            vegetarian=vegetarian,
            gluten_free=gluten_free
        )
        session.add(product)
        session.commit()
        return cls(product_entity=product)
    def set_name(self, name):
        self.name = name
        self.__entity.name = name
        session.commit()

    def set_is_vegan(self, vegan):
        self.vegan = vegan
        self.__entity.vegan = vegan
        session.commit()

    def set_is_vegetarian(self, vegetarian):
        self.vegetarian = vegetarian
        self.__entity.vegetarian = vegetarian
        session.commit()

    def set_is_gluten_free(self, gluten_free):
        self.gluten_free = gluten_free
        self.__entity.gluten_free = gluten_free
        session.commit()

    def delete(self):
        session.delete(self.__entity)
        session.commit()