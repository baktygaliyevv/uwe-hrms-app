from orm.db import session
from orm.entities.entities import Restaurant as RestaurantEntity, RestaurantProduct as RestaurantProductEntity
from orm.table import Table

class Restaurant:
    '''Pass either restaurant_entity to create a Restaurant from RestaurantEntity or all other parameters to create an entirely new Restaurant'''
    def __init__(self, hrms, city = None, restaurant_entity: RestaurantEntity = None):
        self.__hrms = hrms

        if restaurant_entity:
            self.__entity = restaurant_entity
        else: 
            self.__entity = RestaurantEntity(
                city=city
            )
            session.add(self.__entity)
            session.commit()
        
        self.id = self.__entity.id
        self.city = self.__entity.city

    def delete(self):
        session.delete(self.__entity)
        session.commit()

    def get_tables(self):
        return list(filter(lambda t, restaurant=self: t.get_restaurant() == restaurant, self.__hrms.__tables__))
    
    def get_table(self, id):
        return next(table for table in self.get_tables() if table.id == id)

    def add_table(self, table: Table):
        self.__hrms.__tables__.append(table)

    def delete_table(self, table: Table):
        table.delete() 
        self.__hrms.__tables__.remove(table)

    def get_products(self):
        """Return a list of tuples with product id and count."""
        return list(map(
            lambda p: (p, next((rp.count for rp in self.__entity.restaurant_products if rp.product_id == p.id), 0)),
            self.__hrms.products
        ))

    def get_product(self, product_id):
        return next(p for p in self.get_products() if p[0].id == product_id)

    def get_unavailable_menu_items(self):
        """Return a list of unavailable items with reasons."""
        unavailable_products = [product for product, count in self.get_products() if count == 0]
        unavailable_menu_items = dict()
        for item in self.__hrms.menu_items:
            menu_products = item.get_products()
            for product in menu_products:
                if product in unavailable_products:
                    if item in unavailable_menu_items:
                        unavailable_menu_items[item].append(product)
                    else:
                        unavailable_menu_items[item] = [product]
        return [(k, v) for k, v in unavailable_menu_items.items()]
    
    def add_product(self, product, count):
        """Add a product to the restaurant."""
        restaurant_product = session.query(RestaurantProductEntity).filter_by(restaurant_id=self.id, product_id=product.id).first()
        if restaurant_product:
            restaurant_product.count += count
        else:
            restaurant_product = RestaurantProductEntity(
                product_id=product.id,
                restaurant_id=self.id,
                count=count
            )
            session.add(restaurant_product)
        session.commit()

    def remove_product(self, product):
        """Remove a product from the restaurant."""
        restaurant_product = session.query(RestaurantProductEntity).filter_by(restaurant_id=self.id, product_id=product.id).first()
        if restaurant_product:
            session.delete(restaurant_product)
            session.commit()

    def update_product_count(self, product, new_count):
        restaurant_product = session.query(RestaurantProductEntity).filter_by(restaurant_id=self.id, product_id=product.id).first()

        if restaurant_product:
            restaurant_product.count = new_count
            session.commit()
        else:
            new_restaurant_product = RestaurantProductEntity(restaurant_id=self.id, product_id=product.id, count=new_count)
            session.add(new_restaurant_product)
            session.commit()

    def get_orders(self):
        orders = []
        for table in self.get_tables():
            orders.extend(table.get_orders())
        return orders
    
    def get_bookings(self):
        bookings = []
        for table in self.get_tables():
            bookings.extend(table.get_bookings())
        return bookings
    
    def get_deliveries(self):
        return list(filter(lambda d, restaurant=self: d.get_restaurant() == restaurant, self.__hrms.__deliveries__))
    
    def add_delivery(self, delivery):
        self.__hrms.__deliveries__.append(delivery)

    def delete_delivery(self, delivery):
        delivery.delete()
        self.__hrms.__deliveries__.remove(delivery)

