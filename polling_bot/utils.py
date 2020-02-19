# In the name of God
import datetime
import functools
import inspect

from persian import persian
from sqlalchemy.exc import SQLAlchemyError

from config import Config
from db.base import session


class CommonRegex:
    numbers = r'([\d]+|[۰...۹]+)'


def db_persist(logger, session=session, read_only=True, fail_result=None, success_result=None):
    def decorated(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                if not read_only:
                    session.commit()
                # todo: logger.info("success calling db func: " + func.__name)
                if success_result is not None:
                    return success_result
                return result
            except SQLAlchemyError as e:
                session.rollback()
                logger.exception("error in {} {} with args {} and kwargs {}: {}".format(
                    get_staticmethod_class_name(func),
                    func.__name__, inspect.getfullargspec(func).args, args, kwargs, e))
                if fail_result is not None:
                    return fail_result

        return wrapped

    return decorated


def get_staticmethod_class_name(func):
    return getattr(inspect.getmodule(func), func.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0]).__name__


def log_error(logger):
    def decorated(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(
                    "error in {} {} with args {}: {}".format(func.__name__,
                                                             inspect.getfullargspec(func).args,
                                                             get_args_except_self_and_bot(args, kwargs),
                                                             e))

        return wrapped

    return decorated


def get_args_except_self_and_bot(args, kwargs):
    # kwargs.pop('bot')
    return kwargs


def convert_to_datetime(date_string):
    year = date_string[0:2]
    month = date_string[2:4]
    day = date_string[4:]
    date_time = datetime.datetime.strptime('13' + year
                                           + " " + month + " " + day + " 0" * 2, "%Y %m %d %H %M")

    return date_time


def is_valid_datetime_string(date_string):
    # datetime strings are supposed to be like this -> 980202
    return len(date_string) == 6


def get_readable_date(date):
    time = str(date.hour) + ":" + str(date.minute)
    date = str(date.day) + "-" + str(date.month) + "-" + str(date.year)
    date = persian.convert_en_numbers(date)
    time = persian.convert_en_numbers(time)
    return time + " " + date


def get_readable_duration(start_date, end_date):
    delta = end_date - start_date
    days = delta.days
    if not days:
        days = 1
    duration = persian.convert_en_numbers(" {} روز".format(days))
    return duration


def thousand_separator(number):
    number = int(number)
    return '{0:,}'.format(number)


def convert_date_format(datetime):
    # converts 1398-07-04 to 980704
    date = str(datetime).split(" ")[0]
    return date[2:].replace("-", "")




