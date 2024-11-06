import sys
import time
import random
from datetime import datetime, date, timedelta

import database  # модуль для SQLite
import names  # Список имен и фамилий. Библиотеки не используются, для упрощения тестирования.

# Модуль FDataBase для PostgreSQL не используется. Настроен SQLite для упрощения тестирования.
# import FDataBase  # тестовый модуль для PostgreSQL

# TODO необходимо доделать
# ...

# Класс для добавления сотрудника. Имеет два метода, добавление в БД и вычисление возраста.
class Staff:
    def __init__(self, min_age=18, max_age=60, last_name="", first_name="", patronymics="", fullname="", date_birth="", gender=""):
        self.min_age = min_age
        self.max_age = max_age
        self.last_name = last_name
        self.first_name = first_name
        self.patronymics = patronymics
        self.fullname = fullname
        self.date_birth = date_birth
        self.gender = gender


    # Вставка в БД с заданными параметрами.
    def insert_into_db(self, db):
        db.add_staff(self.fullname, self.date_birth, self.gender)

    # Рассчет возраста от даты рождения.
    def calc_age(date_birth):
        birth_date = datetime.strptime(date_birth, "%Y-%m-%d")
        today = datetime.now()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


    # Генерация данных нового сотрудника.
    def generate_staff(self):
        """
        1. Генерация пола.
        2. Генерация имени, фамилии и отчества.
        3. Генерация даты рождения.
        """

        # 1. Генерация пола.
        if self.gender == "male" or self.gender == "femail":
            ...  # Если пол(валидный) передал аргументом, то оставляем как есть.
        else:  # Иначе рандомим.
            self.gender = random.choice(["male", "femail"])

        # 2. Генерация имени, фамилии и отчества.
        # Сгенерируем фамилию. Так же можно получить аргументом первую букву или фамилию полностью.
        # Определим список по заданному полу.
        if self.gender == "male":
            list_last_name = names.male_last_names
        else:
            list_last_name = names.female_last_names

        if self.last_name == "":
            self.last_name = random.choice(list_last_name)
        elif len(self.last_name) == 1:  # Получили 1 символ, то есть 1-ю букву.
            filtered_names = [name for name in list_last_name if name.startswith(self.last_name)]
            self.last_name = random.choice(filtered_names)
        else:
            self.last_name = str(self.last_name.capitalize())

        # Сгенерируем имя. Так же можно получить аргументом первую букву или имя полностью.
        # Определим список по заданному полу.
        if self.gender == "male":
            list_first_name = names.male_first_names
        else:
            list_first_name = names.female_first_names
        if self.first_name == "":
            self.first_name = random.choice(list_first_name)
        elif len(self.first_name) == 1:  # Получили 1 символ, то есть 1-ю букву.
            filtered_names = [name for name in list_first_name if name.startswith(self.first_name)]
            self.first_name = random.choice(filtered_names)
        else:
            self.first_name = str(self.first_name.capitalize())

        # Сгенерируем отчество. Так же можно получить аргументом первую букву или имя полностью.
        # Определим список по заданному полу.
        if self.gender == "male":
            list_patronymics = names.male_patronymics
        else:
            list_patronymics = names.female_patronymics
        if self.patronymics == "":
            self.patronymics = random.choice(list_patronymics)
        elif len(self.patronymics) == 1:  # Получили 1 символ, то есть 1-ю букву.
            filtered_names = [name for name in list_patronymics if name.startswith(self.patronymics)]
            self.patronymics = random.choice(filtered_names)
        else:
            self.patronymics = str(self.patronymics.capitalize())

        # Соберем полное имя. БД принимает строку Имя+Фамилия.
        self.fullname = f"{self.last_name} {self.first_name} {self.patronymics}"

        # 3. Генерация даты рождения.
        # Сгенерируем дату рождения, так чтобы возраст был не больше max_age и не меньше min_age
        today = date.today()  # Сегодняшняя дата
        start_date = today - timedelta(days=self.max_age*365)  # Максимальная дата рождения
        end_date = today - timedelta(days=self.min_age*365)  # Минимальная дата рождения
        # Выбираем случайную дату между start_date и end_date
        random_days = random.randint(0, (end_date - start_date).days)
        self.date_birth = start_date + timedelta(days=random_days)

        # Возвращаем список: имя+фамилию, дату рождения, пол
        return [self.fullname, self.date_birth, self.gender]


def main(argv):
    db = database.PersonDatabase()
    # db_postgres = FDataBase.FDataBase()  # модуль для PostgreSQL

    try:
        if argv[1] == "1":  # Создание таблицы с полями справочника сотрудников.
            print("Создание таблицы с полями справочника сотрудников.")
            db.create_table()
            # db_postgres.create_table()  # модуль для PostgreSQL


        elif argv[1] == "2":  # Создание записи справочника сотрудников.
            print("Создание записи справочника сотрудников.")
            db.add_staff(argv[2], argv[3], argv[4])

        elif argv[1] == "3":  # Вывод всех строк справочника сотрудников.
            print("Вывод всех строк справочника сотрудников.")
            start = time.time()
            staff = db.get_staff_all()
            # staff = db_postgres.get_staff_all()  # модуль для PostgreSQL
            end = time.time() - start
            for i in staff:
                age = Staff.calc_age(i[1])
                print(f"{i[0]}, {i[1]}, {i[2]}, {age} years")
            print(f"Время получения выгрузки из БД: {end}. Время потраченное на вывод в терминал не учитывается.")


        elif argv[1] == "4":  # Заполнение автоматически 1000000 строк справочника сотрудников.
            new_staff_list = []
            # Сгенерируем 1000000 сотрудников
            for _ in range(1000000):
                new_staff = Staff()
                new_staff.generate_staff()
                new_staff_list.append([new_staff.fullname, new_staff.date_birth, new_staff.gender])

            # И еще 100 с заданными параметрами
            for _ in range(100):
                new_staff = Staff(last_name="F", gender="male")
                new_staff.generate_staff()
                new_staff_list.append([new_staff.fullname, new_staff.date_birth, new_staff.gender])

            db.add_staff_from_list(new_staff_list)
            # db_postgres.add_staff_from_list(new_staff_list)  # модуль для PostgreSQL

            print("Заполнение автоматически 1000000 строк справочника сотрудников.")

        elif argv[1] == "5":  # Результат выборки из таблицы по критерию.
            print("Результат выборки из таблицы по критерию.")
            print("Вывод справочника сотрудников.")
            start = time.time()
            staff = db.get_staff(name='F', gender='male')
            # staff = db_postgres.get_staff(name='F', gender='male')  # модуль для PostgreSQL
            end = time.time() - start
            for i in staff:
                age = Staff.calc_age(i[1])
                # print(f"{i[0]}, {i[1]}, {i[2]}, {age} years")
            print(f"Время получения выгрузки из БД: {end}. Время потраченное на вывод в терминал не учитывается.")

        elif argv[1] == "6":  # Оптимизация БД отдельной командой.
            db.optimize_db()
            # db_postgres.optimize_db()  # модуль для PostgreSQL

        else:
            print("Введена не корректная команда.")
    except IndexError:
            print("Введена не корректная команда.")


if __name__ == "__main__":
    main(sys.argv)
