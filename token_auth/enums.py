from enum import Enum


class Sex(Enum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    UNSURE = 'UNSURE'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class Type(Enum):
    ADMINISTRATOR = 'ADMINISTRATOR'
    EMPLOYER = 'EMPLOYER'
    STUDENT = 'STUDENT'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class StudentIdType(Enum):
    TAB = 'TAB'
    DIPLOMA = 'DIPLOMA'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class Degree(Enum):
    BACHELOR = 'BACHELOR'
    MASTER = 'MASTER'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
