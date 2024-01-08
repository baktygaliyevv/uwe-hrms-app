# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table as STable, Text, text
from sqlalchemy.dialects.mysql import ENUM, TEXT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class MenuCategory(Base):
    __tablename__ = 'menu_categories'

    id = Column(Integer, primary_key=True)
    name = Column(Text(collation='utf8mb3_unicode_ci'), nullable=False)


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(50, 'utf8mb3_unicode_ci'), nullable=False)
    vegan = Column(TINYINT(1), nullable=False)
    vegetarian = Column(TINYINT(1), nullable=False)
    gluten_free = Column(TINYINT(1), nullable=False)


class Promocode(Base):
    __tablename__ = 'promocodes'

    id = Column(String(50, 'utf8mb3_unicode_ci'), primary_key=True)
    discount = Column(Integer, nullable=False)
    valid_till = Column(DateTime, nullable=False)


class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    city = Column(String(50, 'utf8mb3_unicode_ci'), nullable=False)

    restaurant_products = relationship("RestaurantProduct", back_populates="restaurant")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(TEXT, nullable=False)
    last_name = Column(Text(collation='utf8mb3_unicode_ci'), nullable=False)
    phone = Column(VARCHAR(10), nullable=False)
    hash = Column(VARCHAR(64))
    salt = Column(String(32, 'utf8mb3_unicode_ci'))
    role = Column(ENUM('admin', 'manager', 'chef', 'staff', 'courier', 'client'), nullable=False, server_default=text("'client'"))


class Delivery(Base):
    __tablename__ = 'deliveries'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    restaurant_id = Column(ForeignKey('restaurants.id'), nullable=False, index=True)
    promocode_id = Column(ForeignKey('promocodes.id'), index=True)
    address = Column(Text(collation='utf8mb3_unicode_ci'), nullable=False)
    created_at = Column(DateTime, nullable=False)
    status = Column(ENUM('new', 'delivering', 'complete'), nullable=False)

    promocode = relationship('Promocode')
    restaurant = relationship('Restaurant')
    user = relationship('User')


class Menu(Base):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True)
    menu_category_id = Column(ForeignKey('menu_categories.id'), nullable=False, index=True)
    name = Column(Text(collation='utf8mb3_unicode_ci'), nullable=False)
    price = Column(Integer, nullable=False)

    menu_category = relationship('MenuCategory')
    products = relationship('Product', secondary='menu_products')


class RestaurantProduct(Base):
    __tablename__ = 'restaurant_products'

    id = Column(Integer, primary_key=True)
    restaurant_id = Column(ForeignKey('restaurants.id'), nullable=False, index=True)
    product_id = Column(ForeignKey('products.id'), nullable=False, index=True)
    count = Column(Integer, nullable=False)

    product = relationship('Product')
    restaurant = relationship('Restaurant')


class Table(Base):
    __tablename__ = 'tables'

    id = Column(Integer, primary_key=True)
    restaurant_id = Column(ForeignKey('restaurants.id'), nullable=False, index=True)
    capacity = Column(Integer, nullable=False)

    restaurant = relationship('Restaurant')


class UserToken(Base):
    __tablename__ = 'user_tokens'

    token = Column(String(64, 'utf8mb3_unicode_ci'), primary_key=True)
    user_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    expiration_date = Column(DateTime, nullable=False)

    user = relationship('User')


class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    table_id = Column(ForeignKey('tables.id'), nullable=False, index=True)
    persons = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    comment = Column(TEXT)

    table = relationship('Table')
    user = relationship('User')


class DeliveryMenu(Base):
    __tablename__ = 'delivery_menu'

    id = Column(Integer, primary_key=True)
    delivery_id = Column(ForeignKey('deliveries.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    menu_id = Column(ForeignKey('menu.id'), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)

    delivery = relationship('Delivery')
    menu = relationship('Menu')


t_menu_products = STable(
    'menu_products', metadata,
    Column('menu_id', ForeignKey('menu.id'), nullable=False, index=True),
    Column('product_id', ForeignKey('products.id'), nullable=False, index=True)
)


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('users.id'), index=True)
    table_id = Column(ForeignKey('tables.id'), nullable=False, index=True)
    promocode_id = Column(ForeignKey('promocodes.id'), index=True)
    created_at = Column(DateTime, nullable=False)
    complete_at = Column(DateTime)

    promocode = relationship('Promocode')
    table = relationship('Table')
    user = relationship('User')


class OrderMenu(Base):
    __tablename__ = 'order_menu'

    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey('orders.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    menu_id = Column(ForeignKey('menu.id'), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)

    menu = relationship('Menu')
    order = relationship('Order')
