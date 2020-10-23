from enum import Enum


class Decision(Enum):
    ACCEPT = 'ACCEPT'
    DECLINE = 'DECLINE'
    NO_ANSWER = 'NO_ANSWER'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
