# In the name of God
from enum import Enum


class States(Enum):
    START = 0
    MENU = 1
    POLLING = 2
    EXPERIENCE_DURATION = 3
    FIELD=4
    FINISH_REGISTER=5
    QUESTION = 6
    POLLING_MESSAGE = 7
    POLLING_NAME = 8
    SHOW_QUESTIONS = 9

