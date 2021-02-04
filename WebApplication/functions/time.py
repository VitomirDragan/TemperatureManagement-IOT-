from datetime import datetime, date
import pytz


def getHourFromTimeFormat(timeFormat):
    tokens = timeFormat.split(':')
    return int(tokens[0])


def getMinuteFromTimeFormat(timeFormat):
    tokens = timeFormat.split(':')
    return int(tokens[1])


def getTime(timeFormat):
    hour = getHourFromTimeFormat(timeFormat)
    minute = getMinuteFromTimeFormat(timeFormat)

    now = datetime.now(pytz.timezone('Europe/Bucharest'))
    dateTimeObject = datetime(now.year, now.month, now.day, hour, minute)

    return dateTimeObject
