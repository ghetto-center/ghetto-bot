#! /usr/bin/env python3

import datetime
import random
import logging
from enum import IntEnum
Week = IntEnum('Week', 'mon tue wed thu fri sat sun', start=0)


def get_next_date():
    today = datetime.date.today()
    dt = today + datetime.timedelta(days=1)
    if dt.weekday() == Week.sat or dt.weekday() == Week.sun:
        dt = today + datetime.timedelta(days=2)
    return dt


def get_rnd_time():
    return datetime.time(random.randint(
        14, 20), random.randint(0, 59), random.randint(0, 59))


def get_next_start():
    dt = datetime.datetime.now()
    d = get_next_date()
    t = get_rnd_time()
    dt = dt.replace(
        year=d.year,
        month=d.month,
        day=d.day,
        hour=t.hour,
        minute=t.minute,
        second=t.second)
    logging.info('get_next_start:' + str(dt))
    return dt


def get_next_start_dev():
    dt = datetime.datetime.now() + datetime.timedelta(seconds=random.randint(10, 30))
    logging.info('get_next_start:' + str(dt))
    return dt


def rnd_percent(percent):
    return random.randint(1, 100) < percent
