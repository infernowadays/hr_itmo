class Constants:
    def __init__(self):
        self.__experience_types = list([])
        self.__experience_types.append({'id': 1, 'name': 'Опыт не требуется'})
        self.__experience_types.append({'id': 2, 'name': 'Опыт от 1 года'})
        self.__experience_types.append({'id': 3, 'name': 'Опыт 3+ лет'})
        self.__experience_types.append({'id': 4, 'name': 'Опыт 5+ лет'})

        self.__employment_types = list([])
        self.__employment_types.append({'id': 1, 'name': 'Полная'})
        self.__employment_types.append({'id': 2, 'name': 'Частичная'})
        self.__employment_types.append({'id': 3, 'name': 'Стажировка'})
        self.__employment_types.append({'id': 4, 'name': 'Практика'})

        self.__schedule_types = list([])
        self.__schedule_types.append({'id': 1, 'name': 'Полный день'})
        self.__schedule_types.append({'id': 2, 'name': 'Гибкий график'})
        self.__schedule_types.append({'id': 3, 'name': 'Удаленная работа'})

    def get_experience_types(self):
        return self.__experience_types

    def get_employment_types(self):
        return self.__employment_types

    def get_schedule_types(self):
        return self.__schedule_types
