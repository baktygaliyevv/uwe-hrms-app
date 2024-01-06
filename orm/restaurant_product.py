from orm.db import session
from orm.entities.entities import RestaurantProduct as RestaurantProductEntity

class RestaurantProduct:
    """Class to interact with RestaurantProduct entities."""
    def __init__(self, hrms, product=None, restaurant=None, count=None, restaurant_product_entity: RestaurantProductEntity = None):
        self.__hrms = hrms

        if restaurant_product_entity:
            self.__entity = restaurant_product_entity
        else:
            self.__entity = RestaurantProductEntity(
                product_id=product.id,
                restaurant_id=restaurant.id,
                count=count
            )
            session.add(self.__entity)
            session.commit()

        self.id = self.__entity.id
        self.product_id = self.__entity.product_id
        self.restaurant_id = self.__entity.restaurant_id
        self.count = self.__entity.count

    def increment_count(self, amount=1):
        self.count += amount
        self.__entity.count = self.count
        session.commit()

    def decrement_count(self, amount=1):
        if self.count >= amount:
            self.count -= amount
            self.__entity.count = self.count
            session.commit()
        else:
            raise ValueError("Not enough stock to decrement.")

    def delete(self):
        session.delete(self.__entity)
        session.commit()

