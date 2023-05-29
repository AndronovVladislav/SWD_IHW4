from sqlalchemy import select

class MenuSelector:
    def __init__(self, db):
        self.__dishes = db.dishes
        self.__engine = db.engine

        self.__error_message = 'Error code: 404 - Not found<br>'
        self.__error_code = 404

    def get_menu(self):
        with self.__engine.connect() as connection:
            connection.begin()

            response = list()
            for position in connection.execute(select(self.__dishes.c.name,
                                                      self.__dishes.c.description,
                                                      self.__dishes.c.price)
                                               .where(self.__dishes.c.is_available == True))\
                                            .fetchall():
                response.append({'name' : position.name,
                                 'description' : position.description,
                                 'price' : position.price
                                })

            return response

    def make_error(self, error_description):
        return (self.__error_message + error_description, self.__error_code)