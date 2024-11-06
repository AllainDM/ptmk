import psycopg2

import config


def connect_db():
    try:
        conn = psycopg2.connect(host=config.host,
                                user=config.user,
                                password=config.password,
                                database=config.db_name)
        return conn
    except psycopg2.OperationalError as e:
        print(f"Ошибка подключения к БД: {e}")


class FDataBase:
    def __init__(self):
        self.__conn = connect_db()
        self.__cursor = self.__conn.cursor()


    # Создание таблицы.
    def create_table(self):
        try:
            with self.__conn:
                self.__cursor.execute("DROP TABLE IF EXISTS staff")  # Удалим старую таблицу(для тестов)
                print("Старая таблица удалена (для тестов).")
                self.__cursor.execute('''
                    CREATE TABLE IF NOT EXISTS staff (
                        id SERIAL PRIMARY KEY,
                        fullname TEXT NOT NULL,
                        date_birth TEXT NOT NULL,                        
                        f_letter_name TEXT NOT NULL,                        
                        gender TEXT NOT NULL
                    )
                ''')
                print("Новая таблица создана.")
                print("Модуль FDataBase: таблица создана.")
                self.__conn.commit()
        except Exception as _ex:
            print("Ошибка создания таблицы в БД", _ex)
            return False


    # Добавление сотрудников списком.
    def add_staff_from_list(self, staff: list):
        try:
            with self.__conn:
                self.__cursor.executemany(
                    f"INSERT INTO staff(fullname, date_birth, gender) "
                    f"VALUES(%s, %s, %s)",
                    [(person[0], person[1], person[2]) for person in staff])
                self.__conn.commit()
                print(f"Модуль FDataBase: список сотрудников добавлен в БД.")
        except Exception as _ex:
            print("Ошибка добавления сотрудника в БД", _ex)
            return False

        return True

    def get_staff_all(self):
        try:
            query = (f"SELECT fullname, date_birth, gender "
                     f"FROM staff "
                     f"ORDER BY fullname")
            # Можно передать первый символ фамилии или пола, или их не передавать.
            with self.__conn:
                self.__cursor.execute(query)
                res = self.__cursor.fetchall()
                if not res:
                    print("Staff not found")
                    return False

            return res
        except Exception as _ex:
            print("Ошибка поиска сотрудников в БД", _ex)

        return False


    def get_staff(self, name="", gender=""):
        try:
            query = (f"SELECT fullname, date_birth, gender "
                     f"FROM staff "
                     f"WHERE SUBSTRING(fullname FROM 1 FOR 1) = %s AND gender = %s "
                     f"ORDER BY fullname")  # TODO Вернуть
            # Можно передать первый символ фамилии или пола, или их не передавать.
            parameter = (name, gender)
            with self.__conn:
                self.__cursor.execute(query, parameter)
                res = self.__cursor.fetchall()
                if not res:
                    print("Staff not found")
                    return False

            return res
        except Exception as _ex:
            print("Ошибка поиска сотрудников в БД", _ex)

        return False

    # Оптимизация БД.
    def optimize_db(self):
        try:
            with self.__conn:
                self.__cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_first_letter_fullname ON staff(SUBSTRING(fullname FROM 1 FOR 1))")
                self.__conn.commit()
                print(f"БД оптимизирована.")
        except Exception as _ex:
            print("Ошибка оптимизации БД", _ex)
            return False

        return True