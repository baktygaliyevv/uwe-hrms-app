# @d2-zhmurenko
from orm.db import session
from orm.entities.entities import MenuCategory as MenuCategoryEntity

class MenuCategory:
    """Create a MenuCategory from a MenuCategoryEntity or new parameters."""
    def __init__(self, hrms, name=None, menu_category_entity: MenuCategoryEntity = None):
        self.__hrms = hrms

        if menu_category_entity:
            self.__entity = menu_category_entity
        else:
            self.__entity = MenuCategoryEntity(name=name)
            session.add(self.__entity)
            session.commit()

        self.id = self.__entity.id
        self.name = self.__entity.name

    def list_menus(self):
        return self.__hrms.list_menus_by_category(self.id)

    def delete(self):
        session.delete(self.__entity)
        session.commit()
