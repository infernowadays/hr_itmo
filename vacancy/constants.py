class Constants:
    def __init__(self):
        self.__experience_types = dict({})
        self.__experience_types['1'] = 'Опыт не требуется'
        self.__experience_types['2'] = 'Опыт от 1 года'
        self.__experience_types['3'] = 'Опыт 3+ лет'
        self.__experience_types['4'] = 'Опыт 5+ лет'

        self.__employment_types = dict({})
        self.__employment_types['1'] = 'Полная'
        self.__employment_types['2'] = 'Частичная'
        self.__employment_types['3'] = 'Стажировка'
        self.__employment_types['4'] = 'Практика'

        self.__schedule_types = dict({})
        self.__schedule_types['1'] = 'Полный день'
        self.__schedule_types['2'] = 'Гибкий график'
        self.__schedule_types['3'] = 'Удаленная работа'

        self.__project_types = dict({})
        self.__project_types['1'] = 'Стартап'
        self.__project_types['2'] = 'Комьюнити'
        self.__project_types['3'] = 'Научный проект'

    def get_experience_types(self, id):
        return self.__experience_types.get(str(id), '')

    def get_employment_types(self, id):
        return self.__employment_types.get(str(id), '')

    def get_schedule_types(self, id):
        return self.__schedule_types.get(str(id), '')

    def get_project_types(self, id):
        return self.__project_types.get(str(id), '')


class ConstantsSuperJob:
    def __init__(self):
        self.__experience_types = dict({})
        self.__experience_types['1'] = '1'
        self.__experience_types['2'] = '2'
        self.__experience_types['3'] = '3'
        self.__experience_types['4'] = '4'

        self.__employment_types = dict({})
        self.__employment_types['1'] = '6'
        self.__employment_types['2'] = '10'
        self.__employment_types['3'] = '12'
        self.__employment_types['4'] = '6'

        self.__schedule_types = dict({})
        self.__schedule_types['1'] = 'Полный день'
        self.__schedule_types['2'] = 'Гибкий график'
        self.__schedule_types['3'] = 'Удаленная работа'

    def get_experience_types(self, id):
        return self.__experience_types.get(str(id), '')

    def get_employment_types(self, id):
        return self.__employment_types.get(str(id), '')

    def get_schedule_types(self, id):
        return self.__schedule_types.get(str(id), '')
