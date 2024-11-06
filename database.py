import sqlite3
from datetime import date


class PersonDatabase:
    def __init__(self, db_name="staff.db"):
        self.__conn = sqlite3.connect(db_name)
        self.__cursor = self.__conn.cursor()

    # Создание таблицы.
    def create_table(self):
        try:
            with self.__conn:
                self.__cursor.execute("DROP TABLE IF EXISTS staff")  # Удалим старую таблицу(для тестов)
                print("Старая таблица удалена (для тестов).")
                self.__cursor.execute('''
                    CREATE TABLE IF NOT EXISTS staff (
                        id INTEGER PRIMARY KEY,
                        fullname TEXT NOT NULL,
                        date_birth TEXT NOT NULL,
                        gender TEXT NOT NULL
                    )
                ''')
                print("Новая таблица создана.")
                self.__conn.commit()
        except sqlite3.Error as _ex:
            print("Ошибка создания таблицы в БД", _ex)
            return False

    # Добавление сотрудника.
    def add_staff(self, fullname: str, date_birth: date, gender: str):
        try:
            with self.__conn:
                self.__cursor.execute(
                    f"INSERT INTO staff(fullname, date_birth, gender) "
                    f"VALUES(?, ?, ?)",
                    (fullname, date_birth, gender))
                self.__conn.commit()
                print(f"Сотрудник добавлен в БД.")
        except sqlite3.Error as _ex:
            print("Ошибка добавления сотрудника в БД", _ex)
            return False

        return True

    # Добавление сотрудников списком.
    def add_staff_from_list(self, staff: list):
        try:
            with self.__conn:
                self.__cursor.executemany(
                    f"INSERT INTO staff(fullname, date_birth, gender) "
                    f"VALUES(?, ?, ?)",
                    [(person[0], person[1], person[2]) for person in staff])
                self.__conn.commit()
                print(f"Сотрудник добавлен в БД.")
        except sqlite3.Error as _ex:
            print("Ошибка добавления сотрудника в БД", _ex)
            return False

        return True

    # Получение списка всех сотрудников. Более быстрый вариант, чем get_staff, который обрабатывает так же аргументы.
    # Лимит не установлен.
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
        except sqlite3.Error as _ex:
            print("Ошибка поиска сотрудников в БД", _ex)

        return False

    # Получение списка сотрудников.
    # Лимит не установлен.
    def get_staff(self, name="", gender=""):
        try:
            query = (f"SELECT fullname, date_birth, gender "
                     f"FROM staff "
                     f"WHERE SUBSTR(fullname, 1, 1) = ? and gender = ? "
                     f"ORDER BY fullname")
            parameter = (name, gender)

            with self.__conn:
                self.__cursor.execute(query, parameter)
                res = self.__cursor.fetchall()
                # print(res)
                if not res:
                    print("Staff not found")
                    return False

            return res
        except sqlite3.Error as _ex:
            print("Ошибка поиска сотрудников в БД", _ex)

        return False

    # Оптимизация БД.
    def optimize_db(self):
        try:
            with self.__conn:
                self.__cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_first_letter_fullname ON staff(SUBSTR(fullname, 1, 1))")
                self.__conn.commit()
                print(f"БД оптимизирована.")
        except sqlite3.Error as _ex:
            print("Ошибка оптимизации БД", _ex)
            return False

        return True




    def close(self):
        self.__conn.close()
