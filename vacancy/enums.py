from enum import Enum


class ExperienceType(Enum):
    NO_EXPERIENCE = 'Опыт не требуется'
    FROM_ONE_YEAR = 'Опыт от 1 года'
    FROM_THREE_YEARS = 'Опыт 3+ лет'
    FROM_FIVE_YEAR = 'Опыт 5+ лет'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class EmploymentType(Enum):
    FULL = 'Полная'
    PART = 'Частичная'
    PRACTICE = 'Практика'
    INTERNSHIP = 'Стажировка'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class ScheduleType(Enum):
    FULL_DAY = 'Полный день'
    REMOTE = 'Удаленная работа'
    FLEXIBLE = 'Гибкий график'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
